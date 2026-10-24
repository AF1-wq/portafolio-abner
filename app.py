import os
import re
import hmac
import ssl
import sqlite3
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = (BASE_DIR / "public").resolve()
DB_PATH = BASE_DIR / "messages.db"

load_dotenv()

# Habilitar CSP y HTTPS en producción respetando estrictamente los estilos y scripts del diseño
is_prod = os.environ.get("FLASK_ENV") == "production" or os.environ.get("RENDER") == "true" or "DYNO" in os.environ

app = Flask(__name__, static_folder=None)

# [SEGURIDAD] Clave secreta: en producción debe venir del entorno (una clave aleatoria por
# proceso invalida sesiones entre workers de gunicorn y entre reinicios).
_secret = os.environ.get("FLASK_SECRET_KEY", "")
if not _secret or _secret == "change-this-to-a-long-random-secret":
    if is_prod:
        print("[SEGURIDAD] ADVERTENCIA: FLASK_SECRET_KEY no configurada en producción.")
    _secret = os.urandom(32).hex()
app.secret_key = _secret

app.config.update(
    # [SEGURIDAD] Limita el tamaño del cuerpo de la petición (evita DoS por payloads enormes)
    MAX_CONTENT_LENGTH=32 * 1024,
    MAX_FORM_MEMORY_SIZE=32 * 1024,
    MAX_FORM_PARTS=50,
    # [SEGURIDAD] Cookies endurecidas
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=is_prod,
    JSON_SORT_KEYS=False,
)
Compress(app)

# Pool controlado de hilos para envío de correos asíncronos sin agotar recursos
mail_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="mail_worker")

# [SEGURIDAD] CSP ajustada a los recursos que realmente usa el sitio:
#  - Se eliminó 'unsafe-eval' (el código no usa eval/new Function).
#  - Se eliminaron CDNs no utilizados (jquery/cdnjs): todas las librerías están embebidas.
#  - Se añadieron los dominios de Google Analytics (gtag) que antes quedaban bloqueados.
#  - 'unsafe-inline' se mantiene porque el diseño usa scripts/estilos embebidos.
_ga_hosts = [
    "https://www.googletagmanager.com",
    "https://*.google-analytics.com",
    "https://*.analytics.google.com",
    "https://stats.g.doubleclick.net",
    "https://www.google.com",
]
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'", "https://www.googletagmanager.com"],
    'style-src': ["'self'", "'unsafe-inline'"],
    'font-src': ["'self'", "data:"],
    'img-src': ["'self'", "data:", "https:"],
    'media-src': ["'self'", "data:", "blob:"],
    'connect-src': ["'self'"] + _ga_hosts,
    'object-src': ["'none'"],
    'base-uri': ["'self'"],
    'form-action': ["'self'"],
    'frame-ancestors': ["'none'"],
}
Talisman(
    app,
    content_security_policy=csp if is_prod else None,
    force_https=is_prod,
    strict_transport_security=is_prod,
    strict_transport_security_max_age=31536000,
    strict_transport_security_include_subdomains=True,
    frame_options="DENY",
    referrer_policy="strict-origin-when-cross-origin",
    session_cookie_secure=is_prod,
    permissions_policy={
        "geolocation": "()",
        "camera": "()",
        "microphone": "()",
        "payment": "()",
        "usb": "()",
    },
)

if is_prod:
    # [SEGURIDAD] Solo se confía en X-Forwarded-For / X-Forwarded-Proto del proxy de la plataforma.
    # No se confía en X-Forwarded-Host / Prefix (evita Host header injection).
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Backend explícito para Limiter (permite Redis mediante RATELIMIT_STORAGE_URI o fallback a memoria sin advertencias)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "100 per hour"],
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
)

# ---------------------------------------------------------------------------
# Utilidades de validación / saneamiento
# ---------------------------------------------------------------------------
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]{1,64}@[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?)+$")
# Caracteres de control (incluye CR/LF) que permitirían inyección en cabeceras de correo o logs
_CTRL_RE = re.compile(r"[\x00-\x1f\x7f\u2028\u2029]")
_CTRL_KEEP_NL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

MAX_LEN = {"name": 150, "email": 150, "company": 150, "service": 300, "message": 4000, "source": 60}


def _clean_line(value) -> str:
    """Texto de una sola línea: elimina CR/LF y caracteres de control (anti header/log injection)."""
    return _CTRL_RE.sub(" ", str(value or "")).strip()


def _clean_multiline(value) -> str:
    """Texto multilínea: conserva saltos de línea pero elimina otros caracteres de control."""
    return _CTRL_KEEP_NL_RE.sub("", str(value or "")).strip()


def _smtp_send(smtp_user: str, smtp_password: str, msg) -> None:
    # [SEGURIDAD] STARTTLS con verificación de certificado y hostname.
    # smtplib por defecto NO verifica el certificado, lo que permitiría un MITM
    # capaz de robar la contraseña de aplicación de Gmail.
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_password)
        server.send_message(msg)


def init_db():
    with sqlite3.connect(DB_PATH, timeout=30.0) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                company TEXT,
                service TEXT,
                source TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Migración automática de columnas para bases de datos existentes
        cursor.execute("PRAGMA table_info(messages)")
        cols = [col[1] for col in cursor.fetchall()]
        for col_name in ["company", "service", "source"]:  # lista fija (no proviene del usuario)
            if col_name not in cols:
                try:
                    cursor.execute(f"ALTER TABLE messages ADD COLUMN {col_name} TEXT")
                except sqlite3.OperationalError:
                    pass
        conn.commit()

init_db()

# ---------------------------------------------------------------------------
# Archivos estáticos
# ---------------------------------------------------------------------------
# [SEGURIDAD] Allowlist de extensiones públicas: impide servir scripts (.py), bases de datos,
# archivos de configuración o cualquier otro archivo que acabe por error dentro de /public.
ALLOWED_STATIC_EXT = {
    ".html", ".css", ".js", ".json", ".txt", ".xml", ".webmanifest",
    ".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".avif",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp4", ".webm", ".mp3", ".ogg", ".pdf",
}


def _is_allowed_static(relative_path: str) -> bool:
    if not relative_path or "\x00" in relative_path or "\\" in relative_path:
        return False
    parts = relative_path.split("/")
    # Bloquea rutas/archivos ocultos (.git, .env, ...), segmentos vacíos y traversal (..)
    if any(p.startswith(".") or p == "" for p in parts):
        return False
    return Path(relative_path).suffix.lower() in ALLOWED_STATIC_EXT


def _safe_send(relative_path: str):
    if not _is_allowed_static(relative_path):
        abort(404)
    try:
        file_path = (PUBLIC_DIR / relative_path).resolve()
    except (OSError, ValueError):
        abort(404)
    if file_path == PUBLIC_DIR or PUBLIC_DIR not in file_path.parents:
        abort(404)
    if not file_path.is_file():
        abort(404)
    # Cache estático de 1 año (31536000 s) para assets y fuentes; revalidación para HTML (evita caché obsoleto en Barba.js)
    ext = Path(relative_path).suffix.lower()
    if ext == ".html":
        max_age = 0
    elif any(relative_path.startswith(prefix) for prefix in ["assets/", "fonts/"]):
        max_age = 31536000
    else:
        max_age = None
    response = send_from_directory(PUBLIC_DIR, relative_path, max_age=max_age)
    if ext == ".html":
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    elif ext in {'.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'}:
        response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    return response

@app.get("/")
def home():
    return _safe_send("index.html")

@app.get("/assets/<path:filename>")
def assets(filename: str):
    return _safe_send(f"assets/{filename}")

@app.post("/api/test-email")
@limiter.limit("5 per hour")
def test_email():
    # [SEGURIDAD] Endpoint administrativo: antes era público (GET) y permitía a cualquiera
    # disparar correos y ver mensajes de error internos. Ahora requiere ADMIN_TOKEN
    # (cabecera X-Admin-Token) y queda deshabilitado si no está configurado.
    admin_token = os.environ.get("ADMIN_TOKEN", "")
    provided = request.headers.get("X-Admin-Token", "")
    if len(admin_token) < 24 or not hmac.compare_digest(provided.encode(), admin_token.encode()):
        abort(404)

    try:
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
        
        if not smtp_user or not smtp_password:
            return jsonify({"ok": False, "error": "Credenciales SMTP no configuradas"}), 500

        msg = MIMEMultipart()
        msg['From'] = formataddr(("Portafolio Abner Franco", smtp_user))
        msg['To'] = smtp_user
        msg['Subject'] = "🔔 Test de Verificación SMTP - Portafolio"
        
        cuerpo = (
            "Prueba de conectividad SMTP exitosa.\n"
            "El servidor de correos del portafolio está funcionando y listo para recibir mensajes de clientes."
        )
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        
        _smtp_send(smtp_user, smtp_password, msg)
        return jsonify({"ok": True, "message": "Correo de prueba enviado con éxito"})
    except Exception:
        app.logger.exception("Error en test-email")
        # [SEGURIDAD] No se devuelve el detalle de la excepción al cliente
        return jsonify({"ok": False, "error": "Error al enviar el correo de prueba"}), 500


@app.get("/<path:requested_path>")
def static_files(requested_path: str):
    requested_path = requested_path.rstrip('/')
    if not requested_path:
        return _safe_send('index.html')
    if requested_path.startswith("api/"):
        abort(404)

    # [SEGURIDAD] Validación previa: no se toca el sistema de archivos con rutas sospechosas
    if "\x00" in requested_path or "\\" in requested_path or any(
        p.startswith(".") for p in requested_path.split("/")
    ):
        abort(404)

    # 1. Archivo directo
    if _is_allowed_static(requested_path):
        candidate = PUBLIC_DIR / requested_path
        if candidate.is_file():
            return _safe_send(requested_path)

    # 2. Alias con extensión .html (ej. /contact -> contact.html)
    candidate_html = PUBLIC_DIR / f"{requested_path}.html"
    if candidate_html.is_file():
        return _safe_send(f"{requested_path}.html")

    # 3. Solicitud de index o fallback al inicio
    return _safe_send("index.html")


def _send_email_async(smtp_user, smtp_password, email, name, message, source, company="", service=""):
    try:
        msg = MIMEMultipart()
        msg['From'] = formataddr(("Portafolio Abner Franco", smtp_user))
        msg['To'] = smtp_user
        msg['Reply-To'] = email  # validado con EMAIL_RE (sin CR/LF)

        if source == "nova-ai":
            msg['Subject'] = f"🤖 [NØVA AI] Mensaje recibido de: {name}"
            cuerpo = (
                f"━━━ Mensaje recibido vía NØVA·AF (Chatbot IA) ━━━\n\n"
                f"👤 Nombre: {name}\n"
                f"📧 Correo del cliente: {email}\n\n"
                f"💬 Mensaje:\n{message}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Este mensaje fue recopilado automáticamente desde el chat de IA.\n"
                f"👉 Haz clic en 'Responder' en tu correo para escribirle directamente a {email}."
            )
        else:
            asunto_extra = f" ({company})" if company else ""
            msg['Subject'] = f"📩 [Portafolio] Nuevo mensaje de: {name}{asunto_extra}"
            
            detalles = [
                f"👤 Nombre: {name}",
                f"📧 Correo del cliente: {email}"
            ]
            if company:
                detalles.append(f"🏢 Organización / Empresa: {company}")
            if service:
                detalles.append(f"🛠️ Servicios de interés: {service}")

            info_bloque = "\n".join(detalles)

            cuerpo = (
                f"━━━ Nuevo mensaje desde el Portafolio Web ━━━\n\n"
                f"{info_bloque}\n\n"
                f"💬 Mensaje:\n{message}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Origen: {source or 'Formulario de Contacto Web'}\n\n"
                f"👉 Haz clic en 'Responder' en tu correo para responder directamente a {name} ({email})."
            )
        
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        
        _smtp_send(smtp_user, smtp_password, msg)
        app.logger.info("Correo enviado exitosamente (Origen: %r)", source or 'formulario')
    except Exception:
        app.logger.exception("Error al enviar el correo SMTP asíncrono")

@app.post("/api/send-message")
@limiter.limit("5 per minute; 30 per hour; 100 per day")
def send_message():
    # [SEGURIDAD] Prevención CSRF: Se requiere Content-Type application/json explícito
    if not request.is_json:
        return jsonify({"error": "Content-Type application/json requerido"}), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        data = {}
    
    # Campo trampa anti-spam (honeypot)
    honeypot = _clean_line(data.get("tel", ""))
    if honeypot:
        app.logger.warning("Spam bot detectado y bloqueado (honeypot): %r", honeypot[:100])
        return jsonify({"ok": True, "message": "Mensaje recibido correctamente"}), 200

    # [SEGURIDAD] Saneamiento: campos de una línea sin CR/LF (anti email header injection)
    name = _clean_line(data.get("name", ""))
    email = _clean_line(data.get("email", ""))
    company = _clean_line(data.get("company", ""))
    service = _clean_line(data.get("service", ""))
    message = _clean_multiline(data.get("message", ""))
    source = _clean_line(data.get("source", ""))

    if not name or not email or not message:
        return jsonify({"error": "Por favor completa los campos obligatorios: Nombre, Correo y Mensaje"}), 400
        
    fields = {"name": name, "email": email, "company": company, "service": service, "message": message, "source": source}
    if any(len(fields[k]) > MAX_LEN[k] for k in fields):
        return jsonify({"error": "Los campos superan la longitud máxima permitida"}), 400

    # [SEGURIDAD] Validación de formato de correo (se usa en la cabecera Reply-To)
    if not EMAIL_RE.match(email):
        return jsonify({"error": "Por favor ingresa un correo electrónico válido"}), 400

    try:
        with sqlite3.connect(DB_PATH, timeout=30.0) as conn:
            cursor = conn.cursor()
            # Consulta parametrizada (protección contra SQL injection)
            cursor.execute(
                "INSERT INTO messages (name, email, message, company, service, source, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, email, message, company, service, source or "Formulario Web", datetime.now().isoformat())
            )
            conn.commit()
        app.logger.info("Mensaje guardado en DB (source: %r)", source or "formulario")
        
        # Enviar correo de manera asíncrona mediante ThreadPoolExecutor controlado
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
        
        if smtp_user and smtp_password:
            mail_executor.submit(
                _send_email_async,
                smtp_user, smtp_password, email, name, message, source, company, service
            )
        else:
            app.logger.warning("Credenciales SMTP no configuradas. El mensaje se guardó en BD pero no se envió correo.")

        return jsonify({"ok": True, "message": "¡Mensaje recibido y enviado correctamente!"}), 200
    except Exception:
        app.logger.exception("Error procesando mensaje en /api/send-message")
        return jsonify({"error": "Error interno al procesar el mensaje"}), 500


# ---------------------------------------------------------------------------
# Manejadores de error (respuestas genéricas, sin filtrar información interna)
# ---------------------------------------------------------------------------
@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": "La petición es demasiado grande"}), 413


@app.errorhandler(429)
def too_many(_e):
    return jsonify({"error": "Demasiadas solicitudes. Intenta de nuevo más tarde."}), 429


@app.errorhandler(500)
def internal_error(_e):
    return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == "__main__":
    debug = os.environ.get("FLASK_ENV") == "development" and not is_prod
    app.run(
        # [SEGURIDAD] Con debug activo se escucha solo en localhost: el debugger de Werkzeug
        # permite ejecución remota de código si queda expuesto en la red.
        host="127.0.0.1" if debug else "0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=debug,
    )
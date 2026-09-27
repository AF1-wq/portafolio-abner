import os
import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor

import requests
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
DB_PATH = BASE_DIR / "messages.db"

load_dotenv()

app = Flask(__name__, static_folder=None)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24).hex()
Compress(app)

# Pool controlado de hilos para envío de correos asíncronos sin agotar recursos
mail_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="mail_worker")

# Habilitar CSP y HTTPS en producción respetando estrictamente los estilos y scripts del diseño
is_prod = os.environ.get("FLASK_ENV") == "production" or os.environ.get("RENDER") == "true"
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://code.jquery.com", "https://cdnjs.cloudflare.com"],
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
    'font-src': ["'self'", "https://fonts.gstatic.com", "data:"],
    'img-src': ["'self'", "data:", "https:"],
    'connect-src': ["'self'"],
}
Talisman(app, content_security_policy=csp if is_prod else None, force_https=is_prod)

if is_prod:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Backend explícito para Limiter (permite Redis mediante RATELIMIT_STORAGE_URI o fallback a memoria sin advertencias)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "100 per hour"],
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
)

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
        for col_name in ["company", "service", "source"]:
            if col_name not in cols:
                try:
                    cursor.execute(f"ALTER TABLE messages ADD COLUMN {col_name} TEXT")
                except sqlite3.OperationalError:
                    pass
        conn.commit()

init_db()

def _safe_send(relative_path: str):
    file_path = (PUBLIC_DIR / relative_path).resolve()
    if file_path == PUBLIC_DIR or PUBLIC_DIR not in file_path.parents:
        abort(404)
    if not file_path.is_file():
        abort(404)
    # Cache estático de 1 año (31536000 s) para assets y fuentes
    max_age = 31536000 if any(relative_path.startswith(prefix) for prefix in ["assets/", "fonts/"]) else None
    return send_from_directory(PUBLIC_DIR, relative_path, max_age=max_age)

@app.get("/")
def home():
    return _safe_send("index.html")

@app.get("/assets/<path:filename>")
def assets(filename: str):
    return send_from_directory(PUBLIC_DIR / "assets", filename, max_age=31536000)

@app.get("/api/test-email")
@limiter.limit("10 per day")
def test_email():
    try:
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
        
        if not smtp_user or not smtp_password:
            return jsonify({"ok": False, "error": "Credenciales MAIL_USERNAME o MAIL_PASSWORD no configuradas"}), 500

        msg = MIMEMultipart()
        msg['From'] = f"Portafolio Abner Franco <{smtp_user}>"
        msg['To'] = smtp_user
        msg['Subject'] = "🔔 Test de Verificación SMTP - Portafolio"
        
        cuerpo = (
            "Prueba de conectividad SMTP exitosa.\n"
            "El servidor de correos del portafolio está funcionando y listo para recibir mensajes de clientes."
        )
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return jsonify({"ok": True, "message": f"Correo de prueba enviado con éxito a {smtp_user}"})
    except Exception as e:
        app.logger.exception("Error en test-email: %s", str(e))
        return jsonify({"ok": False, "error": str(e)}), 500


@app.get("/<path:requested_path>")
def static_files(requested_path: str):
    if requested_path.startswith("api/"):
        abort(404)

    # 1. Archivo directo
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
        msg['From'] = f"Portafolio Abner Franco <{smtp_user}>"
        msg['To'] = smtp_user
        msg['Reply-To'] = email

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
        
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        app.logger.info("Correo enviado exitosamente a %s (Cliente: %s, Origen: %s)", smtp_user, email, source or 'formulario')
    except Exception as e:
        app.logger.exception("Error al enviar el correo SMTP asíncrono: %s", str(e))

@app.post("/api/send-message")
@limiter.limit("15 per minute")
def send_message():
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    
    # Campo trampa anti-spam (honeypot)
    honeypot = str(data.get("tel", "")).strip()
    if honeypot:
        app.logger.warning("Spam bot detectado y bloqueado (honeypot): %s", honeypot)
        return jsonify({"ok": True, "message": "Mensaje recibido correctamente"}), 200

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    company = str(data.get("company", "")).strip()
    service = str(data.get("service", "")).strip()
    message = str(data.get("message", "")).strip()
    source = str(data.get("source", "")).strip()

    if not name or not email or not message:
        return jsonify({"error": "Por favor completa los campos obligatorios: Nombre, Correo y Mensaje"}), 400
        
    if len(name) > 150 or len(email) > 150 or len(message) > 4000:
        return jsonify({"error": "Los campos superan la longitud máxima permitida"}), 400

    try:
        with sqlite3.connect(DB_PATH, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (name, email, message, company, service, source, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, email, message, company, service, source or "Formulario Web", datetime.now().isoformat())
            )
            conn.commit()
        app.logger.info("Mensaje guardado en DB: %s <%s> (source: %s)", name, email, source or "formulario")
        
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
    except Exception as e:
        app.logger.exception("Error procesando mensaje en /api/send-message: %s", str(e))
        return jsonify({"error": "Error interno al procesar el mensaje"}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )
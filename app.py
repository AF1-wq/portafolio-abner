import os
import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

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
Compress(app)

# Habilitar CSP y HTTPS en producción
is_prod = os.environ.get("FLASK_ENV") == "production" or os.environ.get("RENDER") == "true"
csp = {
    'default-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com", "https://fonts.gstatic.com"],
    'img-src': ["'self'", "data:", "https:"],
}
Talisman(app, content_security_policy=csp if is_prod else None, force_https=is_prod)

if is_prod:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

limiter = Limiter(get_remote_address, app=app, default_limits=["300 per day", "100 per hour"])

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
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
                except Exception:
                    pass
        conn.commit()

init_db()

def _safe_send(relative_path: str):
    file_path = (PUBLIC_DIR / relative_path).resolve()
    if file_path == PUBLIC_DIR or PUBLIC_DIR not in file_path.parents:
        abort(404)
    if not file_path.is_file():
        abort(404)
    return send_from_directory(PUBLIC_DIR, relative_path)

@app.get("/")
def home():
    return _safe_send("index.html")

@app.get("/assets/<path:filename>")
def assets(filename: str):
    return send_from_directory(PUBLIC_DIR / "assets", filename)

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
        app.logger.error("Error en test-email: %s", str(e))
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
        print(f" Correo enviado exitosamente a {smtp_user} (Cliente: {email}, Origen: {source or 'formulario'})")
    except Exception as e:
        print(f" Error al enviar el correo SMTP: {str(e)}")

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
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (name, email, message, company, service, source, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, email, message, company, service, source or "Formulario Web", datetime.now().isoformat())
            )
            conn.commit()
        app.logger.info("Mensaje guardado en DB: %s <%s> (source: %s)", name, email, source or "formulario")
        
        # Enviar correo de manera asíncrona
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
        
        if smtp_user and smtp_password:
            threading.Thread(
                target=_send_email_async,
                args=(smtp_user, smtp_password, email, name, message, source, company, service)
            ).start()
        else:
            app.logger.warning("Credenciales SMTP no configuradas. El mensaje se guardó en BD pero no se envió correo.")

        return jsonify({"ok": True, "message": "¡Mensaje recibido y enviado correctamente!"}), 200
    except Exception as e:
        app.logger.error("Error procesando mensaje: %s", str(e))
        return jsonify({"error": "Error interno al procesar el mensaje"}), 500

@app.post("/api/chat")
@limiter.limit("15 per minute")
def chat_endpoint():
    payload = request.get_json(silent=True) or {}
    user_message = str(payload.get("message", "")).strip()
    history = payload.get("history", [])

    if not user_message or len(user_message) > 500:
        return jsonify({"error": "Mensaje inválido o demasiado largo"}), 400

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Falta configurar la variable GROQ_API_KEY en el servidor"}), 500

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "Tu nombre es NØVA. Eres la asistente de IA personal de Abner Franco, integrada en su portafolio web abnerfranco.me. "
        "Habla como una persona real que está atendiendo — nada de listas robóticas ni frases de manual. "
        "Sé cercana, directa y natural. Usa español coloquial pero profesional, como alguien que de verdad te está ayudando. "
        "Puedes usar emojis con moderación. Respuestas cortas y al punto, no te enrolles.\n\n"
        
        "PROYECTOS DE ABNER:\n"
        "- Teleprompter By AF: app web para creadores de contenido, ajusta velocidad y texto en vivo. JS puro, GitHub Pages.\n"
        "- INSAM Salud: plataforma de gestión hospitalaria para estudiantes. Python/Flask/SQL, en DigitalOcean.\n"
        "- FarmacoLandia: juego web interactivo para aprender farmacología. JS + CSS.\n"
        "- Este portafolio: plataforma web multi-página (Inicio, Proyectos, Sobre mí, Contacto, Archivo) desarrollada con Python/Flask y un diseño editorial interactivo de alto impacto.\n\n"
        
        "SOBRE ABNER:\n"
        "- Estudiante de 2° año de Laboratorio Químico en ITCA-FEPADE + Desarrollador Web.\n"
        "- Maneja Python, Flask, SQL, HTML/CSS/JS, Git, IA/Prompt Engineering, análisis químico.\n"
        "- Trabajó como Ejecutivo de Venta en Crece Centro América y Auxiliar en Advance Energy (energías renovables).\n\n"
        
        "ENVÍO DE MENSAJES — FUNCIÓN ESPECIAL:\n"
        "Si alguien quiere contactar a Abner, mandarle un mensaje, o hablar con él sobre trabajo/proyectos, "
        "TÚ PUEDES recopilar sus datos y enviarlo directamente. Haz esto de forma NATURAL, paso a paso:\n"
        "1. Pregunta su nombre de forma casual\n"
        "2. Luego pide su correo electrónico\n"
        "3. Finalmente pregunta qué le quiere decir a Abner\n"
        "NO pidas los 3 datos de golpe. Uno por uno, conversando.\n\n"
        
        "IMPORTANTE — Cuando ya tengas los 3 datos (nombre, email y mensaje), incluye AL FINAL de tu respuesta "
        "este bloque EXACTO (el usuario no lo verá, el sistema lo procesa):\n"
        "<!--CONTACT_DATA:{\"name\":\"NOMBRE\",\"email\":\"EMAIL\",\"message\":\"MENSAJE\"}-->\n"
        "Reemplaza NOMBRE, EMAIL y MENSAJE con los datos reales del usuario. "
        "En tu texto visible, confirma que ya enviaste el mensaje y que Abner responderá pronto.\n\n"
        
        "LÍMITES:\n"
        "- No inventes proyectos ni datos que no estén aquí.\n"
        "- Temas fuera del ámbito de Abner, tecnología o química → redirige amablemente al portafolio.\n"
        "- Nunca pidas contraseñas, tarjetas, DUI ni datos médicos sensibles."
    )

    messages = [{"role": "system", "content": system_instruction}]
    
    # Limitar historial a los últimos 10 mensajes para no exceder tokens
    for msg in history[-10:]:
        role = msg.get("role")
        content = msg.get("content")
        if role in ["user", "assistant"] and isinstance(content, str):
            messages.append({"role": role, "content": content})
            
    messages.append({"role": "user", "content": user_message})

    model_name = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")
    body = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 350
    }

    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        res.raise_for_status()
        data = res.json()
        bot_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not bot_reply:
            bot_reply = "Lo siento, no pude generar una respuesta en este momento."

        # Procesar datos de contacto recopilados por la IA
        contact_match = re.search(r'<!--CONTACT_DATA:\s*(\{.*?\})\s*-->', bot_reply)
        if contact_match:
            try:
                contact_info = json.loads(contact_match.group(1))
                c_name = str(contact_info.get("name", "")).strip()
                c_email = str(contact_info.get("email", "")).strip()
                c_msg = str(contact_info.get("message", "")).strip()
                
                if c_name and c_email and c_msg:
                    with sqlite3.connect(DB_PATH) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO messages (name, email, message, company, service, source, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (c_name, c_email, c_msg, "", "", "nova-ai", datetime.now().isoformat())
                        )
                        conn.commit()
                    
                    smtp_user = os.environ.get("MAIL_USERNAME")
                    smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
                    if smtp_user and smtp_password:
                        threading.Thread(
                            target=_send_email_async,
                            args=(smtp_user, smtp_password, c_email, c_name, c_msg, "nova-ai")
                        ).start()
            except Exception as parse_err:
                app.logger.error("Error al procesar CONTACT_DATA del chatbot: %s", str(parse_err))
            
            # Limpiar la etiqueta oculta de la respuesta al usuario
            bot_reply = re.sub(r'<!--CONTACT_DATA:\s*\{.*?\}\s*-->', '', bot_reply).strip()

        return jsonify({"reply": bot_reply}), 200
    except Exception as e:
        app.logger.error("Error en Groq API: %s", str(e))
        return jsonify({"error": "Error al comunicarse con el servicio de IA"}), 502

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )
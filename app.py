import os
import sqlite3
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

BASE_DIR = Path(__file__).resolve().parent
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

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

def _safe_send(relative_path: str):
    file_path = (BASE_DIR / relative_path).resolve()
    if file_path == BASE_DIR or BASE_DIR not in file_path.parents:
        abort(404)
    if not file_path.is_file():
        abort(404)
    return send_from_directory(BASE_DIR, relative_path)

@app.get("/")
def home():
    return _safe_send("index.html")

@app.get("/assets/<path:filename>")
def assets(filename: str):
    return send_from_directory(BASE_DIR / "assets", filename)

@app.get("/api/test-email")
def test_email():
    try:
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = smtp_user
        msg['Subject'] = "Test Email from API"
        msg.attach(MIMEText("Este es un mensaje de prueba", 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return jsonify({"ok": True, "message": "Test email sent!"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.get("/<path:requested_path>")
def static_files(requested_path: str):
    if requested_path.startswith("api/"):
        abort(404)

    candidate = BASE_DIR / requested_path
    if candidate.is_file():
        return _safe_send(requested_path)

    return _safe_send("index.html")

@app.post("/api/send-message")
def send_message():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    message = str(payload.get("message", "")).strip()
    source = str(payload.get("source", "")).strip()  # "nova-ai" o vacío

    if not name or not email or not message:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (name, email, message, timestamp) VALUES (?, ?, ?, ?)",
                (name, email, message, datetime.now().isoformat())
            )
            conn.commit()
        app.logger.info("Mensaje guardado en DB de %s <%s> (source: %s)", name, email, source or "formulario")
        
        # Enviar correo si están configuradas las credenciales SMTP en el .env
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")
        
        if smtp_user and smtp_password:
            try:
                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = smtp_user
                msg['Reply-To'] = email

                # Diferenciar asunto según el origen del mensaje
                if source == "nova-ai":
                    msg['Subject'] = f"[NØVA·AF] Mensaje automatizado de: {name}"
                    cuerpo = (
                        f"━━━ Mensaje enviado vía NØVA·AF (Chatbot IA) ━━━\n\n"
                        f"Nombre: {name}\n"
                        f"Correo: {email}\n\n"
                        f"Mensaje:\n{message}\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"Este mensaje fue recopilado automáticamente por NØVA·AF\n"
                        f"desde el chat de IA del portafolio."
                    )
                else:
                    msg['Subject'] = f"Nuevo mensaje en Portafolio de: {name}"
                    cuerpo = f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}"
                
                msg.attach(MIMEText(cuerpo, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                server.quit()
                app.logger.info("Correo enviado exitosamente para %s (source: %s)", email, source or "formulario")
            except Exception as e:
                app.logger.error("Error al enviar el correo SMTP: %s", str(e))
        else:
            app.logger.warning("Credenciales SMTP no configuradas. El correo no se envió, pero sí se guardó en BD.")

        return jsonify({"ok": True, "message": "Mensaje recibido correctamente"}), 200
    except Exception as e:
        app.logger.error("Error guardando mensaje en DB: %s", str(e))
        return jsonify({"error": "Error interno al guardar el mensaje"}), 500

@app.post("/api/chat")
@limiter.limit("10 per minute")
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
        "- Este portafolio: hecho desde cero con Python/Flask, diseño Glassmorphism.\n\n"
        
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
    
    for msg in history:
        role = msg.get("role")
        content = msg.get("content")
        if role in ["user", "assistant"] and isinstance(content, str):
            messages.append({"role": role, "content": content})
            
    messages.append({"role": "user", "content": user_message})

    body = {
        "model": "llama-3.3-70b-versatile",
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
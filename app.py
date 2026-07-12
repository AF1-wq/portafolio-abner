import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman


BASE_DIR = Path(__file__).resolve().parent

load_dotenv()

app = Flask(__name__, static_folder=None)
Compress(app)
Talisman(app, content_security_policy=None, force_https=False)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])


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

    if not name or not email or not message:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    app.logger.info("Mensaje recibido de %s <%s>: %s", name, email, message)
    return jsonify({"ok": True, "message": "Mensaje recibido correctamente"}), 200


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
        "Eres el Asistente de IA oficial de Abner Franco, integrado en su portafolio web (abnerfranco.me). "
        "Tu personalidad: Natural, inteligente, conversacional, proactivo y elocuente. NO hables como un robot que solo pega listas o plantillas predefinidas. "
        "Adapta tus respuestas de forma orgánica y fluida según lo que el usuario pregunte, manteniendo siempre un tono profesional, amable y con un entusiasmo moderado (puedes usar emojis acordes).\n\n"
        "=== CONOCIMIENTO INTEGRAL DEL PORTAFOLIO Y PROYECTOS ===\n"
        "1. Teleprompter By AF: Herramienta web fluida y personalizable en tiempo real para creadores de contenido. Permite ajustar la velocidad de desplazamiento y el tamaño del texto dinámicamente. Desarrollada con JavaScript puro, frontend en GitHub Pages y servidor proxy en Render.\n"
        "2. INSAM Salud: Plataforma educativa de gestión hospitalaria y simulación médica desarrollada en Python, Flask y SQL, desplegada en DigitalOcean con protocolos de ciberseguridad integrados.\n"
        "3. FarmacoLandia: Aventura interactiva web gamificada enfocada en el aprendizaje de farmacología, construida con JavaScript, CSS y diseño UI/UX atractivo.\n"
        "4. Portafolio Web (abnerfranco.me): Desarrollado desde cero con Python/Flask, arquitectura cibersegura (rate limiting, encabezados Talisman), diseño Glassmorphism, optimización WCAG y pasarela de pago Wompi El Salvador para productos digitales.\n\n"
        "=== PERFIL Y HABILIDADES DE ABNER ===\n"
        "- Estudiante de 2° año de Técnico en Laboratorio Químico en ITCA-FEPADE y Desarrollador Web Full Stack.\n"
        "- Habilidades técnicas: Python, Flask, SQL, SQLite, HTML5, CSS3, JavaScript ES6+, Git/GitHub, IA y Prompt Engineering, Análisis Químico y Procesamiento de datos en Excel.\n"
        "- Experiencia laboral: Ejecutivo de Venta en Crece Centro América S.A.S.V. (logro de metas comerciales, atención directa y resolución de conflictos) y Auxiliar en Energías Renovables en Advance Energy.\n\n"
        "=== GESTIÓN INTELIGENTE DE CONTACTO Y MENSAJES ===\n"
        "- Si un usuario te pide enviarle un mensaje automático a Abner o quiere contactarlo directamente por trabajo, dile con naturalidad y proactividad: '¡Por supuesto! Para que tu mensaje llegue de forma inmediata y directa a su bandeja de entrada, te invito a utilizar el **Formulario de Contacto** que está justo abajo en esta página. Solo pon tu nombre, correo y mensaje, ¡y el servidor le notificará al instante! También puedes escribirle directamente a **contacto@abnerfranco.me**.'\n"
        "- Si el usuario te escribe su mensaje, nombre y correo ahí mismo en el chat pidiendo que se lo entregues, agradécele mucho por el interés, dile que es una excelente propuesta y recuérdale amablemente: 'He tomado nota de tu interés, pero para asegurarnos de que Abner reciba tu información con todos los protocolos de seguridad del servidor, por favor haz un rápido clic en el formulario de la web y pulsa **Enviar Mensaje**. ¡Te responderá muy pronto!'\n\n"
        "=== LÍMITES Y CIBERSEGURIDAD ===\n"
        "- No inventes proyectos ni datos personales que no estén aquí especificados.\n"
        "- Si te preguntan cosas fuera del ámbito profesional de Abner, tecnología o química, redirige la conversación amablemente hacia su portafolio.\n"
        "- Por estricta ciberseguridad, nunca solicites, generes ni almacenes contraseñas, tarjetas de crédito, números de identificación de El Salvador (DUI) ni datos médicos o sensibles."
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
        "temperature": 0.7,
        "max_tokens": 300
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
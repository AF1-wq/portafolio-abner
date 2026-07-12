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
        "Eres el asistente virtual de Abner Franco, integrado en su portafolio web. "
        "Tono: Profesional, amable, conciso y entusiasta. Usa emojis donde sea oportuno.\n"
        "Información sobre Abner:\n"
        "- Estudiante de 2° año de Laboratorio Químico en ITCA-FEPADE y Desarrollador Web Full Stack.\n"
        "- Proyectos clave: 'INSAM Salud' (plataforma médica hospitalaria en Python/SQL) y 'FarmacoLandia' (app interactiva sobre farmacología en JS).\n"
        "- Habilidades: Python, Flask, SQL, HTML/CSS/JS, Análisis Químico, Procesamiento de datos, APIs REST.\n"
        "- Experiencia: Ejecutivo de Venta en Crece Centro América S.A.S.V. y Auxiliar en Energías Renovables en Advance Energy.\n"
        "- Contacto: contacto@abnerfranco.me, LinkedIn o GitHub.\n"
        "Reglas:\n"
        "1. Responde SOLO sobre Abner, su portafolio, tecnología, química o sus proyectos.\n"
        "2. Sé breve (máximo 2-3 párrafos cortos).\n"
        "3. Usa formato Markdown básico."
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
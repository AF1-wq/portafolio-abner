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


def _normalize_chat_message(entry):
    if isinstance(entry, dict):
        role = str(entry.get("role", "user")).strip() or "user"
        if role == "assistant":
            role = "model"
        text = entry.get("content", entry.get("text", ""))
        return {"role": role, "parts": [{"text": str(text).strip()}]}
    return {"role": "user", "parts": [{"text": str(entry).strip()}]}


@app.post("/api/chat")
@limiter.limit("10 per minute")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    history = payload.get("history") or []

    if not message or len(message) > 500:
        return jsonify({"error": "El mensaje es obligatorio y debe tener máximo 500 caracteres"}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "Falta la clave GEMINI_API_KEY"}), 500

    try:
        contents = []
        if isinstance(history, list):
            contents.extend(_normalize_chat_message(entry) for entry in history)

        if not contents or contents[-1].get("role") != "user" or contents[-1].get("parts", [{}])[0].get("text") != message:
            contents.append(_normalize_chat_message({"role": "user", "content": message}))

        payload = {
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            "Eres el asistente profesional de Abner Franco: un perfil de desarrollador web "
                            "y creador de portafolio con enfoque en soluciones claras, seguras y orientadas al usuario."
                        )
                    }
                ]
            },
            "contents": contents,
        }

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates") or []
        first_candidate = candidates[0] if candidates else {}
        content = first_candidate.get("content") or {}
        parts = content.get("parts") or []
        reply = "".join(str(part.get("text", "")) for part in parts if isinstance(part, dict)).strip()

        if not reply:
            reply = "No fue posible generar una respuesta en este momento."

        return jsonify({"reply": reply}), 200
    except Exception as exc:
        app.logger.error("Error en /api/chat: %s", exc, exc_info=True)
        return jsonify({"error": "Error de comunicación con la IA"}), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )
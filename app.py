from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_folder=None)


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


if __name__ == "__main__":
    import os

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
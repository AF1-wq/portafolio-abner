#!/usr/bin/env python3
# coding: utf-8

"""
╔════════════════════════════════════════════════════════════════╗
║  Backend Flask - AbnerFranco.me                                ║
║  Sistema de Portafolio Estático                                ║
║  Sistema de Correos para Contacto                              ║
╚════════════════════════════════════════════════════════════════╝

SEGURIDAD:
    ✓ Credenciales desde .env (nunca exponer en frontend)
    ✓ Contraseña de Gmail desde .env
    ✓ Validación de entrada completa y robusta
    ✓ Frontend NUNCA tiene acceso a secrets
    ✓ Comunicación segura con Gmail SMTP
"""

import os
import logging
import smtplib
import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from flask_talisman import Talisman
from dotenv import load_dotenv
from datetime import datetime

# ============================================================================
# INICIALIZACIÓN
# ============================================================================

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)

# Directorio base estable del proyecto para servir archivos incluso con Gunicorn.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# SEGURIDAD Y RENDIMIENTO
# ============================================================================
 # Configurar CORS de forma segura (solo orígenes específicos en producción)
allowed_origins = [
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost:4242',  # Si usas otro puerto en desarrollo
    'https://abnerfranco.me',
    'https://www.abnerfranco.me'
]

CORS(app, origins=allowed_origins, supports_credentials=True)

# Compresión gzip automática para mejorar rendimiento
Compress(app)

# Headers de seguridad (HSTS, CSP, X-Frame-Options, etc.)
# Configuración flexible para desarrollo local con archivos estáticos
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com', 'https://fonts.gstatic.com'],
    'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com', 'https://fonts.gstatic.com'],
    'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
    'img-src': ["'self'", 'data:', 'https://images.unsplash.com', 'https://'],
    'connect-src': ["'self'"],
}

Talisman(
    app,
    force_https=False,  # TODO: Cambiar a True en producción con HTTPS
    strict_transport_security=False,  # TODO: Habilitar en producción
    content_security_policy=csp,
    feature_policy={
        'geolocation': "'none'",
        'microphone': "'none'",
        'camera': "'none'",
    }
)

# Rate Limiting para prevenir abuso
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # TODO: Usar Redis en producción para múltiples workers
)

# ============================================================================
# CARGAR CREDENCIALES DESDE .env
# ============================================================================

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Credenciales de Gmail para envío de correos
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Configurar clave secreta de Flask (para sesiones)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# ============================================================================
# VALIDACIÓN DE CREDENCIALES
# ============================================================================

# Validar credenciales de Gmail
MAIL_OK = False
if MAIL_USERNAME and MAIL_PASSWORD:
    logger.info("✅ Credenciales de Gmail cargadas desde .env")
    MAIL_OK = True
else:
    logger.warning("⚠️  Credenciales de Gmail no configuradas - Los correos no se enviarán")


# ============================================================================
# FUNCIONES UTILIDAD
# ============================================================================

def validate_email(email):
    """
    Validar formato básico de email.
    
    Args:
        email (str): Email a validar
    
    Returns:
        bool: True si es un email válido
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip()
    parts = email.split('@')
    
    if len(parts) != 2:
        return False
    
    local, domain = parts
    
    if not local or not domain or '.' not in domain:
        return False
    
    return True


# ============================================================================
# RUTAS / ENDPOINTS
# ============================================================================

# ============================================================================
# SERVIR ARCHIVOS ESTÁTICOS (HTML, CSS, JS, SVG)
# ============================================================================

@app.route('/')
def index():
    """Servir index.html"""
    try:
        return send_from_directory(BASE_DIR, 'index.html')
    except FileNotFoundError:
        return jsonify({'error': 'index.html no encontrado'}), 404


@app.route('/gracias')
def gracias():
    """Servir gracias.html (página de éxito)"""
    try:
        return send_from_directory(BASE_DIR, 'gracias.html')
    except FileNotFoundError:
        return jsonify({'error': 'gracias.html no encontrado'}), 404


@app.route('/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos (CSS, JS, SVG, etc) con caché optimizado"""
    try:
        # Extensiones permitidas
        allowed_extensions = {'.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.gif', '.woff', '.woff2', '.ttf', '.eot', '.html'}
        _, ext = os.path.splitext(filename)
        
        if ext.lower() not in allowed_extensions:
            return jsonify({'error': 'Tipo de archivo no permitido'}), 403
        
        # Enviar archivo con headers de cache optimizados
        response = make_response(send_from_directory(BASE_DIR, filename))
        
        # Cache por 1 año para assets inmutables (CSS, JS, fuentes, imágenes)
        if ext.lower() in {'.css', '.js', '.woff', '.woff2', '.ttf', '.eot', '.svg', '.png', '.jpg', '.jpeg', '.gif'}:
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        # Cache más corto para HTML (validar más frecuentemente)
        elif ext.lower() == '.html':
            response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutos
        
        return response
    except FileNotFoundError:
        return jsonify({'error': f'Archivo {filename} no encontrado'}), 404


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Verifica que el servidor está activo.
    
    Response (200):
    {
        "status": "ok",
        "service": "AbnerFranco.me - Portfolio Backend",
        "mail_configured": true,
        "timestamp": "2026-02-26T12:34:56.789..."
    }
    """
    return jsonify({
        'status': 'ok',
        'service': 'AbnerFranco.me - Portfolio Backend',
        'mail_configured': MAIL_OK,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/send-message', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo 5 mensajes por minuto por IP
def send_message():
    """
    Endpoint para el formulario de contacto con rate limiting y sanitización.
    Recibe name, email y message y envía un correo al propietario usando la configuración SMTP.
    """
    if not MAIL_OK:
        return jsonify({'error': 'Sistema de correos no configurado en el servidor'}), 503
        
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
            
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'JSON inválido'}), 400

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        if not name or not email or not message:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400
            
        if not validate_email(email):
            return jsonify({'error': 'Email inválido'}), 400

        # Validaciones simples de tamaño para evitar payloads abusivos.
        if len(name) > 120:
            return jsonify({'error': 'El nombre es demasiado largo'}), 400
        if len(email) > 254:
            return jsonify({'error': 'El email es demasiado largo'}), 400
        if len(message) > 5000:
            return jsonify({'error': 'El mensaje excede el límite permitido'}), 400
            
        # Sanitizar HTML para prevenir inyección (escape HTML entities)
        name_safe = html.escape(name)
        email_safe = html.escape(email)
        message_safe = html.escape(message)
            
        # Preparar el mensaje que recibirá el administrador
        asunto = f"Nuevo mensaje de tu Portafolio: {name_safe}"
        cuerpo = f"Tienes un nuevo mensaje de contacto.\n\n" \
                 f"📌 Nombre: {name_safe}\n" \
                 f"📧 Correo: {email_safe}\n\n" \
                 f"📝 Mensaje:\n{message_safe}\n"
        
        msg = MIMEMultipart()
        msg['From'] = MAIL_USERNAME
        msg['To'] = MAIL_USERNAME  # Recibes el correo en tu misma cuenta
        # Add Reply-To so the admin can easily reply to the user's email
        msg.add_header('reply-to', email)
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        
        logger.info(f"📧 Procesando mensaje de contacto de: {email}")
        
        # Conectar con timeout para prevenir cuelgues indefinidos
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as servidor:
            servidor.starttls()
            servidor.login(str(MAIL_USERNAME), str(MAIL_PASSWORD))
            servidor.send_message(msg)
            
        logger.info("✅ Mensaje de contacto enviado con éxito")
        
        return jsonify({'success': True, 'message': 'Mensaje enviado exitosamente'}), 200
        
    except smtplib.SMTPException as e:
        logger.error(f"❌ Error SMTP al mandar contacto: {str(e)}")
        return jsonify({'error': 'Error enviando el correo. Intenta de nuevo.'}), 500
    except Exception as e:
        logger.exception(f"❌ Error en send_message: {str(e)}")
        return jsonify({'error': 'Error interno procesando el mensaje'}), 500


# ============================================================================
# MANEJO DE ERRORES GLOBAL
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Endpoint no encontrado"""
    return jsonify({'error': 'Ruta no encontrada'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Método HTTP no permitido"""
    return jsonify({'error': 'Método HTTP no permitido'}), 405


@app.errorhandler(500)
def internal_error(error):
    """Error interno del servidor"""
    logger.error(f"❌ Error 500: {str(error)}")
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    port = 5000
    debug = FLASK_ENV == 'development'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🚀 SERVIDOR FLASK - AbnerFranco.me                       ║
    ║     Portafolio Estático + Sistema de Correos                 ║
    ║     SERVIDOR COMPLETO - TODO EN UN PUERTO 🚀                 ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🔐 SEGURIDAD:
       ✓ Credenciales de Gmail protegidas en .env
       ✓ MAIL_PASSWORD nunca expuesta en frontend
       ✓ Validación completa de entrada
       ✓ Comunicación segura con Gmail SMTP
    
    📍 SERVIDOR INTEGRADO:
       Host: 0.0.0.0
       Puerto: {port}
       URL: http://localhost:{port}
       Modo: {'DEBUG' if debug else 'PRODUCCIÓN'}
       Ambiente: {FLASK_ENV.upper()}
    
    🌍 RUTAS DISPONIBLES:
       GET  /                 →  Página principal (index.html)
       GET  /gracias          →  Página de confirmación (gracias.html)
       GET  /<archivo>        →  Archivos estáticos (CSS, JS, SVG)
       GET  /health           →  Health check
       POST /api/send-message →  Enviar mensaje de contacto
    
    📧 CORREOS:
       {'✅ HABILITADOS' if MAIL_OK else '❌ DESHABILITADOS - Credenciales no configuradas'}
       Usuario: {MAIL_USERNAME if MAIL_OK else 'N/A'}
    
    ✨ ACCESO INMEDIATO:
       Abre en tu navegador: http://localhost:{port}
       Todo está funcionando en UN SOLO PUERTO ⚡
    
    ⚠️  RECUERDA:
       • Nunca compartir archivo .env
       • Nunca subir .env a Git (está protegido por .gitignore)
    """)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )

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


PLANTILLA_COSMOS = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cosmos Email - 3D Edition</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500;600&display=swap');
    body { margin:0; padding:0; background:#02030a; }
</style>
</head>
<body style="margin:0;padding:0;background:#02030a;">

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#02030a;padding:0;">
    <tr>
        <td align="center" style="padding:52px 16px;">
            <table width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;">
                <tr>
                    <td style="padding:0;line-height:0;font-size:0; border-radius:20px 20px 0 0;overflow:hidden;">
                        <svg width="100%" viewBox="0 0 640 390" xmlns="http://www.w3.org/2000/svg" style="display:block;border-radius:20px 20px 0 0;">
                            <defs>
                                <radialGradient id="sp1" cx="22%" cy="58%" r="58%">
                                    <stop offset="0%" stop-color="#1e0845"/><stop offset="100%" stop-color="#02030a"/>
                                </radialGradient>
                                <radialGradient id="sp2" cx="82%" cy="28%" r="48%">
                                    <stop offset="0%" stop-color="#001830"/><stop offset="100%" stop-color="#02030a" stop-opacity="0"/>
                                </radialGradient>
                                <radialGradient id="nb_pur" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="#9333ea" stop-opacity="0.42"/>
                                    <stop offset="60%" stop-color="#7c3aed" stop-opacity="0.12"/>
                                    <stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/>
                                </radialGradient>
                                <radialGradient id="nb_cyn" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.30"/>
                                    <stop offset="100%" stop-color="#0ea5e9" stop-opacity="0"/>
                                </radialGradient>
                                <radialGradient id="nb_ros" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.18"/>
                                    <stop offset="100%" stop-color="#f43f5e" stop-opacity="0"/>
                                </radialGradient>
                                <radialGradient id="pl_body" cx="34%" cy="27%" r="66%">
                                    <stop offset="0%" stop-color="#c4b5fd"/>
                                    <stop offset="22%" stop-color="#7c3aed"/>
                                    <stop offset="58%" stop-color="#3b0764"/>
                                    <stop offset="100%" stop-color="#0a0018"/>
                                </radialGradient>
                                <radialGradient id="pl_atmo" cx="50%" cy="50%" r="50%">
                                    <stop offset="70%" stop-color="#7c3aed" stop-opacity="0"/>
                                    <stop offset="87%" stop-color="#a78bfa" stop-opacity="0.38"/>
                                    <stop offset="100%" stop-color="#ddd6fe" stop-opacity="0.65"/>
                                </radialGradient>
                                <radialGradient id="pl_shadow" cx="88%" cy="78%" r="56%">
                                    <stop offset="0%" stop-color="#000010" stop-opacity="0.88"/>
                                    <stop offset="100%" stop-color="#000010" stop-opacity="0"/>
                                </radialGradient>
                                <linearGradient id="ring_g" x1="0" y1="0" x2="1" y2="0">
                                    <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.04"/>
                                    <stop offset="18%" stop-color="#c4b5fd" stop-opacity="0.58"/>
                                    <stop offset="46%" stop-color="#ede9fe" stop-opacity="0.72"/>
                                    <stop offset="54%" stop-color="#ede9fe" stop-opacity="0.72"/>
                                    <stop offset="82%" stop-color="#c4b5fd" stop-opacity="0.58"/>
                                    <stop offset="100%" stop-color="#a78bfa" stop-opacity="0.04"/>
                                </linearGradient>
                                <linearGradient id="band_g" x1="0" y1="0" x2="1" y2="0">
                                    <stop offset="0%" stop-color="#6d28d9" stop-opacity="0.45"/>
                                    <stop offset="50%" stop-color="#8b5cf6" stop-opacity="0.15"/>
                                    <stop offset="100%" stop-color="#6d28d9" stop-opacity="0.45"/>
                                </linearGradient>
                                <linearGradient id="horiz" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="50%" stop-color="#02030a" stop-opacity="0"/>
                                    <stop offset="100%" stop-color="#0a0d1f" stop-opacity="1"/>
                                </linearGradient>
                                <filter id="gsoft">
                                    <feGaussianBlur stdDeviation="2.5" result="b"/>
                                    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
                                </filter>
                                <filter id="b4"><feGaussianBlur stdDeviation="4"/></filter>
                                <filter id="b10"><feGaussianBlur stdDeviation="10"/></filter>
                                <filter id="b18"><feGaussianBlur stdDeviation="18"/></filter>
                                <clipPath id="pcl"><circle cx="478" cy="150" r="90"/></clipPath>
                                <clipPath id="rfcl"><rect x="340" y="163" width="280" height="80"/></clipPath>
                            </defs>
                            <rect width="640" height="390" fill="#02030a"/>
                            <rect width="640" height="390" fill="url(#sp1)"/>
                            <rect width="640" height="390" fill="url(#sp2)"/>
                            <ellipse cx="150" cy="205" rx="250" ry="155" fill="url(#nb_pur)" filter="url(#b18)"/>
                            <ellipse cx="530" cy="118" rx="210" ry="115" fill="url(#nb_cyn)" filter="url(#b18)"/>
                            <ellipse cx="360" cy="310" rx="190" ry="95"  fill="url(#nb_ros)" filter="url(#b10)"/>
                            <ellipse cx="320" cy="188" rx="300" ry="14" fill="#7c3aed" fill-opacity="0.05" filter="url(#b10)" transform="rotate(-6 320 188)"/>
                            <circle cx="22"  cy="16"  r="0.6" fill="white" fill-opacity="0.45"/>
                            <circle cx="84"  cy="8"   r="0.8" fill="white" fill-opacity="0.55"/>
                            <circle cx="148" cy="30"  r="0.5" fill="white" fill-opacity="0.38"/>
                            <circle cx="212" cy="12"  r="0.7" fill="#e0d4ff" fill-opacity="0.50"/>
                            <circle cx="274" cy="22"  r="0.6" fill="white" fill-opacity="0.42"/>
                            <circle cx="336" cy="7"   r="0.9" fill="white" fill-opacity="0.60"/>
                            <circle cx="396" cy="28"  r="0.5" fill="#bfdbfe" fill-opacity="0.45"/>
                            <circle cx="444" cy="14"  r="0.7" fill="white" fill-opacity="0.52"/>
                            <circle cx="570" cy="22"  r="0.8" fill="#fde68a" fill-opacity="0.55"/>
                            <circle cx="620" cy="10"  r="0.6" fill="white" fill-opacity="0.42"/>
                            <circle cx="56"  cy="60"  r="0.7" fill="white" fill-opacity="0.50"/>
                            <circle cx="116" cy="46"  r="1.0" fill="#fde68a" fill-opacity="0.65"/>
                            <circle cx="178" cy="72"  r="0.6" fill="white" fill-opacity="0.50"/>
                            <circle cx="250" cy="53"  r="0.8" fill="white" fill-opacity="0.56"/>
                            <circle cx="306" cy="76"  r="0.5" fill="#e0d4ff" fill-opacity="0.50"/>
                            <circle cx="366" cy="46"  r="0.9" fill="white" fill-opacity="0.62"/>
                            <circle cx="558" cy="56"  r="0.7" fill="#bfdbfe" fill-opacity="0.57"/>
                            <circle cx="610" cy="70"  r="0.5" fill="white" fill-opacity="0.42"/>
                            <circle cx="34"  cy="108" r="0.6" fill="white" fill-opacity="0.35"/>
                            <circle cx="92"  cy="126" r="0.5" fill="white" fill-opacity="0.40"/>
                            <circle cx="160" cy="103" r="0.7" fill="#fde68a" fill-opacity="0.45"/>
                            <circle cx="238" cy="116" r="0.6" fill="white" fill-opacity="0.50"/>
                            <circle cx="288" cy="138" r="0.5" fill="white" fill-opacity="0.40"/>
                            <circle cx="350" cy="106" r="0.7" fill="#e0d4ff" fill-opacity="0.50"/>
                            <circle cx="626" cy="98"  r="0.6" fill="white" fill-opacity="0.45"/>
                            <ellipse cx="478" cy="180" rx="138" ry="23" fill="none" stroke="url(#ring_g)" stroke-width="12" transform="rotate(-9 478 180)" opacity="0.82"/>
                            <ellipse cx="478" cy="165" rx="92" ry="11" fill="#000018" fill-opacity="0.55" filter="url(#b4)" transform="rotate(-9 478 165)"/>
                            <circle cx="478" cy="150" r="108" fill="#7c3aed" fill-opacity="0.09" filter="url(#b18)"/>
                            <circle cx="478" cy="150" r="98"  fill="#a78bfa" fill-opacity="0.07" filter="url(#b4)"/>
                            <circle cx="478" cy="150" r="90"  fill="url(#pl_body)"/>
                            <g clip-path="url(#pcl)">
                                <ellipse cx="478" cy="130" rx="90" ry="11" fill="url(#band_g)"/>
                                <ellipse cx="478" cy="150" rx="90" ry="9"  fill="url(#band_g)" fill-opacity="0.70"/>
                                <ellipse cx="478" cy="170" rx="90" ry="11" fill="url(#band_g)" fill-opacity="0.50"/>
                                <ellipse cx="458" cy="140" rx="16" ry="11" fill="#6d28d9" fill-opacity="0.55" transform="rotate(-15 458 140)"/>
                                <ellipse cx="458" cy="140" rx="8"  ry="5" fill="#a78bfa" fill-opacity="0.45" transform="rotate(-15 458 140)"/>
                                <ellipse cx="458" cy="140" rx="3"  ry="2" fill="#ddd6fe" fill-opacity="0.40" transform="rotate(-15 458 140)"/>
                            </g>
                            <circle cx="478" cy="150" r="90" fill="url(#pl_atmo)"/>
                            <circle cx="478" cy="150" r="90" fill="url(#pl_shadow)"/>
                            <ellipse cx="446" cy="120" rx="24" ry="15" fill="white" fill-opacity="0.08" filter="url(#b4)" transform="rotate(-22 446 120)"/>
                            <ellipse cx="442" cy="116" rx="8" ry="5" fill="white" fill-opacity="0.12" transform="rotate(-22 442 116)"/>
                            <ellipse cx="478" cy="180" rx="138" ry="23" fill="none" stroke="url(#ring_g)" stroke-width="12" transform="rotate(-9 478 180)" clip-path="url(#rfcl)" opacity="0.92"/>
                            <circle cx="590" cy="50" r="2.6" fill="white" fill-opacity="0.95" filter="url(#gsoft)"/>
                            <line x1="590" y1="37" x2="590" y2="63" stroke="white" stroke-width="0.8" stroke-opacity="0.50"/>
                            <line x1="577" y1="50" x2="603" y2="50" stroke="white" stroke-width="0.8" stroke-opacity="0.50"/>
                            <line x1="583" y1="43" x2="597" y2="57" stroke="white" stroke-width="0.5" stroke-opacity="0.28"/>
                            <line x1="597" y1="43" x2="583" y2="57" stroke="white" stroke-width="0.5" stroke-opacity="0.28"/>
                            <circle cx="590" cy="50" r="10" fill="white" fill-opacity="0.04" filter="url(#b4)"/>
                            <circle cx="116" cy="46" r="2.2" fill="#fde68a" fill-opacity="0.92" filter="url(#gsoft)"/>
                            <circle cx="116" cy="46" r="7"   fill="#fde68a" fill-opacity="0.08" filter="url(#b4)"/>
                            <rect width="640" height="390" fill="url(#horiz)"/>
                              <text x="48" y="300" font-family="'Jost',Helvetica,sans-serif" font-size="9.5" font-weight="500" letter-spacing="4.5" fill="#a78bfa" fill-opacity="0.92">TRANSMISION ENTRANTE · ABNERFRANCO.ME</text>
                            <text x="46" y="350" font-family="'Cormorant Garamond',Georgia,serif" font-size="47" font-weight="300" fill="#f5f0ff" letter-spacing="-1.5">Nuevo Contacto</text>
                            <text x="48" y="382" font-family="'Cormorant Garamond',Georgia,serif" font-size="21" font-style="italic" font-weight="300" fill="#c4b5fd" fill-opacity="0.88">recibido desde el universo.</text>
                        </svg>
                    </td>
                </tr>
                <tr>
                    <td style="background:#0d1030; border-left:1px solid rgba(167,139,250,0.22); border-right:1px solid rgba(167,139,250,0.22); border-bottom:1px solid rgba(167,139,250,0.22); border-top:1px solid rgba(167,139,250,0.40); border-radius:0 0 20px 20px; overflow:hidden; padding:0;">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td style="padding:36px 36px 0;">
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                        <tr valign="top">
                                            <td width="47%" style="background:linear-gradient(145deg,rgba(255,255,255,0.07) 0%,rgba(255,255,255,0.02) 100%); border-top:1px solid rgba(255,255,255,0.20); border-left:1px solid rgba(255,255,255,0.15); border-bottom:1px solid rgba(0,0,0,0.50); border-right:1px solid rgba(0,0,0,0.30); border-radius:14px; padding:20px 22px;">
                                                <table cellpadding="0" cellspacing="0" border="0">
                                                    <tr><td style="font-family:'Jost',Helvetica,Arial,sans-serif; font-size:9px; font-weight:600; letter-spacing:3px; color:#8b9cc8; text-transform:uppercase; padding-bottom:8px;"><span style="color:#c084fc;">◈</span>&nbsp; Emisor</td></tr>
                                                    <tr><td style="font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif; font-size:23px; font-weight:400; color:#f0ebff; line-height:1.2;">[[NOMBRE_USUARIO]]</td></tr>
                                                </table>
                                            </td>
                                            <td width="6%">&nbsp;</td>
                                            <td width="47%" style="background:linear-gradient(145deg,rgba(6,182,212,0.06) 0%,rgba(255,255,255,0.02) 100%); border-top:1px solid rgba(103,232,249,0.28); border-left:1px solid rgba(103,232,249,0.18); border-bottom:1px solid rgba(0,0,0,0.50); border-right:1px solid rgba(0,0,0,0.30); border-radius:14px; padding:20px 22px;">
                                                <table cellpadding="0" cellspacing="0" border="0">
                                                    <tr><td style="font-family:'Jost',Helvetica,Arial,sans-serif; font-size:9px; font-weight:600; letter-spacing:3px; color:#8b9cc8; text-transform:uppercase; padding-bottom:8px;"><span style="color:#67e8f9;">◈</span>&nbsp; Coordenadas</td></tr>
                                                    <tr><td><a href="mailto:[[EMAIL_USUARIO]]" style="font-family:'Jost',Helvetica,Arial,sans-serif; font-size:13px; font-weight:400; color:#7dd3fc; text-decoration:none; word-break:break-all;">[[EMAIL_USUARIO]]</a></td></tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr><td style="padding:22px 36px 0; font-family:'Jost',Helvetica,Arial,sans-serif; font-size:9px; font-weight:600; letter-spacing:3.5px; color:#8b9cc8; text-transform:uppercase;">Contenido del mensaje</td></tr>
                        </table>
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td style="padding:14px 36px 32px;">
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                        <tr>
                                            <td style="background:#14082e; border-top:1px solid rgba(167,139,250,0.55); border-left:1px solid rgba(167,139,250,0.40); border-bottom:1px solid rgba(20,10,50,0.85); border-right:1px solid rgba(20,10,50,0.65); border-radius:16px; padding:28px 30px 32px;">
                                                <p style="margin:0 0 16px 0; font-family:'Jost',Helvetica,sans-serif; font-size:9px; letter-spacing:3px; color:#6d7fb8; text-transform:uppercase;">✦ señal decodificada</p>
                                                <p style="margin:0; font-family:'Cormorant Garamond',Georgia,serif; font-size:18px; font-weight:400; line-height:1.9; color:#ede8ff; letter-spacing:0.3px;">
                                                    [[MENSAJE_USUARIO]]
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
</html>
"""


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

        # Sanitizar HTML para prevenir inyeccion (escape HTML entities)
        name_safe = html.escape(name)
        email_safe = html.escape(email)
        message_safe = html.escape(message)

        # Convertir saltos de linea para mostrarlos correctamente en HTML.
        mensaje_html = message_safe.replace('\n', '<br>')

        # Preparar el mensaje HTML que recibira el administrador
        asunto = f"Nuevo mensaje de tu Portafolio: {name_safe}"
        html_final = PLANTILLA_COSMOS.replace('[[NOMBRE_USUARIO]]', name_safe).replace('[[EMAIL_USUARIO]]', email_safe).replace('[[MENSAJE_USUARIO]]', mensaje_html)

        msg = MIMEMultipart('alternative')
        msg['From'] = MAIL_USERNAME
        msg['To'] = MAIL_USERNAME  # Recibes el correo en tu misma cuenta
        # Add Reply-To so the admin can easily reply to the user's email
        msg.add_header('reply-to', email)
        msg['Subject'] = asunto
        msg.attach(MIMEText(html_final, 'html', 'utf-8'))
        
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

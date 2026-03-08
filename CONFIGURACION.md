# Configuración del Formulario de Contacto

## Problema Resuelto

El formulario de contacto tenía un error porque estaba configurado para usar Formspree (un servicio externo de terceros), pero la API key era inválida o el servicio estaba caído.

## Solución Implementada

Ahora el formulario usa el backend Flask propio del sitio (`/api/send-message`) que envía correos directamente mediante Gmail SMTP.

## Configuración Requerida

### 1. Crear el archivo `.env`

Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

### 2. Configurar Gmail para envío de correos

#### Opción A: Usar contraseña de aplicación (RECOMENDADO)

1. Ve a https://myaccount.google.com/security
2. Activa la verificación en dos pasos (si no está activa)
3. Busca "Contraseñas de aplicaciones"
4. Genera una nueva contraseña para "Correo"
5. Copia la contraseña generada (16 caracteres)

#### Opción B: Permitir aplicaciones menos seguras (NO RECOMENDADO)

Si no puedes usar contraseñas de aplicación:
1. Ve a https://myaccount.google.com/lesssecureapps
2. Activa "Permitir aplicaciones menos seguras"

### 3. Editar el archivo `.env`

```env
FLASK_ENV=production
FLASK_SECRET_KEY=cambia-esto-por-algo-muy-aleatorio-y-largo
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicación
```

### 4. Reiniciar el servidor

```bash
# Si usas gunicorn
gunicorn app:app

# Si usas Flask development server
python app.py
```

## Características de Seguridad

El sistema incluye:
- ✅ Rate limiting (5 mensajes por minuto por IP)
- ✅ Validación de campos (nombre, email, mensaje)
- ✅ Sanitización HTML para prevenir XSS
- ✅ Timeout de conexión SMTP (10 segundos)
- ✅ Headers de seguridad (CSP, HSTS, etc.)
- ✅ CORS configurado para dominios permitidos

## Troubleshooting

### Error: "Sistema de correos no configurado"

- Verifica que el archivo `.env` existe
- Verifica que `MAIL_USERNAME` y `MAIL_PASSWORD` están configurados
- Revisa los logs del servidor para más detalles

### Error: "Error enviando el correo"

- Verifica que la contraseña de aplicación es correcta
- Verifica que el email es una cuenta de Gmail válida
- Revisa si Gmail bloqueó el acceso (revisa tu email)

### Error: "Rate limit exceeded"

- Espera 1 minuto antes de volver a enviar
- El límite es 5 mensajes por minuto por IP

## Archivos Modificados

- `index.html`: Actualizado formulario y JavaScript
  - Campos cambiados de `nombre/mensaje` a `name/message`
  - Endpoint cambiado de Formspree a `/api/send-message`
- `.env.example`: Archivo de ejemplo para configuración
- `CONFIGURACION.md`: Esta documentación

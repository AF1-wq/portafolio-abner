# 🚀 Backend Flask - AbnerFranco.me

## Descripción
Backend completo para tu portafolio web con integración de:
- **Stripe** para procesamiento seguro de pagos
- **Flask-Mail** para envío de mensajes de contacto
- **Flask-CORS** para conexión segura con frontend

---

## 📋 Requisitos Previos

- **Python 3.8+** instalado
- **Pip** (gestor de paquetes de Python)
- Cuenta de **Stripe** (https://stripe.com)
- Cuenta de **Gmail** con autenticación de 2 factores habilitada

---

## 🔧 Instalación Paso a Paso

### 1️⃣ **Crear un entorno virtual**

```bash
# En Windows (PowerShell o CMD)
python -m venv venv

# Activar el entorno virtual
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ **Instalar dependencias**

```bash
pip install -r requirements.txt
```

### 3️⃣ **Configurar variables de entorno**

#### Opción A: Usar `.env`

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
# Usar tu editor favorito (VSCode, Notepad++, etc.)
```

#### Formato correcto del archivo `.env`:

```env
ENVIRONMENT=development
DOMAIN=http://localhost:5000

# Stripe Keys
STRIPE_SECRET_KEY=sk_test_51234567890abcdef...
STRIPE_PUBLISHABLE_KEY=pk_test_51234567890abcdef...

# Gmail
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=xyzw abcd efgh ijkl
MAIL_RECIPIENT=abnerfranco@gmail.com
```

---

## 🔑 Obtener las claves de Stripe

1. Ve a https://dashboard.stripe.com/apikeys
2. Copia la **Secret Key** (comienza con `sk_test_`)
3. Copia la **Publishable Key** (comienza con `pk_test_`)
4. Pégalas en tu archivo `.env`

---

## 📧 Configurar Gmail para envío de emails

### Paso 1: Habilitar autenticación de 2 factores
1. Ve a https://myaccount.google.com/security
2. Busca "Verificación en dos pasos" y actívalo

### Paso 2: Generar contraseña de aplicación
1. En https://myaccount.google.com/apppasswords
2. Selecciona: **Correo** → **Windows**
3. Google te generará una contraseña de 16 caracteres
4. Cópiala en `MAIL_PASSWORD` de tu `.env`

⚠️ **Nota**: USA LA CONTRASEÑA DE APLICACIÓN, NO TU CONTRASEÑA DE GOOGLE

---

## 🚀 Ejecutar el servidor

```bash
# Asegúrate de que el entorno virtual esté activado
python app.py
```

**Salida esperada:**
```
╔════════════════════════════════════════════════════════════╗
║         🚀 Servidor Flask - AbnerFranco.me                ║
╚════════════════════════════════════════════════════════════╝

📍 Ambiente: DEVELOPMENT
🔗 Dominio: http://localhost:5000
🔐 CORS habilitado para:
   - http://localhost:3000
   - http://localhost:5000
   - http://localhost:8000
   - https://abnerfranco.me
   - https://www.abnerfranco.me

Endpoints disponibles:
✓ GET /health
✓ POST /api/create-checkout-session
✓ POST /api/send-message
```

---

## ✅ Verificar que funciona

### 1. Health Check
```bash
curl http://localhost:5000/health
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "timestamp": "2025-02-26T10:30:45.123456",
  "environment": "development"
}
```

### 2. Probar endpoint de contacto
```bash
curl -X POST http://localhost:5000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "message": "Hola, me interesa tu portafolio"
  }'
```

---

## 📱 Conectar Frontend con Backend

Tu HTML ya está configurado para conectarse a los endpoints. Solo asegúrate de que:

1. **El servidor Flask esté corriendo** en `http://localhost:5000`
2. **Las variables de entorno estén configuradas**
3. **Abras tu `index.html` en un navegador**

Los botones de:
- ✦ **Enviar Mensaje** → POST `/api/send-message`
- **Proceder a Pago** → POST `/api/create-checkout-session`

---

## 🛡️ Seguridad en Producción

### Antes de hacer deployment:

1. **Actualiza `.env`** con modo producción:
```env
ENVIRONMENT=production
DOMAIN=https://abnerfranco.me
STRIPE_SECRET_KEY=sk_live_... # Clave LIVE de Stripe
```

2. **Cambia `debug=False`** en `app.py`

3. **Usa HTTPS** obligatoriamente

4. **Guarda `.env` en un servicio de secretos** (nunca lo subas a GitHub)

5. **Whitelist los dominios CORS** correctamente

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Asegúrate de haber activado el entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Luego instala nuevamente
pip install -r requirements.txt
```

### "Connection refused" en el frontend
- ✅ Verifica que `python app.py` esté corriendo
- ✅ Flask debe escuchar en `http://localhost:5000`
- ✅ Abre `http://localhost:5000/health` en el navegador

### "Error al enviar email"
- ✅ Verifica `MAIL_USERNAME` y `MAIL_PASSWORD` en `.env`
- ✅ Confirma que la contraseña sea de aplicación, no la de Google
- ✅ Revisa que 2FA esté habilitado en tu Google Account

### "Error con Stripe"
- ✅ Verifica que `STRIPE_SECRET_KEY` sea correcta
- ✅ Asegúrate de usar claves de `test`, no `live`
- ✅ Revisa que el JSON enviado sea válido

---

## 📚 API Reference

### POST `/api/send-message`
Envía un mensaje de contacto por email

**Request:**
```json
{
  "name": "Tu Nombre",
  "email": "tu@email.com",
  "message": "Tu mensaje aquí"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Mensaje enviado correctamente. Te responderé pronto."
}
```

---

### POST `/api/create-checkout-session`
Crea una sesión de pago con Stripe

**Request:**
```json
{
  "items": [
    {
      "name": "Producto 1",
      "price": 1500,
      "quantity": 1
    }
  ],
  "email": "cliente@ejemplo.com"
}
```

**Response (200):**
```json
{
  "session_id": "cs_test_...",
  "url": "https://checkout.stripe.com/pay/cs_test_..."
}
```

---

## 📞 Soporte

Si tienes problemas, revisa:
1. Los logs en la consola del servidor Flask
2. El `.env` tenga todos los valores correctos
3. Las credenciales de Stripe y Gmail sean válidas

---

**Creado con ❤️ por Abner Franco**  
*Última actualización: 26 de febrero de 2025*

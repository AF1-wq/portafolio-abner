# ⚡ INICIO RÁPIDO - Backend Flask

## 🏃 Instalación & Ejecución (5 minutos)

### Windows (PowerShell)

```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo .env (copiar .env.example)
copy .env.example .env

# 5. Editar .env con tus claves
# IMPORTANTE: Abre .env en VSCode y rellena:
# - STRIPE_SECRET_KEY
# - STRIPE_PUBLISHABLE_KEY  
# - MAIL_USERNAME
# - MAIL_PASSWORD
# - MAIL_RECIPIENT

# 6. Ejecutar servidor
python app.py
```

### macOS/Linux (Terminal)

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo .env
cp .env.example .env

# 5. Editar .env (usar nano, vim o tu editor)
nano .env

# 6. Ejecutar servidor
python app.py
```

---

## 🔑 Claves que necesitas

### 1. **STRIPE**
- Ve a: https://dashboard.stripe.com/apikeys
- Copia `Secret Key` (comienza con `sk_test_`)
- Copia `Publishable Key` (comienza con `pk_test_`)

### 2. **GMAIL**
- Ve a: https://myaccount.google.com/apppasswords
- Selecciona **Correo** → **Windows**
- Copia la contraseña de 16 caracteres
- Esta es tu `MAIL_PASSWORD`

---

## 📝 Archivo `.env` debe verse así:

```env
ENVIRONMENT=development
DOMAIN=http://localhost:5000

STRIPE_SECRET_KEY=sk_test_5123456789a...
STRIPE_PUBLISHABLE_KEY=pk_test_5123456789a...

MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=xyzw abcd efgh ijkl
MAIL_RECIPIENT=tu_email@gmail.com
```

---

## ✅ Verificar que funciona

Una vez ejecutando `python app.py`, deberías ver:

```
╔════════════════════════════════════════════════════════════╗
║         🚀 Servidor Flask - AbnerFranco.me                ║
╚════════════════════════════════════════════════════════════╝

📍 Ambiente: DEVELOPMENT
🔗 Dominio: http://localhost:5000
🔐 CORS habilitado...

Endpoints disponibles:
✓ GET /health
✓ POST /api/create-checkout-session
✓ POST /api/send-message
```

---

## 🧪 Probar los endpoints (en otra terminal)

### Health Check
```bash
curl http://localhost:5000/health
```

### Enviar mensaje (Postman o cURL)
```bash
curl -X POST http://localhost:5000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","message":"Mensaje de prueba"}'
```

---

## 📱 Abrir tu portafolio

1. Abre `index.html` en tu navegador
2. Prueba el botón **"Enviar Mensaje"**
3. Prueba añadir productos y **"Proceder a Pago"**

¡Listo! Todo debe funcionar correctamente 🎉

---

## ☠️ Problemas comunes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Activa el entorno virtual: `venv\Scripts\activate` |
| "Connection refused" | Asegúrate que `python app.py` está ejecutándose |
| Email no se envía | Verifica `MAIL_PASSWORD` es de aplicación, no contraseña Google |
| Error 400 en Stripe | Revisa que `STRIPE_SECRET_KEY` sea válida |

---

## 🚀 Siguiente paso: DEPLOYMENT

Ver `SETUP-FLASK.md` para instrucciones de producción (Heroku, Railway, etc.)

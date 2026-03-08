# ⚡ Comandos Rápidos - Referencia

## 🚀 Iniciar el Servidor (Primera Vez)

### Windows (PowerShell)
```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar archivo de configuración
copy .env.example .env

# 5. EDITAR .env con tus claves (IMPORTANTE!)
# Abre .env en VSCode y rellena:
# - STRIPE_SECRET_KEY
# - STRIPE_PUBLISHABLE_KEY
# - MAIL_USERNAME
# - MAIL_PASSWORD
# - MAIL_RECIPIENT

# 6. Ejecutar servidor
python app.py
```

## 🔄 Iniciar el Servidor (Próximas Veces)

### Windows 
```powershell
# Activar entorno (si no está activado)
venv\Scripts\activate

# Ejecutar
python app.py
```

### macOS/Linux
```bash
# Activar entorno
source venv/bin/activate

# Ejecutar
python app.py
```

---

## 🧪 Probar los Endpoints

### Opción 1: Usar script Python de prueba
```bash
# En otra terminal (con el servidor corriendo)
python test_api.py
```

### Opción 2: Usar cURL (Command Line)

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Enviar Mensaje:**
```bash
curl -X POST http://localhost:5000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","message":"Este es un mensaje de prueba"}'
```

**Crear Checkout:**
```bash
curl -X POST http://localhost:5000/api/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"items":[{"name":"Test","price":2999,"quantity":1}],"email":"test@test.com"}'
```

### Opción 3: Usar Postman
1. Descargar Postman: https://www.postman.com/downloads/
2. Nuevo Request
3. Seleccionar método: POST
4. URL: `http://localhost:5000/api/send-message`
5. Headers: `Content-Type: application/json`
6. Body (raw, JSON):
```json
{
  "name": "Juan Pérez",
  "email": "juan@email.com",
  "message": "Hola, me interesa tu portafolio"
}
```

---

## 📝 Editar el .env

### Abrir en VSCode
```bash
code .env
```

### Formato Correcto
```env
ENVIRONMENT=development
DOMAIN=http://localhost:5000
STRIPE_SECRET_KEY=sk_test_abc123...
STRIPE_PUBLISHABLE_KEY=pk_test_abc123...
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
MAIL_RECIPIENT=donde_destino@gmail.com
```

---

## 🔍 Errores Comunes

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Solución: Activar el entorno virtual
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # macOS/Linux

# Luego instalar
pip install -r requirements.txt
```

### "Connection refused" en frontend
```bash
# Solución: Asegurar que Flask esté corriendo
python app.py

# Abre en navegador:
# http://localhost:5000/health
```

### "No module named 'dotenv'"
```bash
# Solución: Reinstalar requirements
pip install python-dotenv
# o
pip install -r requirements.txt
```

### Email no se envía
```
Checklist:
□ MAIL_USERNAME es un email Gmail válido
□ MAIL_PASSWORD es de APLICACIÓN (no Google)
□ 2FA está habilitado en Google Account
□ Has generado contraseña en myaccount.google.com/apppasswords
□ El email receptor (MAIL_RECIPIENT) existe
```

### Stripe da error 400
```
Checklist:
□ STRIPE_SECRET_KEY es correcta
□ STRIPE_SECRET_KEY comienza con sk_test_ (o sk_live_ en producción)
□ Precios están en centavos (ej: 2999 para $29.99)
□ Cantidades son enteros positivos
```

---

## 📂 Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Servidor Flask (core del backend) |
| `.env` | Variables seguras (⚠️ NO SUBIR A GIT) |
| `.env.example` | Plantilla para crear .env |
| `requirements.txt` | Dependencias Python |
| `.gitignore` | Archivos a omitir en Git |
| `index.html` | Frontend (actualizado) |
| `test_api.py` | Script de pruebas automáticas |

---

## 🌐 URLs Importantes

| URL | Descripción |
|-----|-------------|
| `http://localhost:5000` | Base del servidor Flask |
| `http://localhost:5000/health` | Health check |
| `http://localhost:5000/api/send-message` | Enviar contacto |
| `http://localhost:5000/api/create-checkout` | Crear pago Stripe |
| `https://dashboard.stripe.com/apikeys` | Obtener claves Stripe |
| `https://myaccount.google.com/apppasswords` | Generar contraseña Gmail |
| `https://www.postman.com` | Cliente REST para testing |

---

## 🎯 Checklist: Antes de Usar

- [ ] Python 3.8+ instalado
- [ ] `venv` creado y activado
- [ ] `requirements.txt` instalado
- [ ] `.env` configurado con todas las claves
- [ ] `STRIPE_SECRET_KEY` válida (sk_test_...)
- [ ] `MAIL_PASSWORD` es de aplicación (16 caracteres)
- [ ] `MAIL_RECIPIENT` es un email válido
- [ ] `python app.py` ejecutándose sin errores
- [ ] `http://localhost:5000/health` devuelve 200

---

## 📱 Flujo Completo (Prueba Manual)

### 1. Iniciar servidor
```bash
python app.py
```

### 2. Abrir portafolio
```
Abre en navegador: file://C:\Users\abner\Downloads\MI-PORTAFOLIO\index.html
```

### 3. Probar contacto
- Llena formulario
- Click "Enviar Mensaje"
- Revisa inbox (debe llegar email)

### 4. Probar carrito
- Añade producto
- Click "Proceder a Pago"
- Serás redirigido a Stripe (usa tarjeta de prueba)

### 5. Tarjeta de prueba Stripe
```
Número: 4242 4242 4242 4242
Expiración: 12/25
CVC: 123
```

---

## 🚀 Pasos Siguientes

1. **Leer SETUP-FLASK.md** → Instrucciones detalladas
2. **Leer ARQUITECTURA.md** → Entender cómo funciona
3. **Ejecutar test_api.py** → Verificar que todo funciona
4. **Ir a QUICK-START.md** → Si necesitas empezar de cero

---

**Última actualización: 26 de febrero de 2025**

# 🚀 DEPLOYMENT - Guía de Deployment a Producción

## 📍 Opciones de Hosting

### 1. **Heroku** (Recomendado para beginners)
- Gratuito con limitaciones
- Muy fácil de usar
- Soporta Python

### 2. **Railway** (Recomendado)
- Gratis $5/mes
- Muy moderno
- Excelente para Flask

### 3. **PythonAnywhere**
- Hosting especializado en Python
- Plan gratuito disponible
- Soporte para Flask

### 4. **AWS/Google Cloud** (Avanzado)
- Más potente pero complejo
- Requiere configuración manual

---

## 🚀 OPCIÓN 1: Deployment con Railway (RECOMENDADO)

### Requisitos Previos
- Cuenta en https://railway.app
- Repositorio en GitHub
- Tu código completamente funcional en local

### Paso 1: Preparar tu Repositorio

1. **Inicializar Git** (si no lo has hecho)
```bash
cd C:\Users\abner\Downloads\MI-PORTAFOLIO
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
```

2. **Crear .gitignore correcto** (ya incluido)
```bash
git add .gitignore
```

3. **Agregar todos los archivos**
```bash
git add app.py requirements.txt .env.example *.html *.css *.js
git commit -m "Initial commit: Flask backend setup"
```

4. **Crear repositorio en GitHub**
- Ve a https://github.com/new
- Nombre: `mi-portafolio-backend`
- Descripción: "Backend Flask para AbnerFranco.me"
- Público
- Create repository

5. **Conectar con GitHub**
```bash
git branch -M main
git remote add origin https://github.com/TU_USERNAME/mi-portafolio-backend.git
git push -u origin main
```

### Paso 2: Conectar Railway con GitHub

1. Ve a https://railway.app
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway
5. Selecciona tu repositorio `mi-portafolio-backend`
6. Click "Deploy"

Railway automáticamente:
- ✅ Detecta que es Python
- ✅ Instala `requirements.txt`
- ✅ Ejecuta `python app.py`

### Paso 3: Configurar Variables de Entorno

1. En Railway dashboard, abre tu proyecto
2. Ve a la pestaña "Variables"
3. Añade todas tus variables (.env):
   ```
   ENVIRONMENT=production
   DOMAIN=https://tu-dominio.railway.app
   
   STRIPE_SECRET_KEY=sk_live_... (clave LIVE)
   STRIPE_PUBLISHABLE_KEY=pk_live_...
   
   MAIL_USERNAME=tu@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   MAIL_RECIPIENT=tu@gmail.com
   ```

### Paso 4: Obtener URL de Producción

1. En Railway, ve al proyecto
2. Abre "Deployments" > tu build actual
3. En la sección "Environment", copiar la URL (ej: `https://xxx-production.up.railway.app`)

### Paso 5: Actualizar tu Frontend

En `index.html`, cambiar la URL base para producción:

```javascript
// En la función checkout():
const API_BASE = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000'
  : 'https://xxx-production.up.railway.app';

const response = await fetch(API_BASE + '/api/create-checkout-session', ...);
```

O más simple, cambiar en cada fetch:

```javascript
// ANTES:
const response = await fetch('/api/send-message', ...)

// DESPUÉS:
const response = await fetch('https://tu-url-production.railway.app/api/send-message', ...)
```

### Paso 6: Conectar tu Dominio

1. En tu registrador de dominios (GoDaddy, Namecheap, etc.)
2. Vai a DNS settings
3. Crear un CNAME record:
   ```
   Host: @
   Points to: xxx-production.up.railway.app
   ```
4. O crear un A record (depende de tu hosting)

---

## 🚀 OPCIÓN 2: Deployment con Heroku

### Requisitos
- Cuenta en https://heroku.com
- Heroku CLI instalado
- Git configurado

### Paso 1: Instalar Heroku CLI

```bash
# Windows: Descargar desde https://devcenter.heroku.com/articles/heroku-cli

# macOS
brew install heroku/brew/heroku

# Verificar instalación
heroku --version
```

### Paso 2: Crear Procfile

En la raíz del proyecto, crear archivo `Procfile` (sin extensión):

```
web: gunicorn app:app
```

Instalar gunicorn:
```bash
pip install gunicorn
pip install -r requirements.txt > temp.txt
pip freeze >> requirements.txt
```

### Paso 3: Deployar

```bash
# Conectar con Heroku
heroku login

# Crear nueva app
heroku create mi-portafolio-backend

# Establecer variables de entorno
heroku config:set STRIPE_SECRET_KEY=sk_test_...
heroku config:set MAIL_PASSWORD=xxxx xxxx xxxx xxxx
# ... etcétera

# Deployar
git push heroku main

# Ver logs
heroku logs --tail
```

---

## 🚀 OPCIÓN 3: PythonAnywhere

### Paso Rápido

1. Ve a https://pythonanywhere.com
2. Sign Up (gratuito)
3. Upload files o conectar GitHub
4. Open web app
5. Configurar WSGI (agregar `app.py`)
6. Reload

Más info: https://help.pythonanywhere.com/pages/Flask/

---

## 🔗 Conectar tu Dominio abnerfranco.me

### Si comprasste el dominio en GoDaddy:

1. Ve a https://godaddy.com/domains
2. Selecciona `abnerfranco.me`
3. Abre "DNS"
4. Crear nuevo A record o CNAME:
   ```
   Type: CNAME
   Name: @
   Value: tu-app-produccion.railway.app
   ```

### Si lo compraste en Namecheap:

1. Ve al panel de control
2. Domain List > selected domain > Manage
3. Advanced DNS
4. Crear:
   ```
   Type: CNAME Record
   Host: @
   Value: tu-app-produccion.railway.app
   ```

Esperar 5-30 minutos para que se propague DNS

---

## 🔒 Cambiar a Modo Producción

### Paso 1: Actualizar .env

En Railway/Heroku dashboard:

```
ENVIRONMENT=production
DOMAIN=https://abnerfranco.me

# Usar claves LIVE de Stripe (no test)
STRIPE_SECRET_KEY=sk_live_123...
STRIPE_PUBLISHABLE_KEY=pk_live_123...

# Resto igual
MAIL_USERNAME=tu@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
MAIL_RECIPIENT=tu@gmail.com
```

### Paso 2: Actualizar app.py

```python
# En la sección de punto de entrada (final del file)
if __name__ == '__main__':
    debug_mode = ENVIRONMENT == 'development'
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug_mode,        # Será False en producción
        use_reloader=debug_mode
    )
```

### Paso 3: Actualizar Frontend

En `index.html`, todos los fetch deben apuntar al dominio:

```javascript
// ✅ CORRECTO para producción
const API_URL = 'https://abnerfranco.me/api/send-message';

// O mejor aún, usar ruta relativa:
fetch('/api/send-message', ...)  // Funciona en localhost y producción
```

### Paso 4: Configurar CORS

En `app.py`, asegurar que se permite tu dominio:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://abnerfranco.me",
            "https://www.abnerfranco.me"
        ],
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## ✅ Verificar que está en Producción

### Checklist:

1. **¿Dominio apunta a app?**
   ```bash
   curl https://abnerfranco.me/health
   ```
   Debe devolver JSON

2. **¿Email funciona?**
   - Envía un contacto desde tu dominio
   - Revisa que llega al inbox

3. **¿Stripe funciona?**
   - Añade producto al carrito
   - Click pago
   - Debe redirigir a Stripe (usar tarjeta test)

4. **¿HTTPS funciona?**
   - Abre en navegador: https://abnerfranco.me
   - Debe mostrar candado 🔒 verde

5. **¿Redireccionamientos post-pago?**
   - Éxito → success.html
   - Cancelar → index.html

---

## 🚨 Problemas Comunes en Producción

### "Disallowed Host"
```python
# En app.py, agregar:
app.config['SERVER_NAME'] = 'abnerfranco.me'
```

### "SSL Certificate Error"
- Railway/Heroku incluyen SSL automáticamente
- Si usas otro hosting, usa Let's Encrypt
- Certbot: https://certbot.eff.org/

### "CORS Error en Producción"
- Verifica que el frontend esté en dominio permitido
- Revisa valores de `origins` en CORS

---

## 📊 Monitoreo en Producción

### Heroku
```bash
# Ver logs
heroku logs --tail

# Ver variables
heroku config
```

### Railway
- Dashboard > Deployments
- Pestaña "Logs" para errores en vivo

### Ambos
Configura alertas para:
- Errores HTTP 5xx
- Crasheos de aplicación
- Límite de bandwidth

---

## 🔄 Actualizar Código en Producción

### Con Git Push (Railway/Heroku):
```bash
# Hacer cambios locales
# Commit
git add .
git commit -m "Fix: mensaje descriptivo"

# Push (se redeploy automáticamente)
git push origin main
git push heroku main  # si usas Heroku
```

### Manual:
1. Hacer cambios locales
2. Probar con `python app.py`
3. Subir archivos a hosting (dashboard)
4. Reiniciar aplicación

---

## 📈 Mejoras para Producción

- [ ] Configurar HTTPS (Let's Encrypt)
- [ ] Agregar logging detallado
- [ ] Configurar rate limiting
- [ ] Backups de bases de datos
- [ ] Monitoreo de errores (Sentry)
- [ ] CDN para contenido estático
- [ ] Caché de respuestas
- [ ] Compresión GZIP

---

## 🎓 Próximos Pasos

1. **Deployar primero en desarrollo** → Probar todo localmente
2. **Deployar en staging** → Ambiente similar a producción
3. **Deployar en producción** → Dominio final

**Siempre**: Backup antes de cambios importantes

---

**Última actualización: 26 de febrero de 2025**

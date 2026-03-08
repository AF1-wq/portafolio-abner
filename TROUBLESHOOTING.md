# 🔧 Troubleshooting - Solución de Problemas

## 🚨 Problemas Comunes y Soluciones

---

## 1. **Python no está instalado**

### Síntoma
```
'python' is not recognized as an internal or external command
```

### Solución
1. Descargar Python desde https://www.python.org/downloads/
2. **IMPORTANTE**: Marcar ✓ "Add Python to PATH" durante instalación
3. Reiniciar el terminal
4. Verificar:
```bash
python --version
```

---

## 2. **Entorno virtual no se crea**

### Síntoma
```
Error creating virtual environment
```

### Solución
```bash
# Windows - Asegúrate de estar en la carpeta correcta
cd C:\Users\abner\Downloads\MI-PORTAFOLIO

# Eliminar venv anterior si existe
rmdir /s venv

# Crear nuevo
python -m venv venv

# Activar
venv\Scripts\activate

# Verificar (debe aparecer (venv) en el prompt)
# (venv) C:\Users\abner\Downloads\MI-PORTAFOLIO>
```

---

## 3. **Error: "ModuleNotFoundError: No module named 'flask'"**

### Síntoma
```
Traceback (most recent call last):
  File "app.py", line 8, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'
```

### Cause
El entorno virtual no está activado O las dependencias no están instaladas

### Solución

**Opción A: Activar entorno**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Debe mostrar: (venv) en el prompt
```

**Opción B: Reinstalar dependencias**
```bash
# Asegúrate de haber activado el entorno
venv\Scripts\activate

# Luego
pip install -r requirements.txt

# Verificar que Flask está instalado
pip list | grep Flask
```

**Opción C: Instalación manual**
```bash
venv\Scripts\activate
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install Flask-Mail==0.9.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0
```

---

## 4. **Error: "No module named 'dotenv'"**

### Síntoma
```
ModuleNotFoundError: No module named 'dotenv'
```

### Solución
```bash
# Activar entorno
venv\Scripts\activate

# Instalar específicamente dotenv
pip install python-dotenv

# Reiniciar el servidor
python app.py
```

---

## 5. **Variables de entorno no se cargan (.env no funciona)**

### Síntoma
```
Error: WOMPI_APP_ID not found
```

### Solución

**Paso 1: Verificar que el archivo existe**
```bash
# Windows
dir .env

# macOS/Linux
ls -la .env
```

**Paso 2: Verificar contenido del archivo**
```bash
# Windows
type .env

# macOS/Linux
cat .env
```

**Paso 3: Asegúrate que no hay espacios extra**
```env
# ❌ INCORRECTO (espacios extra)
WOMPI_APP_ID = 3af3c5b4-ceac-4b67-b435-5ff606e12e5d

# ✅ CORRECTO (sin espacios alrededor de =)
WOMPI_APP_ID=3af3c5b4-ceac-4b67-b435-5ff606e12e5d
```

**Paso 4: Reiniciar el servidor**
```bash
# Presiona Ctrl+C para detener el servidor
# Luego
python app.py
```

---

## 6. **Error: "Connection refused" en el frontend**

### Síntoma
En el navegador, al hacer click en "Enviar Mensaje" o "Proceder a Pago":
```
Failed to fetch
Error: Connection refused
```

### Causa
El servidor Flask no está corriendo

### Solución
```bash
# Abre una NUEVA terminal
# Asegúrate de estar en la carpeta correcta
cd C:\Users\abner\Downloads\MI-PORTAFOLIO

# Activar entorno
venv\Scripts\activate

# Ejecutar servidor
python app.py

# Deberías ver:
# ╔════════════════════════════════════════════════════════════╗
# ║         🚀 Servidor Flask - AbnerFranco.me                ║
# ╚════════════════════════════════════════════════════════════╝
```

**Verificar que está corriendo:**
```bash
# En otra terminal
curl http://localhost:5000/health
```

---

## 7. **Error 400: "Content-Type must be application/json"**

### Síntoma
```json
{
  "error": "Content-Type debe ser application/json"
}
```

### Causa
El request no incluye el header correcto

### Solución
Esto ya está configurado en `index.html`, pero verifica:

```javascript
// ✅ CORRECTO
fetch('/api/send-message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },  // ← IMPORTANTE
  body: JSON.stringify({ name, email, message })
});
```

---

## 8. **Error al enviar email: "Authentication failed"**

### Síntoma
```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and password not accepted')
```

### Causa
Credenciales Gmail incorrectas

### Solución

**Paso 1: Verificar que 2FA está habilitado**
1. Ve a https://myaccount.google.com/security
2. Busca "Verificación en dos pasos"
3. Si está OFF, actívalo
4. Espera 5 minutos

**Paso 2: Generar contraseña de aplicación**
1. Ve a https://myaccount.google.com/apppasswords
2. Selecciona: **Correo** → **Windows**
3. Google te le dará una contraseña de 16 caracteres
4. Cópiala a tu `.env` en `MAIL_PASSWORD` (sin espacios extra)

**Paso 3: Verificar formato en .env**
```env
# ❌ INCORRECTO (con espacios del medio)
MAIL_PASSWORD=xxxx xxxx xxxx xxxx

# ✅ CORRECTO (copia exactamente como da Google)
MAIL_PASSWORD=xyzwabcdefghijkl
```

**Paso 4: Reiniciar servidor**
```bash
# Ctrl+C para detener
python app.py
```

**⚠️ IMPORTANTE**
- NO uses tu contraseña regular de Google
- SIEMPRE usa la contraseña de aplicación (16 caracteres)
- Si no te deja generar, asegúrate que 2FA está ON

---

## 9. **Error 400: "Cada item debe tener: name, price, quantity"**

### Síntoma
```json
{
  "error": "Each item must have: name, price, quantity"
}
```

### Causa
Los datos del carrito no están en el formato correcto

### Solución
Verificar que en `index.html`, la función `checkout()` convierte correctamente:

```javascript
// ✅ CORRECTO
const items = cart.map(item => ({
  name: item.name,
  price: Math.round(item.price * 100), // IMPORTANTE: en centavos
  quantity: item.qty                    // debe ser cantidad
}));
```

---

## 11. **Error CORS: "Access to fetch blocked by CORS policy"**

### Síntoma
```
Access to fetch at 'http://localhost:5000/api/send-message' 
from origin 'file://' has been blocked by CORS policy
```

### Causa
Abrir `index.html` como archivo local (`file://`) no funciona con CORS

### Solución

**Opción A: Usar servidor HTTP simple**
```bash
# Python 3
python -m http.server 8000

# Luego abrir en navegador:
# http://localhost:8000/index.html
```

**Opción B: Usar Live Server en VSCode**
1. Instalar extensión "Live Server"
2. Click derecho en `index.html` → "Open with Live Server"
3. Automáticamente abre en `http://localhost:5500`

**Opción C: Desactivar CORS en desarrollo (NO recomendado)**
```python
# ⚠️ SOLO PARA DESARROLLO
from flask_cors import CORS
CORS(app)  # Permite TODOS los orígenes
```

---

## 12. **Puerto 5000 ya está en uso**

### Síntoma
```
Address already in use: ('0.0.0.0', 5000)
```

### Causa
Otra aplicación usa el puerto 5000

### Solución

**Opción A: Matar proceso en Windows**
```powershell
# Encontrar qué usa puerto 5000
netstat -ano | findstr :5000

# Matar el proceso (reemplazar PID con el número)
taskkill /PID <PID> /F

# Luego ejecutar Flask
python app.py
```

**Opción B: Cambiar puerto en Flask**
```python
# En app.py, cambiar último línea:
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,  # ← Cambiar a 5001 o cualquier otro puerto
        debug=debug_mode
    )
```

**Opción C: Usar puerto diferente en index.html**
```javascript
// Cambiar URL base
const API_URL = 'http://localhost:5001';  // Nuevo puerto
```

---

## 13. **Archivo .env aparece en GitHub**

### Síntoma
Cuando subes a GitHub, ves que `.env` está en los commits (MALO)

### Solución

**Paso 1: Remover el archivo del historio de Git**
```bash
# Remover del historial (no elimina el archivo local)
git rm --cached .env

# Hacer commit
git commit -m "Remove .env from history"

# Push
git push
```

**Paso 2: Asegurar que .gitignore protege**
```bash
# Verificar que .gitignore tiene:
cat .gitignore | grep "^.env"

# Si no lo tiene, agregar al inicio de .gitignore:
echo .env >> .gitignore
```

**Paso 3: Commit .gitignore
```bash
git add .gitignore
git commit -m "Update .gitignore to protect .env"
git push
```

---

## 14. **Las funciones fetch no existen**

### Síntoma
```
ReferenceError: handleContactSubmit is not defined
ReferenceError: checkout is not defined
```

### Causa
Las funciones no están definidas en el HTML o script.js

### Solución
Verificar que en `index.html`, dentro del último `<script>`, existan:

```javascript
// Debe existir en HTML
function handleContactSubmit(event) { ... }
async function checkout() { ... }
```

Si no existen, cópialas de `script.js` o del archivo actualizado que te proporcioné.

---

## 15. **SSL/HTTPS error en producción**

### Síntoma
```
SSL_ERROR_HANDSHAKE_FAILURE_ALERT
```

### Causa
No tienes certificado SSL en tu dominio

### Solución
1. Usar Let's Encrypt (gratis)
2. O usar un servicio de hosting que incluya SSL (Heroku, Railway, etc.)
3. Para desarrollo local, usar siempre `http://` (sin SSL)

---

## 🆘 Si aún tienes problemas

### Checklist de debugging:

1. ¿El servidor Flask está corriendo?
   ```bash
   curl http://localhost:5000/health
   ```

2. ¿Está activado el entorno virtual?
   ```bash
   # Debe mostrar: (venv) al inicio
   ```

3. ¿El .env está configurado?
   ```bash
   cat .env  # Verifica que tenga valores, no vacío
   ```

4. ¿Los requisitos están instalados?
   ```bash
   pip list | grep Flask
   pip list | grep requests
   pip list | grep dotenv
   ```

5. ¿Hay errores en la consola?
   ```bash
   # Ejecuta con verbose
   python -u app.py
   ```

---

## 📞 Recursos útiles

- **Documentación Flask**: https://flask.palletsprojects.com/
- **Documentación Wompi**: https://docs.wompi.sv/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/flask
- **Flask-Mail**: https://pythonhosted.org/Flask-Mail/

---

**Última actualización: 26 de febrero de 2025**

¡Hola! Bienvenido a tu nuevo backend Flask profesional. 

Soy Abner Franco. Este es el stack full-stack para mi portafolio abnerfranco.me

---

# 🎯 COMIENZA AQUÍ

## ¿Qué necesito hacer?

### Opción A: Solo Publicar (sin backend)
Si solo quieres que tu portafolio esté en internet:
```
Abre index.html directamente en tu navegador
```
✅ El portafolio funciona sin instalar nada

---

### Opción B: Pagos + Emails (Recomendado)
Si quieres que funcionen realmente pagos con Stripe y emails:

**Paso 1:** Abre [`QUICK-START.md`](QUICK-START.md)  
**Paso 2:** Sigue las 5 instrucciones  
**Paso 3:** Listo! ✅

Tiempo: ~5 minutos

---

## 📚 ¿Qué hay en esta carpeta?

### 🐍 Backend (Python Flask)
```
app.py                 ← Tu servidor Flask
.env.example           ← Plantilla de configuración
requirements.txt       ← Dependencias Python
test_api.py           ← Script de pruebas
```

### 🌐 Frontend (HTML/CSS/JS)
```
index.html            ← Tu portafolio (ACTUALIZADO)
style.css             ← Estilos
script.js             ← JavaScript actualizado
```

### 📖 Documentación
```
RESUMEN-COMPLETO.md   ← Guía completa del proyecto
QUICK-START.md        ← 5 pasos rápidos
SETUP-FLASK.md        ← Instrucciones detalladas
ARQUITECTURA.md       ← Cómo funciona todo
TROUBLESHOOTING.md    ← Solución de problemas
DEPLOYMENT.md         ← Cómo deployar a producción
COMANDOS-RAPIDOS.md   ← Referencia de comandos
```

---

## ✨ ¿Qué nuevo traigo?

### Endpoint 1: Envío de Emails 📧
```javascript
// Cuando usuario llena formulario de contacto
// Automáticamente se envía email a tu inbox
```

### Endpoint 2: Pagos con Stripe 💳
```javascript
// Cuando usuario añade productos y paga
// Stripe procesa el pago automáticamente
```

### Endpoint 3: Health Check ✅
```bash
// Para verificar que el servidor está activo
curl http://localhost:5000/health
```

---

## 🏃 ¡HAZLO AHORA! (5 minutos)

### Paso 1: Instala Python (si no lo tienes)
Descargalo desde: https://python.org/downloads/

### Paso 2: Copia este para la terminal
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 3: Copia el archivo de configuración
```powershell
copy .env.example .env
```

### Paso 4: Edita .env
Abre `.env` en VSCode y rellena:
- STRIPE_SECRET_KEY (de https://dashboard.stripe.com)
- MAIL_PASSWORD (de https://myaccount.google.com/apppasswords)
- Otros campos...

### Paso 5: Ejecuta el servidor
```powershell
python app.py
```

¡Listo! Tu servidor está corriendo en http://localhost:5000

---

## 📖 ¿Necesito ayuda?

### Soy principiante
→ Lee: **QUICK-START.md**

### No entiendo cómo funciona
→ Lee: **ARQUITECTURA.md**

### Algo no funciona
→ Busca en: **TROUBLESHOOTING.md**  
→ Ejecuta: `python test_api.py`

### Quiero llevarlo a internet
→ Lee: **DEPLOYMENT.md**

---

## 🎯 Timeline Sugerido

| Día | Actividad | Tiempo |
|-----|-----------|--------|
| Hoy | Setup local | 30 min |
| Hoy | Probar endpoints | 15 min |
| Mañana | Entender arquitectura | 30 min |
| Mañana | Customizar código | 1 hora |
| Próximo | Deployar a producción | 1 hora |

---

## 💡 Recuerda

✅ **TODA la documentación está en Español**  
✅ **El código está comentado y explicado**  
✅ **Hay ejemplos de cómo usar cada endpoint**  
✅ **Las claves están protegidas en .env**  
✅ **Todo es gratis (Stripe test, Gmail, hosting)**  

---

## 🚀 ¡COMIENZA AQUÍ!

### Opción 1: Setup rápido
→ Abre [`QUICK-START.md`](QUICK-START.md)

### Opción 2: Entender primero
→ Lee [`RESUMEN-COMPLETO.md`](RESUMEN-COMPLETO.md)

### Opción 3: Instalar paso a paso
→ Sigue [`SETUP-FLASK.md`](SETUP-FLASK.md)

---

## 📋 Checklist: ¿Estoy listo?

- [ ] Python 3.8+ instalado
- [ ] He leído QUICK-START.md
- [ ] He copiado .env.example a .env
- [ ] He obtenido mis claves (Stripe + Gmail)
- [ ] He ejecutado pip install -r requirements.txt
- [ ] He ejecutado python app.py
- [ ] El servidor está corriendo sin errores

Si marcaste todos: **¡FELICITACIONES!** 🎉  
Tu backend está listo. Ahora a probar!

---

## 🤔 Preguntas Frecuentes

**¿Necesito Node.js?**  
No. Usamos Python + Flask. Node.js es opcional.

**¿Es gratis?**  
Sí, 100% gratis. Python, Flask, Stripe (test), Gmail, todo es gratis.

**¿Es seguro?**  
Sí. Tus claves están en .env (no se suben a Git). Validamos todos los datos. Usamos CORS.

**¿Funciona en Windows/Mac/Linux?**  
Sí, Python funciona en todos.

**¿Puedo cambiar los mensajes de error?**  
Claro, todo es personalizable en app.py

---

## 🎓 Lo que aprendiste

- Backend REST con Flask
- Integración con API externas (Stripe)
- Sistema de emails SMTP (Gmail)
- Validación y seguridad
- Variables de entorno
- Frontend <> Backend communication

Este es un proyecto **profesional y valioso** para tu portafolio.

---

## ¡Siguiente Paso!

### 👉 Abre ahora: [`QUICK-START.md`](QUICK-START.md)

---

**Creado con ❤️ para AbnerFranco.me**  
*Versión: 1.0 - Febrero 26, 2025*

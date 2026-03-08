# 🚀 MI PORTAFOLIO - AbnerF

## 🎯 NUEVA ACTUALIZACIÓN: Backend Flask ✨

Tu portafolio ahora tiene un **backend profesional** con:
- ✅ **Pagos reales con Stripe**
- ✅ **Emails de contacto vía Gmail**  
- ✅ **API REST con Flask (Python)**
- ✅ **Seguridad con variables de entorno**

### 📖 **Empezar con Backend Flask:**

👉 **Lee primero:** [`RESUMEN-COMPLETO.md`](RESUMEN-COMPLETO.md)  
👉 **Instalación rápida:** [`QUICK-START.md`](QUICK-START.md)  
👉 **Problemas?:** [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)  

---

## ⚡ INICIO INMEDIATO (Sin instalar nada)

### 🎯 USA AHORA MISMO:

**Haz doble clic en cualquiera de estos archivos:**
- [`portfolio.html`](portfolio.html) ← Recomendado ⭐
- [`index.html`](index.html) ← Tambén funciona

**¡Ya está! Todo funciona en modo demo** ✅

---

## 📋 ¿Qué funciona sin Node.js?

✅ **Navegación completa** - Todas las secciones  
✅ **Sección Hogar** - Hero, estadísticas, animaciones  
✅ **Sección Quién Soy** - Habilidades, skills, tags  
✅ **Galería** - Feed de proyectos, subir imágenes  
✅ **Tienda** - 6 productos, carrito funcional  
✅ **Checkout** - Simulación de compra (modo demo)  

---

## 💳 ¿Necesitas Pagos Reales con Stripe?

Solo entonces necesitas instalar Node.js.

### 📖 Guía completa de instalación:
👉 **Lee:** [`INSTALAR-NODEJS.md`](INSTALAR-NODEJS.md)

### 🚀 Resumen rápido:

```powershell
# 1. Instalar Node.js desde https://nodejs.org/
# 2. REINICIAR tu computadora
# 3. Abrir VS Code de nuevo
# 4. Ejecutar:

npm install          # Instalar dependencias
npm start           # Iniciar servidor
# Abrir: http://localhost:4242
```

---

## 🔧 Scripts de Ayuda

### Verificar si Node.js está instalado:

**Windows:**
```cmd
verificar-nodejs.bat
```

**PowerShell:**
```powershell
.\verificar-nodejs.ps1
```

Estos scripts:
- ✅ Verifican Node.js y npm
- ✅ Instalan dependencias automáticamente
- ✅ Te dicen qué hacer si falta algo

---

## 📂 ARCHIVOS DEL PROYECTO

```
MI-PORTAFOLIO/
│
├── 🌐 ARCHIVOS PRINCIPALES (úsalos directamente)
│   ├── index.html         ← Abre este (redirige a portfolio.html)
│   ├── portfolio.html     ← O abre este directamente
│   └── success.html       ← Página de confirmación de pago
│
├── 🖥️ SERVIDOR (solo para pagos reales)
│   ├── server.js          ← Servidor Express + Stripe
│   ├── package.json       ← Dependencias Node.js
│   └── .env              ← Configuración (claves Stripe)
│
└── 📄 OTROS
    ├── README.md          ← Esta guía
    └── .gitignore         ← Archivos a ignorar en Git
```

---

## 🎨 CARACTERÍSTICAS

### ✅ Funciona SIN servidor:
- 🏠 Sección "Hogar" con estadísticas
- 👤 Sección "Quién Soy" con habilidades
- 📸 Galería interactiva con subida de imágenes
- 🛒 Tienda con carrito de compras
- 💰 Simulación de pagos (demo)

### ✅ Funciona CON servidor:
- Todo lo anterior +
- 💳 Pagos reales con Stripe Checkout
- 🔐 Validación de precios en servidor
- 📧 Webhooks para confirmación de pagos

---

## 🔧 MODO DETECCIÓN AUTOMÁTICA

El portafolio detecta automáticamente si estás usando servidor:

| Modo | Cómo se abre | Pagos |
|------|--------------|-------|
| **Demo** | Doble clic en HTML | Simulados |
| **Producción** | http://localhost:4242 | Reales (Stripe) |

---

## ❓ PROBLEMAS COMUNES

### No veo nada al abrir el HTML
- Asegúrate de que el navegador no bloquee archivos locales
- Prueba con otro navegador (Chrome, Firefox, Edge)

### El carrito no funciona
- Verifica que JavaScript esté habilitado
- Abre la consola del navegador (F12) para ver errores

### Error: "Cannot find module 'express'"
- Necesitas instalar dependencias: `npm install`
- Solo necesario si quieres usar el servidor

### El servidor no inicia
- Verifica que Node.js esté instalado: `node --version`
- Verifica que el puerto 4242 no esté ocupado

---

## 🚀 COMANDOS ÚTILES (Solo con servidor)

```powershell
# Instalar dependencias
npm install

# Iniciar servidor
npm start

# Verificar versión de Node.js
node --version

# Verificar versión de npm
npm --version
```

---

## 💡 RECOMENDACIÓN

**Para ver el portafolio rápidamente:**
👉 Simplemente abre `portfolio.html` con doble clic

**Para probar pagos reales:**
👉 Sigue las instrucciones de "OPCIÓN 2"

---

## 📞 SOPORTE

El proyecto está configurado para funcionar de forma standalone. Si encuentras problemas:

1. Verifica que abriste correctamente el archivo HTML
2. Revisa la consola del navegador (F12) para errores
3. Para pagos reales, asegúrate de tener Node.js y Stripe configurados

---

## ✨ ESTADO

✅ **FUNCIONANDO AL 100%**

- ✅ Modo Demo: Listo (sin instalación)
- ✅ Modo Servidor: Listo (requiere Node.js)
- ✅ Todas las secciones funcionando
- ✅ Carrito de compras operativo
- ✅ Checkout con detección automática

---

**Última actualización:** 14 de febrero de 2026  
**Desarrollado por:** AbnerF


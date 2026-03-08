# 🏗️ Arquitectura del Stack Full-Stack (Flask + Vanilla JS)

## 📊 Diagrama General

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENTE (Frontend)                      │
│                   index.html + CSS + JS                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  Formulario      │         │  Carrito de      │          │
│  │  de Contacto     │         │  Compras         │          │
│  └────────┬─────────┘         └────────┬─────────┘          │
│           │                            │                    │
│           │ fetch() POST               │ fetch() POST       │
│           │ /api/send-message          │ /api/checkout      │
│           │                            │                    │
└───────────┼────────────────────────────┼───────────────────┘
            │                            │
            │                            │
┌───────────▼────────────────────────────▼───────────────────┐
│                    SERVIDOR (Backend)                        │
│                    Flask (Python)                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app.py - Lógica Principal                            │   │
│  │                                                       │   │
│  │  ✓ Flask (web framework)                             │   │
│  │  ✓ Flask-CORS (seguridad CORS)                       │   │
│  │  ✓ Flask-Mail (SMTP)                                 │   │
│  │  ✓ Stripe SDK (pagos)                                │   │
│  │  ✓ python-dotenv (variables seguras)                 │   │
│  │                                                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Endpoints:                                                  │
│  • GET /health                    → Health Check            │
│  • POST /api/send-message         → Email via Gmail SMTP    │
│  • POST /api/create-checkout      → Sesión Stripe Checkout │
│                                                              │
└─────────────────────────────────────────────────────────────┘
            │                            │
            │                            │
┌───────────▼────────────────────────────▼───────────────────┐
│            SERVICIOS EXTERNOS (3rd Party Services)          │
│                                                              │
│  ┌──────────────┐              ┌──────────────┐            │
│  │  Gmail SMTP  │              │  Stripe API  │            │
│  │  (Emails)    │              │  (Pagos)     │            │
│  └──────────────┘              └──────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Archivos

```
MI-PORTAFOLIO/
│
├── 🐍 BACKEND FLASK
│   ├── app.py                    ← Servidor principal (IMPORTANTE)
│   ├── .env.example              ← Plantilla de variables
│   ├── .env                      ← Variables reales (⚠️ NO SUBIR A GIT)
│   ├── requirements.txt          ← Dependencias Python
│   ├── test_api.py              ← Script de pruebas
│   │
│   └── venv/                     ← Entorno virtual (automático)
│
├── 🌐 FRONTEND
│   ├── index.html                ← Archivo principal (actualizado)
│   ├── style.css                 ← Estilos
│   ├── script.js                 ← JavaScript (partes actualizadas)
│   ├── success.html              ← Página de éxito de Stripe
│   │
│   └── (otros archivos HTML)
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md                 ← Documentación general
│   ├── SETUP-FLASK.md            ← Instrucciones detalladas
│   ├── QUICK-START.md            ← Guía rápida
│   ├── ARQUITECTURA.md           ← Este archivo
│   │
│   └── (otros archivos)
│
├── 🔧 CONFIGURACIÓN GIT
│   ├── .gitignore                ← Archivos a ignorar (actualizado)
│   └── .git/                     ← Repositorio Git
│
└── 📦 DEPENDENCIAS
    └── package.json              ← (Optional: si usas Node.js también)
```

---

## 🔄 Flujos de Datos

### 1️⃣ Flujo: Envío de Mensaje de Contacto

```
Usuario                        JavaScript              Flask Backend           Gmail
  │                               │                         │                    │
  ├─ Ingresa datos en form        │                         │                    │
  ├─ Click en botón               │                         │                    │
  │                               │                         │                    │
  │                        ┌──────▼────────────┐             │                    │
  │                        │ Validación básica  │             │                    │
  │                        │ (nombre, email,    │             │                    │
  │                        │  mensaje)          │             │                    │
  │                        └──────┬────────────┘             │                    │
  │                               │                         │                    │
  │                        ┌──────▼────────────────────┐    │                    │
  │                        │ fetch POST /api/send-msg  │    │                    │
  │                        │ {                         │    │                    │
  │                        │  name, email, message     │    │                    │
  │                        │ }                         │    │                    │
  │                        └──────┬──────────────────────────▼───────┐           │
  │                               │                         │        │           │
  │                               │                    ┌────▼─────────────┐     │
  │                               │                    │ Validación       │     │
  │                               │                    │ • Email válido   │     │
  │                               │                    │ • Mensaje > 10 c │     │
  │                               │                    │ • Longitud < 5K  │     │
  │                               │                    └────┬──────────────┘     │
  │                               │                         │                    │
  │                               │                    ┌────▼──────────────┐    │
  │                               │                    │ Crear HTML del    │    │
  │                               │                    │ email con datos   │    │
  │                               │                    └────┬──────────────┘    │
  │                               │                         │                    │
  │                               │                    ┌────▼──────────────┐    │
  │                               │                    │ Mail.send()       │    │
  │                               │                    │ SMTP Connection   │    │
  │                               │                    └────┬──────────────┘    │
  │                               │                         │                    │
  │                               │                         │          ┌────────▼─┐
  │                               │                         │          │ Recibe  │
  │                               │                         │          │ en inbox│
  │                               │                         │          └────────┬─┘
  │                               │                         │                    │
  │                        ┌──────▼─────────────┐             │                    │
  │                        │ JSON Response 200  │             │                    │
  │                        │ {                  │             │                    │
  │                        │  status: success   │             │                    │
  │                        │ }                  │             │                    │
  │                        └──────┬─────────────┘             │                    │
  │                               │                         │                    │
  │        ┌──────────────────────▼───────────────┐         │                    │
  │        │ Mostrar mensaje "✓ Enviado"          │         │                    │
  │        │ Limpiar formulario                   │         │                    │
  │        └────────────────────────────────────┘         │                    │
```

### 2️⃣ Flujo: Pago con Stripe

```
Usuario              JavaScript         Flask Backend         Stripe Dashboard
  │                      │                    │                      │
  ├─ Añade productos     │                    │                      │
  │  al carrito          │                    │                      │
  │                      │                    │                      │
  ├─ Click "Proceder     │                    │                      │
  │  a Pago"             │                    │                      │
  │                ┌─────▼──────────────┐     │                      │
  │                │ Validación:        │     │                      │
  │                │ ¿Carrito vacío?    │     │                      │
  │                │ ¿Items válidos?    │     │                      │
  │                └─────┬──────────────┘     │                      │
  │                      │                    │                      │
  │                ┌─────▼─────────────────────▼────────┐            │
  │                │ fetch POST /api/checkout-session   │            │
  │                │ {                                  │            │
  │                │  items: [                          │            │
  │                │    {name, price (cents), qty}      │            │
  │                │  ],                                │            │
  │                │  email: "user@email.com"           │            │
  │                │ }                                  │            │
  │                └─────┬──────────────────────────────────────┐    │
  │                      │                    │                 │    │
  │                      │                ┌───▼───────────────┐ │    │
  │                      │                │ Validar items     │ │    │
  │                      │                │ - Precios > 0     │ │    │
  │                      │                │ - Cantidades > 0  │ │    │
  │                      │                └───┬───────────────┘ │    │
  │                      │                    │                 │    │
  │                      │                ┌───▼────────────────────────────┐
  │                      │                │ stripe.checkout.Session.create │
  │                      │                │ {                             │
  │                      │                │  mode: 'payment'              │
  │                      │                │  line_items: [...]            │
  │                      │                │  success_url: /success.html   │
  │                      │                │  cancel_url: /index.html      │
  │                      │                │ }                             │
  │                      │                └───┬────────────────────────────┘
  │                      │                    │                 │            │
  │                      │                    │                 │     ┌──────▼─────┐
  │                      │                    │                 │     │ Crea sesión│
  │                      │                    │                 │     │ de checkout│
  │                      │                    │                 │     └──────┬─────┘
  │                      │                    │                 │            │
  │                ┌─────▼─────────────────────▼────────────────────┐        │
  │                │ JSON Response 200                              │        │
  │                │ {                                              │        │
  │                │  session_id: "cs_test_...",                   │        │
  │                │  url: "https://checkout.stripe.com/pay/cs..." │        │
  │                │ }                                              │        │
  │                └─────┬──────────────────────────────────────────┘        │
  │                      │                                                    │
  │     ┌────────────────▼────────────────┐                                 │
  │     │ window.location.href = url      │                                 │
  │     │ (Redirigir a Stripe Checkout)   │                                 │
  │     └────────────────┬────────────────┘                                 │
  │                      │                                                    │
  │     ┌────────────────▼─────────────────────────────────────────────────────▼──┐
  │     │ Usuario en Stripe Checkout                                              │
  │     │  - Ingresa datos de tarjeta                                             │
  │     │  - Completa pago                                                        │
  │     └────────────────┬──────────────────────────────┬─────────────────────────┘
  │                      │                              │
  │          ┌───────────▼──────────┐      ┌───────────▼──────────┐
  │          │  Pago Exitoso        │      │  Pago Cancelado      │
  │          │  → Stripe redirige a │      │  → Stripe redirige a │
  │          │    /success.html     │      │    /index.html       │
  │          └──────────────────────┘      └──────────────────────┘
  │                      │
  │     ┌────────────────▼────────────────┐
  │     │ Mostrar página de éxito         │
  │     │ "¡Pago completado!"             │
  │     │ Guardar session_id si es needed │
  │     └─────────────────────────────────┘
```

---

## 🔐 Seguridad

### Variables Sensibles (.env)

```
⚠️ NUNCA COMITEAR ESTOS ARCHIVOS EN GIT:

.env
.env.local
.env.*.local
__pycache__/
venv/
*.pyc
node_modules/
```

### Validación en Backend

```python
# Todos los datos se validan en app.py antes de procesarlos:

✓ Email: formato válido
✓ Nombre: longitud mínima (2 caracteres)
✓ Mensaje: longitud entre 10-5000 caracteres
✓ Precios: > 0, en centavos (números)
✓ Cantidades: > 0, enteros
✓ Tipos de datos: JSON válido
```

### Configuración CORS

```python
# Solo acepta solicitudes de:
✓ http://localhost:3000     (desarrollo frontend)
✓ http://localhost:5000     (desarrollo backend)
✓ http://localhost:8000     (desarrollo alternativo)
✓ https://abnerfranco.me    (producción)
✓ https://www.abnerfranco.me (producción www)
```

---

## 📱 Flujo del Usuario Final

### 1. **Ver Portafolio**
   ```
   Usuario abre index.html
   → Carga contenido estático + carrito
   ```

### 2. **Contacto**
   ```
   Usuario llena formulario
   → Click "Enviar Mensaje"
   → Backend recibe en /api/send-message
   → Valida datos
   → Envía email via Gmail
   → Muestra confirmación
   ```

### 3. **Compra**
   ```
   Usuario añade productos al carrito
   → Revisa carrito
   → Click "Proceder a Pago"
   → Backend crea sesión Stripe
   → Usuario redirigido a Stripe Checkout
   → Ingresa datos de tarjeta
   → Stripe procesa pago
   → Redirige a success.html
   ```

---

## 🛠️ Stack Tecnológico

### Backend
```
Python 3.8+
├── Flask 3.0.0           (Web Framework)
├── Flask-CORS 4.0.0      (Manejo CORS)
├── Flask-Mail 0.9.1      (SMTP)
├── Stripe 7.4.0          (Pagos)
└── python-dotenv 1.0.0   (Variables)
```

### Frontend
```
Vanilla JS (sin frameworks)
├── HTML5
├── CSS3
└── Fetch API
```

### Servicios Externos
```
Gmail SMTP              (Envío de emails)
Stripe Checkout        (Procesamiento de pagos)
```

---

## ⚙️ Cómo Funciona la Integración

### 1. **Usuario hace request desde JS**
   ```javascript
   // index.html / script.js
   await fetch('/api/send-message', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ name, email, message })
   });
   ```

### 2. **Flask recibe y valida**
   ```python
   # app.py
   @app.route('/api/send-message', methods=['POST'])
   @require_json
   def send_message():
       data = request.get_json()
       # Validar...
       # Procesar...
       # Responder...
   ```

### 3. **Backend conecta con servicio externo**
   ```python
   # Flask-Mail integrado con Gmail SMTP
   mail.send(msg)
   
   # Stripe SDK
   stripe.checkout.Session.create(...)
   ```

### 4. **JS maneja la respuesta**
   ```javascript
   if (response.ok) {
       // Éxito: mostrar mensaje o redirigir
   } else {
       // Error: mostrar a usuario
   }
   ```

---

## 📊 Modelos de Datos

### Estructura: Mensaje de Contacto
```json
{
  "name": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "message": "Me interesa tu servicio..."
}
```

### Estructura: Items del Carrito
```json
{
  "items": [
    {
      "name": "Curso Python Avanzado",
      "price": 4999,
      "quantity": 1
    }
  ],
  "email": "cliente@example.com"
}
```

### Respuesta: Sesión Stripe
```json
{
  "session_id": "cs_test_a1234567890",
  "url": "https://checkout.stripe.com/pay/cs_test_a1234567890"
}
```

---

## 🚀 Deployment

### Pasos para Producción:
1. Cambiar `ENVIRONMENT=production` en `.env`
2. Usar claves **LIVE** de Stripe (no test)
3. Actualizar `DOMAIN=https://abnerfranco.me`
4. Usar servicio de hosting (Heroku, Railway, PythonAnywhere, etc.)
5. Configurar variables en hosting (no archivo `.env`)

---

## 📞 Debugging

### Ver Logs en Desarrollo
```bash
python app.py
# Los logs aparecen en la terminal

# Busca:  ✓ Operación exitosa
#         ❌ Errores o fallos
#         ⚠️  Advertencias
```

### Usar Test Suite
```bash
python test_api.py
# Automáticamente prueba todos los endpoints
```

---

**Última actualización: 26 de febrero de 2025**  
*Créado para AbnerFranco.me*

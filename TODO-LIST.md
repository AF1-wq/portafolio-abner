# ✅ TODO LIST - Pasos Completados y Próximos

## 🎉 Lo que ya creamos para ti

### Backend Flask ✅
- [x] **app.py** - Servidor completo con 3 endpoints
  - POST /api/send-message (emails sin Gmail)
  - POST /api/create-checkout-session (pagos Stripe)
  - GET /health (verificar servidor activo)
  
- [x] **requirements.txt** - Todas las dependencias Python
  
- [x] **.env.example** - Plantilla de configuración segura
  
- [x] **.gitignore** - Protege archivos sensibles

### Frontend Actualizado ✅
- [x] **index.html** - Formulario y botones conectados al backend
- [x] **script.js** - Funciones fetch() con manejo de errores
- [x] **Validación** - En frontend y backend

### Documentación Completa ✅
- [x] **START-HERE.md** - Este es el punto de inicio 👈
- [x] **RESUMEN-COMPLETO.md** - Explicacion de todo
- [x] **QUICK-START.md** - 5 pasos rápidos
- [x] **SETUP-FLASK.md** - Guía detallada
- [x] **ARQUITECTURA.md** - Cómo funciona
- [x] **TROUBLESHOOTING.md** - 15+ problemas solucionados
- [x] **DEPLOYMENT.md** - Llevar a producción
- [x] **COMANDOS-RAPIDOS.md** - Referencia rápida

### Testing & Debugging ✅
- [x] **test_api.py** - Script automático de pruebas

---

## 📋 TU TODO LIST DE AHORA

### FASE 1: Setup Local (Hoy - 30 minutos)

#### Pre-requisitos
- [ ] Instalar Python 3.8+ (https://python.org/downloads/)
  - ℹ️ Marcar "Add Python to PATH"
  - ℹ️ Reiniciar computadora después
  
- [ ] Verificar instalación
  ```bash
  python --version
  # Debe mostrar 3.8 o superior
  ```

#### Crear Entorno
- [ ] Abrir terminal/PowerShell en la carpeta
  
- [ ] Crear entorno virtual
  ```bash
  python -m venv venv
  ```
  
- [ ] Activar entorno
  ```bash
  # Windows
  venv\Scripts\activate
  # Debe verse: (venv) al inicio
  ```

- [ ] Instalar dependencias
  ```bash
  pip install -r requirements.txt
  ```

#### Configurar Credenciales
- [ ] Copiar .env.example a .env
  ```bash
  copy .env.example .env
  ```

- [ ] **Obtener STRIPE_SECRET_KEY**
  - [ ] Ir a https://dashboard.stripe.com/apikeys
  - [ ] Copiar "Secret Key" (sk_test_...)
  - [ ] Pegar en .env

- [ ] **Obtener STRIPE_PUBLISHABLE_KEY**
  - [ ] Copiar "Publishable Key" (pk_test_...)
  - [ ] Pegar en .env

- [ ] **Obtener MAIL_PASSWORD**
  - [ ] Ir a https://myaccount.google.com/security
  - [ ] Activar "Verificación en dos pasos" (si no lo está)
  - [ ] Ir a https://myaccount.google.com/apppasswords
  - [ ] Seleccionar "Correo" → "Windows"
  - [ ] Copiar contraseña (16 caracteres)
  - [ ] Pegar en .env → MAIL_PASSWORD

- [ ] **Completar MAIL_USERNAME y MAIL_RECIPIENT**
  - [ ] MAIL_USERNAME = tu_email@gmail.com
  - [ ] MAIL_RECIPIENT = tu_email@gmail.com (o donde quieras recibir mensajes)

- [ ] Verificar .env está completo
  ```bash
  cat .env  # Asegurarse que NO hay valores vacíos
  ```

#### Pruebas Iniciales
- [ ] Ejecutar servidor Flask
  ```bash
  python app.py
  ```
  
- [ ] Verificar que muestra:
  ```
  ╔════════════════════════════════════════════════════════════╗
  ║         🚀 Servidor Flask - AbnerFranco.me                ║
  ╚════════════════════════════════════════════════════════════╝
  ```

- [ ] Abrir nueva terminal y probar health check
  ```bash
  curl http://localhost:5000/health
  # O en navegador: http://localhost:5000/health
  ```

- [ ] Debería devolver JSON con status: "ok"

---

### FASE 2: Testing (Hoy - 15 minutos)

- [ ] En una terminal con servidor corriendo, ejecutar:
  ```bash
  python test_api.py
  ```

- [ ] Debería pasar 3 tests:
  - [ ] ✓ Health Check
  - [ ] ✓ Send Message
  - [ ] ✓ Create Checkout

- [ ] Revisar inbox - debe llegar un email de prueba

---

### FASE 3: Prueba Manual (Hoy - 15 minutos)

- [ ] Abrir index.html en navegador
  - [ ] Opción 1: Doble click en index.html
  - [ ] Opción 2: `python -m http.server 8000` + http://localhost:8000
  - [ ] Opción 3: Live Server en VSCode

- [ ] **Probar formulario de contacto**
  - [ ] Llenar: Nombre, Email, Mensaje
  - [ ] Click "Enviar Mensaje"
  - [ ] Debe mostrar: "✓ Mensaje enviado"
  - [ ] Revisa inbox - debe llegar email

- [ ] **Probar carrito**
  - [ ] Scroll a "Tienda de Servicios"
  - [ ] Click "Añadir al Carrito" en un producto
  - [ ] Click en icono 🛒 (abajo derecha)
  - [ ] Debe mostrar producto con precio

- [ ] **Probar Stripe (opcional)**
  - [ ] En carrito, click "Proceder a Pago"
  - [ ] Debe redirigir a Stripe Checkout
  - [ ] Usar tarjeta test: 4242 4242 4242 4242
  - [ ] Completar pago
  - [ ] Debe ir a success.html

---

### FASE 4: Entender el Código (Mañana - 1 hora)

- [ ] Leer **ARQUITECTURA.md**
  - [ ] Entender flujo de emails
  - [ ] Entender flujo de pagos
  - [ ] Ver diagramas

- [ ] Explorar **app.py**
  - [ ] Entender decoradores
  - [ ] Ver validaciones
  - [ ] Entender manejo de errores

- [ ] Explorar **index.html (script.js)**
  - [ ] Funciones handleContactSubmit()
  - [ ] Funciones checkout()
  - [ ] Manejo de fetch

---

### FASE 5: Customización (Próximo - 30 minutos)

- [ ] Cambiar mensajes de éxito/error
- [ ] Personalizar HTML del email
- [ ] Cambiar URL de éxito/cancelación en Stripe
- [ ] Agregar más validaciones
- [ ] Cambiar estilos del formulario

---

### FASE 6: Deployar a Producción (Próximo - 2 horas)

#### Pre-requisitos
- [ ] Tener código funcional localmente
- [ ] Crear cuenta GitHub (https://github.com/signup)
- [ ] Crear repositorio privado
- [ ] Push código a GitHub

#### Elegir Hosting
- [ ] **OPCIÓN A: Railway** (Recomendado)
  - [ ] Crear cuenta https://railway.app
  - [ ] Conectar GitHub
  - [ ] Seleccionar repositorio
  - [ ] Railway deploy automáticamente
  - [ ] Obtener URL de app

- [ ] **OPCIÓN B: Heroku**
  - [ ] Crear cuenta https://heroku.com
  - [ ] Instalar Heroku CLI
  - [ ] Ejecutar `heroku create` y `git push heroku main`

- [ ] **OPCIÓN C: PythonAnywhere**
  - [ ] Crear cuenta https://pythonanywhere.com
  - [ ] Upload files
  - [ ] Configurar WSGI

#### Configurar Dominio
- [ ] Ir a tu registrador (GoDaddy, Namecheap, etc.)
- [ ] Crear CNAME record:
  - [ ] Host: @
  - [ ] Points to: tu-app-produccion.railway.app
- [ ] Esperar 5-30 minutos para DNS propague

#### Actualizar Variables Producción
- [ ] En hosting dashboard, agregar variables .env:
  - [ ] ENVIRONMENT=production
  - [ ] DOMAIN=https://abnerfranco.me
  - [ ] STRIPE_SECRET_KEY=sk_live_... (¡CAMBIAR A LIVE!)
  - [ ] Otros igual...

#### Probar en Producción
- [ ] Abrir https://abnerfranco.me/health
- [ ] Debe devolver JSON
- [ ] Probar envío de email
- [ ] Probar pago con Stripe real
- [ ] Revisar logs por errores

---

### FASE 7: Monitoreo (Continuo)

- [ ] Revisar logs regularmente
- [ ] Monitorear errores de API
- [ ] Revisar emails que llegan
- [ ] Probar pagos semanalmente

---

## 📊 Matriz de Responsabilidad

| Tarea | Backend | Frontend | DevOps |
|-------|---------|----------|--------|
| Crear venv | ✓ | | |
| Instalar requirements.txt | ✓ | | |
| Crear .env | ✓ | | |
| Obtener claves | ✓ | | |
| Ejecutar Flask | ✓ | | |
| Actualizar HTML | | ✓ | |
| Probar formulario | | ✓ | |
| Probar carrito | | ✓ | |
| Probar endpoints | ✓ | | |
| Deployar | ✓ | ✓ | ✓ |
| Configurar dominio | | | ✓ |

---

## 🎯 El mínimo para hoy

1. Instalar Python
2. `pip install -r requirements.txt`
3. Copiar .env.example a .env
4. Rellena STRIPE_SECRET_KEY y MAIL_PASSWORD
5. `python app.py`
6. `python test_api.py`
7. Abre index.html

**Si todo lo anterior sale verde: ¡FELICITACIONES!** 🎉

---

## 🆘 ¿Stuck?

1. Busca el error en **TROUBLESHOOTING.md**
2. Ejecuta `python test_api.py` para debug
3. Revisa los logs en la terminal

---

## 📞 Resumen rápido

```bash
# Terminal 1: Activar entorno
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Hacer: Copiar .env.example a .env y rellenarlo

# Terminal 1: Ejecutar servidor
python app.py

# Terminal 2: Probar endpoints
python test_api.py

# Terminal 3 / Navegador: Abrir
http://localhost:5000/health
file://ruta/a/index.html
```

---

**¡Bienvenido a tu nuevo stack Full-Stack! 🚀**

Última actualización: 26 de febrero de 2025

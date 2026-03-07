
// ════════════════════════════════════
//  PORTFOLIO DATA - CMS ESTÁTICO
// ════════════════════════════════════

const portfolioData = {
  setup: [
    {
      icon: '🎓',
      category: 'EDUCACIÓN',
      title: 'GitHub Student Developer Pack',
      description: 'Acceso a herramientas premium para desarrollo: GitHub Pro, Azure, DigitalOcean, y más de 100 herramientas profesionales.',
      specs: [
        { label: 'GitHub Pro', value: 'Repositorios privados ilimitados' },
        { label: 'Cloud Credits', value: 'Azure + DigitalOcean' },
        { label: 'Herramientas', value: '+100 recursos premium' }
      ]
    },
    {
      icon: '💻',
      category: 'HARDWARE',
      title: 'Desarrollo & Producción',
      description: 'Equipo optimizado para desarrollo web full-stack, testing y deployment de aplicaciones.',
      specs: [
        { label: 'Procesador', value: 'AMD Ryzen 5' },
        { label: 'RAM', value: '16GB DDR4' },
        { label: 'Almacenamiento', value: 'SSD 512GB NVMe' }
      ]
    },
    {
      icon: '⚙️',
      category: 'STACK TECNOLÓGICO',
      title: 'Entorno de Desarrollo',
      description: 'Herramientas y lenguajes que utilizo diariamente para construir sistemas web robustos y escalables.',
      specs: [
        { label: 'Backend', value: 'PHP 8.x + MySQL' },
        { label: 'Frontend', value: 'HTML5 + CSS3 + JavaScript' },
        { label: 'Control de Versiones', value: 'Git + GitHub' }
      ]
    }
  ]
};

// ════════════════════════════════════
//  PRODUCTOS TIENDA
// ════════════════════════════════════

const productos = [
  {
    id: 1,
    name: 'Curso PHP Avanzado',
    description: 'Domina PHP desde cero hasta nivel profesional con 15+ proyectos reales',
    price: 49.99,
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=870',
    badge: 'MÁS VENDIDO',
    demoUrl: '#'
  },
  {
    id: 2,
    name: 'Master SQL & MySQL',
    description: 'Aprende SQL, diseño de bases de datos y optimización de queries',
    price: 39.99,
    image: 'https://images.unsplash.com/photo-1593720213428-28a5b9e94613?auto=format&fit=crop&q=80&w=870',
    badge: 'NUEVO',
    demoUrl: '#'
  },
  {
    id: 3,
    name: 'Frontend Moderno',
    description: 'HTML5, CSS3, JavaScript ES6+ y frameworks modernos para web',
    price: 44.99,
    image: 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&q=80&w=870',
    demoUrl: '#'
  },
  {
    id: 4,
    name: 'Arquitectura de Software',
    description: 'Diseño de sistemas escalables y patrones de arquitectura para aplicaciones web',
    price: 54.99,
    image: 'https://images.unsplash.com/photo-1618477388954-7852f32655ec?auto=format&fit=crop&q=80&w=870',
    badge: 'PRO',
    demoUrl: '#'
  },
  {
    id: 5,
    name: 'Desarrollo de APIs REST',
    description: 'Crea APIs escalables y seguras con PHP, autenticación JWT y más',
    price: 59.99,
    image: 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&q=80&w=870',
    demoUrl: '#'
  },
  {
    id: 6,
    name: 'Deploy & DevOps Básico',
    description: 'Deploya tus proyectos en producción con mejor práctica y seguridad',
    price: 34.99,
    image: 'https://images.unsplash.com/photo-1607798748738-b15c40d33d57?auto=format&fit=crop&q=80&w=870',
    demoUrl: '#'
  }
];

// ════════════════════════════════════
//  CARRITO - ESTADO GLOBAL
// ════════════════════════════════════

let cart = [];

// ════════════════════════════════════
//  FUNCIONES CARRITO
// ════════════════════════════════════

function addToCart(productId, quantity) {
  if (!quantity || quantity < 1) {
    alert('Por favor selecciona una cantidad válida');
    return;
  }

  const product = productos.find(p => p.id === productId);
  if (!product) {
    console.error('Producto no encontrado:', productId);
    return;
  }

  const existingItem = cart.find(item => item.id === productId);
  if (existingItem) {
    existingItem.qty += quantity;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      price: product.price,
      qty: quantity
    });
  }
  updateCart();
}

function removeFromCart(productId) {
  cart = cart.filter(item => item.id !== productId);
  updateCart();
}

function updateCart() {
  const cartItems = document.getElementById('cartItems');
  const cartCount = document.getElementById('cartCount');
  const cartTotal = document.getElementById('cartTotal');

  cartItems.innerHTML = '';
  let total = 0;
  let count = 0;
  const fragment = document.createDocumentFragment();

  cart.forEach(item => {
    total += item.price * item.qty;
    count += item.qty;

    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
        <div class="cart-item-info">
          <h4>${item.name}</h4>
          <p>$${item.price} x ${item.qty}</p>
        </div>
        <button class="cart-item-remove" onclick="removeFromCart(${item.id})">✕</button>
      `;
    fragment.appendChild(div);
  });

  cartItems.appendChild(fragment);
  cartCount.textContent = count;
  cartTotal.textContent = `$${total.toFixed(2)}`;
}

// ════════════════════════════════════
//  FUNCIONES CHECKOUT (DESHABILITADO)
// ════════════════════════════════════

function checkout() {
  // Validar que el carrito no esté vacío
  if (!cart || cart.length === 0) {
    alert('❌ Tu carrito está vacío. Añade productos antes de continuar.');
    return;
  }

  // TODO: SISTEMA DE PAGOS DESHABILITADO
  // Para habilitar pagos reales, necesitas:
  // 1. Crear cuenta en Stripe (https://stripe.com) o MercadoPago
  // 2. Obtener API keys (Secret Key y Publishable Key)
  // 3. Agregar credenciales en .env del backend:
  //    STRIPE_SECRET_KEY=sk_test_...
  //    STRIPE_PUBLISHABLE_KEY=pk_test_...
  // 4. Crear endpoint en app.py: POST /api/create-checkout-session
  // 5. Configurar webhook para confirmar pagos
  // 6. Descomentar el código de integración aquí abajo
  
  // Código de ejemplo para cuando habilites Stripe:
  // const response = await fetch('/api/create-checkout-session', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ items: cart })
  // });
  // const session = await response.json();
  // window.location.href = session.url;  // Redirigir a Stripe Checkout
  
  // Mostrar mensaje de sistema deshabilitado
  alert('El sistema de compras automáticas está deshabilitado temporalmente. Por favor, contáctame a través del formulario principal para adquirir este producto.');
  
  // Vaciar el carrito
  cart = [];
  
  // Actualizar la interfaz visual del carrito
  updateCart();
}

// ════════════════════════════════════
//  RENDER DINÁMICO
// ════════════════════════════════════

function renderSetup() {
  const grid = document.getElementById('setupGrid');
  const fragment = document.createDocumentFragment();

  portfolioData.setup.forEach(card => {
    const div = document.createElement('div');
    div.className = 'setup-card fade-in';
    div.innerHTML = `
        <div class="setup-icon">${card.icon}</div>
        <p class="setup-category">${card.category}</p>
        <h3>${card.title}</h3>
        <p>${card.description}</p>
        <div class="setup-specs">
          ${card.specs.map(spec => `
            <div class="setup-spec-item">
              <span>${spec.label}</span>
              <strong>${spec.value}</strong>
            </div>
          `).join('')}
        </div>
      `;
    fragment.appendChild(div);
  });

  grid.appendChild(fragment);
}

function renderProducts() {
  const grid = document.getElementById('productGrid');
  const fragment = document.createDocumentFragment();

  productos.forEach(p => {
    const div = document.createElement('div');
    div.className = 'product-card fade-in';
    div.innerHTML = `
        <div class="product-media">
          <img src="${p.image}" alt="${p.name}" loading="lazy">
          ${p.badge ? `<div class="product-badge">${p.badge}</div>` : ''}
        </div>
        <h3>${p.name}</h3>
        <p>${p.description}</p>
        <div class="product-price">$${p.price}</div>
        <div class="product-buttons">
          <input type="number" value="1" min="1" class="qty-input" id="qty-${p.id}">
          <button class="add-to-cart-btn" onclick="addToCart(${p.id}, document.getElementById('qty-${p.id}').valueAsNumber)">
            Añadir al Carrito
          </button>
        </div>
      `;
    fragment.appendChild(div);
  });

  grid.appendChild(fragment);
}

// ════════════════════════════════════
//  MANEJO DE EVENTOS
// ════════════════════════════════════

function toggleMenu() {
  const navLinks = document.getElementById('navLinks');
  navLinks.classList.toggle('active');
}

function toggleCart() {
  const cartDrawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('overlay');
  cartDrawer.classList.toggle('open');
  overlay.classList.toggle('show');
}

function closeOverlays() {
  document.getElementById('cartDrawer').classList.remove('open');
  document.getElementById('overlay').classList.remove('show');
}

async function handleContactSubmit(event) {
  event.preventDefault();
  const form = event.target;

  // Obtener valores del formulario
  const nameInput = form.querySelector('input[placeholder="Tu nombre completo"]');
  const emailInput = form.querySelector('input[type="email"]');
  const messageInput = form.querySelector('textarea');

  const name = nameInput?.value?.trim() || '';
  const email = emailInput?.value?.trim() || '';
  const message = messageInput?.value?.trim() || '';

  // Validación de campos
  if (!name) {
    alert('❌ Por favor ingresa tu nombre');
    return;
  }
  if (!email) {
    alert('❌ Por favor ingresa tu email');
    return;
  }
  if (!message) {
    alert('❌ Por favor escribe un mensaje');
    return;
  }

  // Mostrar loading en botón
  const sendBtn = document.getElementById('sendBtn');
  const originalText = sendBtn.textContent;
  sendBtn.disabled = true;
  sendBtn.textContent = '⏳ Enviando...';

  try {
    // Timeout de 15 segundos para prevenir esperas indefinidas
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    const response = await fetch('/api/send-message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name,
        email: email,
        message: message
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Error al enviar el mensaje');
    }

    // Éxito
    sendBtn.style.background = '#16a34a';
    sendBtn.textContent = '✓ ¡Mensaje enviado! Gracias.';
    form.reset();

    // Restaurar después de 4 segundos
    setTimeout(() => {
      sendBtn.style.background = '';
      sendBtn.textContent = originalText;
      sendBtn.disabled = false;
    }, 4000);

  } catch (error) {
    console.error('❌ Error en contacto:', error);
    
    if (error.name === 'AbortError') {
      alert('❌ Timeout: El servidor tardó demasiado en responder. Por favor, inténtalo de nuevo.');
    } else {
      alert(`❌ Error: ${error.message}\n\nAsegúrate de que el servidor Flask está ejecutándose en http://localhost:5000`);
    }
    
    sendBtn.style.background = '';
    sendBtn.textContent = originalText;
  } finally {
    sendBtn.disabled = false;
  }
}


// ════════════════════════════════════
//  INICIALIZACIÓN
// ════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  renderSetup();
  renderProducts();

  // Intersection Observer para animaciones "fade-in" con throttling
  const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Dejar de observar después de animar
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
});

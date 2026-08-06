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

// ════════════════════════════════════
//  MANEJO DE EVENTOS
// ════════════════════════════════════

function toggleMenu() {
  const navLinks = document.getElementById('navLinks');
  navLinks.classList.toggle('active');
}

// Función mejorada para validar email
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email.toLowerCase());
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

  // Validación de campos con mensajes específicos
  if (!name || name.length < 2) {
    alert('❌ Por favor ingresa un nombre válido (mínimo 2 caracteres)');
    nameInput?.focus();
    return;
  }
  if (!email || !isValidEmail(email)) {
    alert('❌ Por favor ingresa una dirección de email válida');
    emailInput?.focus();
    return;
  }
  if (!message || message.length < 10) {
    alert('❌ Por favor escribe un mensaje (mínimo 10 caracteres)');
    messageInput?.focus();
    return;
  }

  // Obtener botón y guardar estado original
  const sendBtn = document.getElementById('sendBtn');
  const originalText = sendBtn.textContent;
  const originalBg = sendBtn.style.background;
  
  // Deshabilitar botón y mostrar estado de carga
  sendBtn.disabled = true;
  sendBtn.style.pointerEvents = 'none';
  sendBtn.textContent = '⏳ Enviando...';
  sendBtn.style.opacity = '0.7';

  try {
    // Configurar timeout de 15 segundos para la petición
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, 15000);

    // Realizar petición fetch con manejo robusto
    const response = await fetch('/api/send-message', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        email: email,
        message: message
      }),
      signal: controller.signal
    });

    // Limpiar timeout si la respuesta llegó a tiempo
    clearTimeout(timeoutId);

    // Intentar parsear JSON
    let data;
    try {
      data = await response.json();
    } catch (parseError) {
      console.error('❌ Error al parsear respuesta JSON:', parseError);
      throw new Error('Respuesta del servidor inválida');
    }

    // Verificar si la respuesta fue exitosa
    if (!response.ok) {
      throw new Error(data.error || `Error del servidor: ${response.status}`);
    }

    // ✓ ÉXITO: Mensaje enviado correctamente
    sendBtn.style.background = '#16a34a';
    sendBtn.textContent = '✓ ¡Mensaje enviado! Gracias.';
    sendBtn.style.opacity = '1';
    
    // Limpiar formulario
    form.reset();
    nameInput?.focus();

    // Restaurar botón después de 4 segundos
    setTimeout(() => {
      sendBtn.style.background = originalBg;
      sendBtn.textContent = originalText;
      sendBtn.style.opacity = '1';
      sendBtn.disabled = false;
      sendBtn.style.pointerEvents = 'auto';
    }, 4000);

  } catch (error) {
    console.error('❌ Error en contacto:', error);
    
    // Determinar tipo de error y proporcionar mensaje específico
    let errorMessage = 'Error desconocido';

    if (error.name === 'AbortError') {
      errorMessage = '❌ Timeout: El servidor tardó demasiado en responder (>15s).\n\nPor favor, inténtalo de nuevo. Si el problema persiste, verifica tu conexión o contacta directamente.';
    } else if (error instanceof TypeError && error.message.includes('fetch')) {
      errorMessage = '❌ Error de conexión: No se puede conectar al servidor.\n\nAsegúrate de que:\n- El servidor Flask está ejecutándose\n- Tienes conexión a internet\n- El dominio es accesible';
    } else if (error.message.includes('JSON')) {
      errorMessage = '❌ Error de respuesta del servidor (formato inválido).\n\nPor favor, inténtalo de nuevo.';
    } else {
      errorMessage = `❌ Error: ${error.message}`;
    }

    alert(errorMessage);
    
    // Restaurar botón a estado normal para permitir reintento
    sendBtn.style.background = '#ff6b6b'; // Mostrar que hubo error
    sendBtn.textContent = '↻ Reintentar';
    
    setTimeout(() => {
      sendBtn.style.background = originalBg;
      sendBtn.textContent = originalText;
      sendBtn.disabled = false;
      sendBtn.style.pointerEvents = 'auto';
      sendBtn.style.opacity = '1';
    }, 3000);

  } finally {
    // Asegurar que el botón siempre sea habilitado y visible
    sendBtn.disabled = false;
    sendBtn.style.pointerEvents = 'auto';
  }
}

// ════════════════════════════════════
//  INICIALIZACIÓN
// ════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  renderSetup();

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

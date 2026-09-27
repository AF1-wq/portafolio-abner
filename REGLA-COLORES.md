# REGLA DE PROTECCIÓN DE COLORES — Portafolio Abner Franco
# ==========================================================
# Fecha creación: 2026-09-15
#
# CONTEXTO DEL PROBLEMA:
# Un agente anterior introdujo el color azul marino oscuro (#0a192f)
# en variables CSS que representan BLANCO/CLARO. Eso causó fondos
# y elementos oscuros donde deberían ser blancos.
#
# VARIABLES CSS CORRECTAS (public/about.html, work.html, archive.html, contact.html):
# ─────────────────────────────────────────────────────────────────────
# --color-dark:       #FFFFFF   ← fondo principal (BLANCO)
# --color-dark-dark:  #FFFFFF   ← fondo secundario (BLANCO)
# --color-white:      #FFFFFF   ← blanco puro — NUNCA debe ser #0a192f
# --color-light:      #FFFFFF   ← claro — NUNCA debe ser #0a192f
# --color-text:       #0a192f   ← texto oscuro sobre fondo blanco (CORRECTO)
# --color-text-light: #FFFFFF   ← texto claro (sobre fondos oscuros si los hay)
# --color-gray:       #999D9E   ← gris neutro — NUNCA debe ser #0a192f
# --color-blue:       #455CE9   ← azul de acento
# --color-blue-dark:  #334BD3   ← azul oscuro de acento
#
# REGLA DE ORO:
# ► El color #0a192f SOLO puede aparecer en propiedades "color:" (texto)
#   NUNCA en "background:", "background-color:", ni en variables *-white, *-light, *-gray
#
# VERIFICACIÓN RÁPIDA (corre en PowerShell):
# Select-String -Path "public\*.html" -Pattern "--color-white:\s*#0a192f|--color-light:\s*#0a192f|--color-gray:\s*#0a192f|background.*#0a192f"
# → Si da resultados, algo está MAL.
#
# DISEÑO: Apple One UI / Liquid Glass — fondo blanco, texto oscuro
# NO añadir iconos, no restaurar index antiguos, no cambiar el diseño

# ADICIÓN: El azul oscuro también aparece como RGBA
# rgba(10, 25, 47, ...) es exactamente #0a192f en formato rgba.
# Fue encontrado en el gradiente del overlay del footer (.footer-wrap.theme-dark .overlay-gradient)
# y causaba la "ola oscura" encima del footer.
#
# VERIFICACIÓN AMPLIADA (corre en PowerShell):
# Select-String -Path "public\*.html" -Pattern "--color-white:\s*#0a192f|--color-light:\s*#0a192f|--color-gray:\s*#0a192f|background.*#0a192f|rgba\(10,\s*25,\s*47"
# → Si da resultados, algo está MAL.

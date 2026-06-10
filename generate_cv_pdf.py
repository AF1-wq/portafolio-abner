from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm

doc = SimpleDocTemplate("CV.pdf", pagesize=A4,
                        rightMargin=20*mm, leftMargin=20*mm,
                        topMargin=20*mm, bottomMargin=20*mm)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('title', parent=styles['Heading1'], fontSize=24, leading=28)
h2 = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=12, leading=14)
normal = ParagraphStyle('normal', parent=styles['Normal'], fontSize=10, leading=14)

content = []

content.append(Paragraph('Abner Franco', title_style))
content.append(Spacer(1, 6))
content.append(Paragraph('El Salvador • abnerfranco.me • contacto@abnerfranco.me', normal))
content.append(Spacer(1, 12))

content.append(Paragraph('Resumen', h2))
content.append(Paragraph('Estudiante de 2° año de Técnico en Laboratorio Químico y Desarrollador Web. Desarrollé el simulador hospitalario INSAM Salud, implementando protocolos de ciberseguridad y despliegue en la nube para entornos educativos. Tengo experiencia en ventas y gestión de clientes en el sector de telecomunicaciones.', normal))
content.append(Spacer(1, 10))

content.append(Paragraph('Experiencia Profesional', h2))
content.append(Paragraph('<b>Crece Centro América S.A.S.V.</b> — Ejecutivo de Venta, San Salvador | Oct 2025 – Abr 2026.<br/>Asesoré a clientes residenciales logrando el cumplimiento de metas comerciales mensuales. Gestioné carteras de clientes mediante atención directa, resolviendo conflictos y mejorando la retención de usuarios.', normal))
content.append(Spacer(1, 6))
content.append(Paragraph('<b>Advance Energy</b> — Auxiliar en Energías Renovables, San Salvador | Nov 2024 – Feb 2025.<br/>Apoyé operativamente en proyectos de energía, adaptándome rápidamente a procesos técnicos y normas de seguridad.', normal))
content.append(Spacer(1, 10))

content.append(Paragraph('Proyectos', h2))
content.append(Paragraph('<b>INSAM Salud</b> — Desarrollador Principal | Mar 2026.<br/>Construí un simulador de gestión hospitalaria desde cero para estudiantes de salud. Implementé medidas de seguridad frente a CSRF y optimicé la base de datos para el manejo de registros. Desplegué la aplicación en DigitalOcean.', normal))
content.append(Spacer(1, 6))
content.append(Paragraph('<b>Portafolio Personal (abnerfranco.me)</b> — Desarrollador | Ene 2026.<br/>Programé un sitio interactivo usando Python y Flask; integré control de versiones con Git y configuré dominios personalizados.', normal))
content.append(Spacer(1, 10))

content.append(Paragraph('Educación', h2))
content.append(Paragraph('ITCA-FEPADE — Técnico en Laboratorio Químico (2° Año). Santa Tecla, El Salvador — Actualidad', normal))
content.append(Spacer(1, 10))

content.append(Paragraph('Habilidades', h2))
content.append(Paragraph('Tecnologías: Python (Flask), HTML, Java, Git/GitHub. Herramientas: Excel (Intermedio), Adobe Suite (Intermedio). Idiomas: Español (Nativo), Inglés (Básico).', normal))

doc.build(content)

print('CV.pdf generado correctamente.')

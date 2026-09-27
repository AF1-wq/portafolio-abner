import os

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the text
old_text = '<h4><span>Independiente</span> Diseñador &amp; Desarrollador</h4>'
new_text = '<h4><span>Creador de</span> Experiencias Web</h4>'

# Also try without the amp; just in case
old_text_alt = '<h4><span>Independiente</span> Diseñador & Desarrollador</h4>'

if old_text in content:
    content = content.replace(old_text, new_text)
elif old_text_alt in content:
    content = content.replace(old_text_alt, new_text)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done replacing subtitle')

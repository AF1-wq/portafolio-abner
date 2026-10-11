import os
import glob

files = glob.glob('public/*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Original text
    old_1 = '<h2 class="home-active home-active-first">Inicio<div class="dot"></div></h2>'
    old_2 = '<h2 class="home-active">Proyectos<div class="dot"></div></h2>'
    old_3 = '<h2 class="home-active-last">Abner Franco<div class="dot"></div></h2>'

    # New text
    new_1 = '<h2 class="home-active home-active-first">Bienvenidos<div class="dot"></div></h2>'
    new_2 = '<h2 class="home-active">a mi<div class="dot"></div></h2>'
    new_3 = '<h2 class="home-active-last">portafolio<div class="dot"></div></h2>'

    content = content.replace(old_1, new_1)
    content = content.replace(old_2, new_2)
    content = content.replace(old_3, new_3)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done replacing loading words')

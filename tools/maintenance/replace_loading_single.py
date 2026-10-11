import os
import glob

files = glob.glob('public/*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The current text to replace
    old_text = '''<h2 class="home-active home-active-first">Bienvenidos<div class="dot"></div></h2>
<h2 class="home-active">a mi<div class="dot"></div></h2>
<h2 class="home-active-last">portafolio<div class="dot"></div></h2>'''

    new_text = '<h2 class="home-active-first home-active-last">Bienvenidos a mi portafolio .</h2>'

    content = content.replace(old_text, new_text)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done replacing loading words with single line')

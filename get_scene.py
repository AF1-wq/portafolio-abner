import sys
c = open('index.html', 'r', encoding='utf-8').read()
start = c.find('<div class="proj-grid" id="pGrid">')
end = c.find('<div class="proj-card reveal reveal-d1" data-cat="web">', start)
open('original_scene1_utf8.txt', 'w', encoding='utf-8').write(c[start:end])

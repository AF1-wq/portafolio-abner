import sys
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
start = c.find('<div class="proj-grid" id="pGrid">')
end = c.find('<div class="proj-card reveal reveal-d1" data-cat="web">', start)
old = c[start:end]
new = open('original_scene1_utf8.txt', 'r', encoding='utf-8').read()
c = c.replace(old, new)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('patched!')

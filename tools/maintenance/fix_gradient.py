import os
import glob

files = glob.glob('public/*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Disable the overlay gradient shadow
    content = content.replace(
        'background: linear-gradient(to bottom,rgba(10, 25, 47, 1) 0%, rgba(10, 25, 47, 0) 100%);\n   opacity: .75;',
        'background: none; /* removed shadow */\n   display: none;\n   opacity: 0;'
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done fixing gradient')

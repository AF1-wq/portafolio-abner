import os
import glob
import re

files = glob.glob('public/*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix box-shadow on footer-wrap and footer-contact
    content = content.replace('box-shadow: 0px 5px 0px 5px var(--color-dark);', 'box-shadow: 0px 10px 0px 0px var(--color-dark);')

    # 2. Fix gradient shadow in overlay-gradient
    # We'll just replace 'opacity: .75;' to 'display: none;' in the block for .overlay-gradient
    # Let's match the block roughly
    content = re.sub(
        r'(\.footer-wrap\.theme-dark \.overlay-gradient\s*\{[\s\S]*?)opacity: \.75;(\s*\})',
        r'\1display: none;\2',
        content
    )

    # 3. Fix potential subpixel gap
    # Replace .footer-rounded-div .rounded-div-wrap { transform: translateY(-1px);
    content = re.sub(
        r'(\.footer-rounded-div \.rounded-div-wrap\s*\{\s*transform: translateY\()-1px(\);)',
        r'\1-2px\2',
        content
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done fixing shadows')

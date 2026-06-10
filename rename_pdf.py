import os

src = r"c:\Users\abner\Downloads\MI-PORTAFOLIO\abner FRANCO cv2.pdf"
dst = r"c:\Users\abner\Downloads\MI-PORTAFOLIO\CV.pdf"

try:
    os.replace(src, dst)
    print('RENAMED')
except Exception as e:
    print('ERROR', e)

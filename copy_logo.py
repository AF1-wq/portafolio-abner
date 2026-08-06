import os
import shutil

source = r"C:\Users\abner\.gemini\antigravity-ide\brain\dad52a2f-b597-4d61-b073-753576a6ba32\logo_af_1786038578749.png"
dest = r"c:\Users\abner\Downloads\MI-PORTAFOLIO\assets\img\logo_af.png"

try:
    if os.path.exists(source):
        shutil.copy(source, dest)
        print("✅ Logo copiado exitosamente a assets/img/logo_af.png")
    else:
        print("❌ Error: No se encontró el logo generado en la ruta origen.")
except Exception as e:
    print(f"❌ Error al copiar el logo: {e}")

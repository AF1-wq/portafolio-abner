import os
import re

# 1. Eliminar archivos basura y residuales
files_to_delete = [
    "app - Acceso directo.lnk",
    "index - Acceso directo.lnk",
    "get_scene.py",
    "patch.py",
    "rename_pdf.py",
    "write_patch.py",
    "original_scene1.txt",
    "original_scene1_utf8.txt"
]

print("Iniciando limpieza de archivos...")
for f in files_to_delete:
    try:
        if os.path.exists(f):
            os.remove(f)
            print(f"✅ Eliminado: {f}")
    except Exception as e:
        print(f"❌ Error eliminando {f}: {e}")

print("\nExtrayendo CSS de index.html a style.css...")
# 2. Extraer CSS de index.html a style.css
try:
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Buscar la etiqueta <style>...</style>
    style_match = re.search(r"<style>(.*?)</style>", content, flags=re.DOTALL | re.IGNORECASE)
    if style_match:
        css_content = style_match.group(1).strip()
        
        # Guardar en style.css (sobrescribiendo el contenido viejo no utilizado)
        with open("style.css", "w", encoding="utf-8") as f:
            f.write(css_content)
            print("✅ CSS extraído correctamente y guardado en style.css")
            
        # Reemplazar <style> en index.html por <link>
        new_content = content[:style_match.start()] + '<link rel="stylesheet" href="style.css">' + content[style_match.end():]
        
        # También eliminamos el drawer del carrito en index.html si aún existe
        # Buscamos el HTML del carrito y lo eliminamos
        cart_regex = r'<div class="cart-drawer" id="cartDrawer">.*?</div>\s*<div class="overlay" id="overlay" onclick="closeOverlays\(\)"></div>'
        new_content = re.sub(cart_regex, '', new_content, flags=re.DOTALL)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
            print("✅ index.html actualizado con la etiqueta <link> y sin el HTML del carrito")
    else:
        print("⚠️ No se encontró la etiqueta <style> en index.html (probablemente ya se extrajo).")
except Exception as e:
    print(f"❌ Error en la extracción: {e}")

print("\n¡Proceso de limpieza y refactorización completado con éxito!")

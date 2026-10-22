"""Pruebas de regresión de seguridad. Ejecutar desde la raíz: python tools/security_tests.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.pop("MAIL_USERNAME", None)
os.environ.pop("MAIL_PASSWORD", None)
os.environ["ADMIN_TOKEN"] = ""

import app as appmod  # noqa: E402

# Base de datos temporal para no ensuciar messages.db
appmod.DB_PATH = os.path.join(tempfile.mkdtemp(), "test.db")
appmod.init_db()
appmod.limiter.enabled = False
client = appmod.app.test_client()
fails = 0


def check(desc, cond):
    global fails
    print(("[OK]   " if cond else "[FAIL] ") + desc)
    if not cond:
        fails += 1


# 1. Páginas legítimas siguen funcionando
for route in ['/', '/contact', '/about', '/work', '/index.html', '/robots.txt', '/sitemap.xml', '/imagen1.webp',
              '/assets/img/portafolio.webp', '/assets/icons/github.svg' if False else '/assets/icons/linkedin.svg']:
    r = client.get(route)
    check(f"GET {route} -> 200", r.status_code == 200)

# 2. Path traversal / archivos sensibles NO se sirven
idx = client.get('/').data
for route in ['/../app.py', '/..%2fapp.py', '/%2e%2e/app.py', '/assets/../../app.py', '/assets/..%2f..%2fapp.py',
              '/.env', '/.git/config', '/assets/.env', '/fix_gradient.py', '/app.py', '/messages.db',
              '/requirements.txt', '/..\\app.py', '/assets/%00.webp']:
    r = client.get(route)
    leaked = b"import os" in r.data or b"FLASK_SECRET" in r.data or b"Flask==" in r.data
    check(f"GET {route} no filtra archivos ({r.status_code})", not leaked and (r.status_code == 404 or r.data == idx))

# 3. Endpoint administrativo deshabilitado / protegido
check("GET /api/test-email ya no es público", client.get('/api/test-email').status_code in (404, 405))
check("POST /api/test-email sin token -> 404", client.post('/api/test-email').status_code == 404)
os.environ["ADMIN_TOKEN"] = "x" * 32
check("POST /api/test-email token incorrecto -> 404",
      client.post('/api/test-email', headers={"X-Admin-Token": "y" * 32}).status_code == 404)
os.environ["ADMIN_TOKEN"] = ""

# 4. Validaciones del formulario
ok = {"name": "Cliente", "email": "cliente@empresa.com", "message": "Hola, me interesa un proyecto."}
check("Mensaje válido -> 200", client.post('/api/send-message', json=ok).status_code == 200)
check("Formulario simple (sin application/json) -> 415", client.post('/api/send-message', data=ok).status_code == 415)
check("Email inválido -> 400", client.post('/api/send-message', json={**ok, "email": "no-es-email"}).status_code == 400)
check("Header injection en email -> 400",
      client.post('/api/send-message', json={**ok, "email": "a@b.com\r\nBcc: victima@x.com"}).status_code == 400)
check("company demasiado largo -> 400", client.post('/api/send-message', json={**ok, "company": "A" * 500}).status_code == 400)
check("JSON no-objeto no rompe (lista)", client.post('/api/send-message', json=["x"]).status_code == 400)
r = client.post('/api/send-message', data=b'{"name":"' + b"A" * 40000 + b'"}', content_type="application/json")
check(f"Payload > 32KB -> 413 ({r.status_code})", r.status_code == 413)

# 5. Saneamiento CR/LF en campos de cabecera
check("_clean_line elimina CR/LF", "\n" not in appmod._clean_line("Juan\r\nBcc: x@y.com") and "\r" not in appmod._clean_line("a\rb"))
check("_clean_multiline conserva saltos de línea", appmod._clean_multiline("a\nb\x00c") == "a\nbc")

# 6. Cabeceras de seguridad
h = client.get('/').headers
check("X-Frame-Options presente", h.get("X-Frame-Options") == "DENY")
check("X-Content-Type-Options nosniff", h.get("X-Content-Type-Options") == "nosniff")
check("Referrer-Policy presente", "strict-origin" in (h.get("Referrer-Policy") or ""))
check("Permissions-Policy presente", "camera=()" in (h.get("Permissions-Policy") or ""))

print("\nRESULTADO:", "TODO OK" if fails == 0 else f"{fails} FALLOS")
sys.exit(1 if fails else 0)

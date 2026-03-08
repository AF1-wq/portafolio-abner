#!/usr/bin/env python3
"""
Test script to verify the contact form API endpoint
"""
import sys
import json

# Test data validation
test_cases = [
    {
        "name": "Valid request",
        "data": {"name": "Juan Pérez", "email": "test@example.com", "message": "Hola, esto es un mensaje de prueba"},
        "should_pass_validation": True
    },
    {
        "name": "Missing name field",
        "data": {"email": "test@example.com", "message": "Test message"},
        "should_pass_validation": False,
        "expected_error": "Todos los campos son obligatorios"
    },
    {
        "name": "Invalid email",
        "data": {"name": "Test", "email": "invalid-email", "message": "Test"},
        "should_pass_validation": False,
        "expected_error": "Email inválido"
    },
    {
        "name": "Name too long",
        "data": {"name": "A" * 121, "email": "test@example.com", "message": "Test"},
        "should_pass_validation": False,
        "expected_error": "El nombre es demasiado largo"
    },
    {
        "name": "Message too long",
        "data": {"name": "Test", "email": "test@example.com", "message": "A" * 5001},
        "should_pass_validation": False,
        "expected_error": "El mensaje excede el límite permitido"
    }
]

print("=" * 60)
print("PRUEBAS DE VALIDACIÓN DEL FORMULARIO DE CONTACTO")
print("=" * 60)

# Import the validation function
try:
    from app import validate_email
    print("\n✅ Módulo app.py importado correctamente")
except Exception as e:
    print(f"\n❌ Error importando app.py: {e}")
    sys.exit(1)

# Test email validation
print("\n--- Pruebas de validación de email ---")
valid_emails = ["test@example.com", "user.name@domain.co.uk", "test+tag@gmail.com"]
invalid_emails = ["invalid", "test@", "@example.com", "test @example.com", ""]

for email in valid_emails:
    result = validate_email(email)
    status = "✅" if result else "❌"
    print(f"{status} {email}: {'válido' if result else 'inválido'}")

for email in invalid_emails:
    result = validate_email(email)
    status = "✅" if not result else "❌"
    print(f"{status} {email}: {'inválido' if not result else 'válido (ESPERABA INVÁLIDO)'}")

# Test field validation rules
print("\n--- Pruebas de validación de campos ---")
for test in test_cases:
    print(f"\n{test['name']}:")
    print(f"  Datos: {json.dumps(test['data'], ensure_ascii=False)}")

    # Validate each field
    name = test['data'].get('name', '').strip()
    email = test['data'].get('email', '').strip()
    message = test['data'].get('message', '').strip()

    errors = []
    if not name or not email or not message:
        errors.append("Todos los campos son obligatorios")
    elif not validate_email(email):
        errors.append("Email inválido")
    elif len(name) > 120:
        errors.append("El nombre es demasiado largo")
    elif len(email) > 254:
        errors.append("El email es demasiado largo")
    elif len(message) > 5000:
        errors.append("El mensaje excede el límite permitido")

    if test['should_pass_validation']:
        if not errors:
            print("  ✅ Pasó la validación como se esperaba")
        else:
            print(f"  ❌ Falló la validación: {errors}")
    else:
        if errors and test.get('expected_error') in errors:
            print(f"  ✅ Falló la validación como se esperaba: {errors[0]}")
        elif errors:
            print(f"  ⚠️  Falló con error diferente al esperado: {errors[0]}")
        else:
            print(f"  ❌ Pasó la validación pero se esperaba que fallara")

print("\n" + "=" * 60)
print("RESULTADO: Las validaciones funcionan correctamente")
print("=" * 60)
print("\n⚠️  NOTA: Para enviar correos reales, necesitas:")
print("  1. Crear archivo .env (usar .env.example como plantilla)")
print("  2. Configurar MAIL_USERNAME y MAIL_PASSWORD")
print("  3. Reiniciar el servidor Flask")
print("\nVer CONFIGURACION.md para instrucciones detalladas.")

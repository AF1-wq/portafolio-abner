import os
import sys
import sqlite3
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, init_db

def test_full_flow():
    print(">>> 1. Initializing DB and checking schema...")
    init_db()
    
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(messages)")
    cols = [row[1] for row in c.fetchall()]
    print(f"Columns in messages table: {cols}")
    assert "company" in cols, "Column 'company' missing in messages table"
    assert "service" in cols, "Column 'service' missing in messages table"
    assert "source" in cols, "Column 'source' missing in messages table"
    
    print(">>> 2. Testing /api/send-message endpoint...")
    client = app.test_client()
    test_payload = {
        "name": "Cliente Interesado",
        "email": "cliente.empresa@gmail.com",
        "company": "Laboratorios & Software S.A.",
        "service": "Desarrollo Web Full-Stack & Automatización",
        "message": "Hola Abner, vimos tu portafolio y nos interesa coordinar una reunión para el desarrollo de una plataforma web y automatización de procesos.",
        "source": "Formulario de Contacto Web"
    }
    
    response = client.post('/api/send-message', json=test_payload)
    print(f"HTTP Status: {response.status_code}")
    json_data = response.get_json()
    print(f"Response JSON: {json_data}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert json_data.get("ok") is True, f"Expected ok: True"
    
    # Wait 3 seconds for async SMTP thread to complete
    time.sleep(3)
    
    print(">>> 3. Verifying database entry...")
    c.execute("SELECT id, name, email, company, service, message, source, timestamp FROM messages ORDER BY id DESC LIMIT 1")
    latest = c.fetchone()
    print(f"Latest record in DB:")
    print(f"  ID: {latest[0]}")
    print(f"  Name: {latest[1]}")
    print(f"  Email: {latest[2]}")
    print(f"  Company: {latest[3]}")
    print(f"  Service: {latest[4]}")
    print(f"  Message: {latest[5]}")
    print(f"  Source: {latest[6]}")
    print(f"  Timestamp: {latest[7]}")
    
    assert latest[1] == test_payload["name"]
    assert latest[2] == test_payload["email"]
    assert latest[3] == test_payload["company"]
    assert latest[4] == test_payload["service"]
    assert latest[6] == test_payload["source"]
    
    print("\n>>> 4. Testing Spam Honeypot...")
    spam_payload = {
        "name": "Spam Bot",
        "email": "bot@spam.com",
        "message": "Buy crypto now",
        "tel": "555-123456"  # honeypot filled
    }
    spam_res = client.post('/api/send-message', json=spam_payload)
    print(f"Spam Honeypot Status: {spam_res.status_code}, Response: {spam_res.get_json()}")
    assert spam_res.status_code == 200
    
    # Verify spam bot was NOT saved in DB
    c.execute("SELECT count(*) FROM messages WHERE name='Spam Bot'")
    spam_count = c.fetchone()[0]
    assert spam_count == 0, "Spam bot should not be saved in DB"
    print("Spam correctly ignored and not saved to DB!")
    
    print("\n>>> 5. Testing Static Page Routes...")
    for route in ['/', '/contact', '/contact.html', '/about', '/about.html', '/work', '/work.html', '/archive', '/archive.html', '/index', '/index.html']:
        res = client.get(route)
        print(f"GET {route.ljust(15)} -> HTTP {res.status_code}")
        assert res.status_code == 200, f"Route {route} returned status {res.status_code}"
        
    print("\n ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_full_flow()

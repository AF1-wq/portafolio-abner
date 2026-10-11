import os
import sqlite3
import sys

def main():
    try:
        # Ruta relativa al proyecto (antes estaba hardcodeada una ruta personal del equipo)
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'messages.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, message, timestamp FROM messages ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Timestamp: {row[4]}")
            print(f"Message: {row[3][:50]}...")
            print("-" * 20)
        if not rows:
            print("No messages found in DB.")
    except Exception as e:
        print(f"Error reading DB: {e}")

if __name__ == "__main__":
    main()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

smtp_user = os.environ.get("MAIL_USERNAME")
smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")

print(f"User: {smtp_user}")
# [SEGURIDAD] Nunca imprimir la contraseña (queda en historial de terminal / logs de CI)
print(f"Password configurada: {'sí' if smtp_password else 'no'}")

try:
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = smtp_user
    msg['Subject'] = f"Test message"
    
    cuerpo = f"Test body"
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    import ssl
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
    # [SEGURIDAD] set_debuglevel(1) volcaba el diálogo SMTP (incluido AUTH en base64) en consola
    server.starttls(context=ssl.create_default_context())
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

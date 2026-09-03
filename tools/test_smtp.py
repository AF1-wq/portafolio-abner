import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

smtp_user = os.environ.get("MAIL_USERNAME")
smtp_password = os.environ.get("MAIL_PASSWORD", "").replace(" ", "")

print(f"User: {smtp_user}")
print(f"Password: {smtp_password}")

try:
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = smtp_user
    msg['Subject'] = f"Test message"
    
    cuerpo = f"Test body"
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()
    print("Success")
except Exception as e:
    print(f"Error: {e}")

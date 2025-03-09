import smtplib
import random
from email.message import EmailMessage
from flask import session, current_app

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp  

    msg = EmailMessage()
    msg.set_content(f"Tu código de verificación es: {otp}")
    msg['Subject'] = 'Código de verificación'
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False
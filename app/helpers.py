from flask_mail import Message
from flask import flash
from app import app, mail, logging, apm

def send_async_email(app, msg):
    try:
        with app.app_context():
            mail.send(msg)
    except Exception as e:
       app.log_exception(e)
       pass

def send_email(subject, sender, recipients, text_body, html_body): 
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

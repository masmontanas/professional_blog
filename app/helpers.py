from flask_mail import Message
from flask import flash
from app import app, mail, logging, apm
import json
from collections import namedtuple
from threading import Thread

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

# def subscribe_user(email, client):
    
#     try:
#         client.lists.members.create(app.config['MAILCHIMP_LIST_ID'], {'email_address': email, 'status': 'subscribed'})
#         flash('Thank you for subscribing!')
#         app.logger.info('{} successfully subscribed to {}'.format(email,app.config['MAILCHIMP_LIST_ID']))

#     except Exception as e:
#         e = str(e)
#         e = e.replace("'",'"')
#         error = json.loads(e, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
#         app.log_exception('Failed to subscribe email <{}> with error < {} >'.format(email,error.detail))
#         flash(u'Error: {}'.format(error.title), 'error')


# def subscribe_commentor(email, client):
#     try:
#         client.lists.members.create(app.config['MAILCHIMP_COMMENTOR_LIST_ID'], {'email_address': email, 'status': 'subscribed'})
#         app.logger.info('{} successfully subscribed to {}'.format(email,app.config['MAILCHIMP_COMMENTOR_LIST_ID']))
    
#     except Exception as e:
#         e = str(e)
#         e = e.replace("'",'"')
#         error = json.loads(e, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
#         app.log_exception('Failed to subscribe email <{}> with error < {} >'.format(email,error.detail))

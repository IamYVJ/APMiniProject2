from flask import render_template
from app import app
from flask_mail import Message
from app import mail
from threading import Thread

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email_pass, args=(app, msg)).start()
    # mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[QuadCore.com] Reset Your Password',
               sender="systems.quadcore@gmail.com",
               recipients=[user.email],
               text_body=render_template('emailPasswordReset/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('emailPasswordReset/reset_password.html',
                                         user=user, token=token))

def send_async_email_pass(app, msg):
    with app.app_context():
        mail.send(msg)

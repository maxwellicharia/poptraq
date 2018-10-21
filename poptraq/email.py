from threading import Thread
from flask_mail import Message
from poptraq import app, mail


def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=app.config['MAIL_DEFAULT_SENDER'])
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()
    return thr


def send_async_email(msg):
    with app.app_context():
        print('====> Sending Email - Async')
        mail.send(msg)

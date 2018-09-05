""" Mail module to send mails using flask_mail"""

from flask import request, session, url_for
from flask_mail import Mail, Message
from main.models import Emails, db

__author__ = 'hughson.simon@gmail.com'

mail = Mail()


def send_email(subject, recipients, message, cc=[], bcc=[], attachment_filename=None,
               attachment_content_type='application/octet-stream', attachment_data=None):
    if not recipients and cc:
        recipients = cc
        cc = []
    msg = Message(body=message, subject=subject, recipients=recipients, cc=cc, bcc=bcc)
    if attachment_data:
        msg.attach(attachment_filename, attachment_content_type, attachment_data)
    mail.send(msg)


def user_register_email(user, password):
    """User registration mail along with aut generated password.

    :param user: This is user DB obeject
    :param password: random auto generated password
    :return: True
    """
    email_records = Emails.query.filter_by(email_slug="register").first()
    print(email_records.email_subject)
    message = email_records.email_message
    message = message.replace("<-FIRSTNAME->", user.first_name)
    message = message.replace("<-LASTNAME->", user.last_name)
    message = message.replace("<-PASSWORD->", password)
    try:
        send_email(email_records.email_subject, [user.email], message)
    except:
        db.session.rollback()
        raise

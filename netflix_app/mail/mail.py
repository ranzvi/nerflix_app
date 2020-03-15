import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def load_settings():
    to_emails = list(os.environ['EMAILS'].split(' '))
    sender_email = str(os.environ['GOOGLE_USER'])
    password = str(os.environ['GOOGLE_PASSWORD'])

    return sender_email, to_emails, password


def _create_message(subject, sender_email, to_emails):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ','.join(to_emails)

    return message


def create_message(subject, sender_email, to_emails, html_data):
    blank_message = _create_message(subject, sender_email, to_emails)
    part1 = MIMEText(html_data, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    blank_message.attach(part1)
    return blank_message


def _open_connection_and_send_email(sender_email, to_email, password, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, to_email, message.as_string()
        )


def send_email(subject, body):
    sender_email, to_emails, password = load_settings()
    message = create_message(subject, sender_email, to_emails, body)
    _open_connection_and_send_email(sender_email, to_emails, password, message)

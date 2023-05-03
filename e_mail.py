import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from core.config import settings
from sendgrid.helpers.mail import (From, To, PlainTextContent, HtmlContent)


def send_email(to_email, subject, body):
    message = Mail(
        from_email=From('kuzik94vadim@gmail.com'),
        to_emails=To(to_email),
        subject=subject,
        plain_text_content=PlainTextContent(body))
    try:
        mail_json = message.get()
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(mail_json)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from decouple import config
from core.config import settings
from sendgrid.helpers.mail import (From, To, PlainTextContent, HtmlContent)
from services.user_service import UserService
from core.security import get_password
from schemas.user_schema import UserUpdate


async def send_email(to_email, subject, body):
    print('start func')
    if (await UserService.get_user_by_email(to_email)):
        print('true after if statement')
        message = Mail(
            from_email=From('kuzik94vadim@gmail.com'),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=PlainTextContent(body))
            
        try:
            mail_json = message.get()
            print(mail_json)
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(mail_json)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            user_id = await UserService.get_user_by_email(to_email)
            await UserService.update_user(id=user_id.user_id, data=UserUpdate(email=to_email, hashed_password=body))
        except Exception as e:
            print(e)



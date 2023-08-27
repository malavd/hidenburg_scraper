from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from_email = os.environ.get('MY_EMAIL')
sendgrid_key = os.environ.get('SENDGRID_KEY')

recipient_email = None
with open('email_recipients.txt', 'r') as f:
    recipient_email = f.read()
    recipient_email = recipient_email.split('\n')

def send_email(subject: str, html_content: str, recipient_email:list = recipient_email) -> str:
    for email in recipient_email:
        message = Mail(
            from_email = from_email,
            to_emails = email,
            subject = subject,
            html_content = html_content
        )
        try:
            sg = SendGridAPIClient(sendgrid_key)
            response = sg.send(message)
            print(response.status_code)
            #print(response.body)
            #print(response.headers)
        except Exception as e:
            print(e.message)


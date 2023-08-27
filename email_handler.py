from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from_email = os.environ.get('MY_EMAIL')
sendgrid_key = os.environ.get('SENDGRID_KEY')

recipient_email = None
# read the default email list
with open('email_recipients.txt', 'r') as f:
    recipient_email = f.read()
    recipient_email = recipient_email.split('\n')

def send_email(subject: str, html_content: str, recipient_email:list = recipient_email) -> str:

    if type(recipient_email) is str:
        tmp_list = list()
        tmp_list.append(recipient_email)
        recipient_email = tmp_list

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
            print(response.status_code, 'email sent with subject:', subject)
            #print(response.body)
            #print(response.headers)
        except Exception as e:
            print('An error occured in sending email with subject: ', subject)
            print(e)
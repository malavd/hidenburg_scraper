from twilio.rest import Client
import os

account_sid = 'xyz'
auth_token = 'xyz'
client = Client(account_sid, auth_token)   # Create a Twilio client

# read the default email list
with open('whatsapp_receivers.txt', 'r') as file_receiver:
    whatsapp_rec = file_receiver.read()
    whatsapp_rec = whatsapp_rec.split('\n')


# Send a WhatsApp message
def send_whatsapp_message(to_numbers, message):
    for to_number in to_numbers:
        message = client.messages.create(
            to=f'whatsapp:{to_number}',
            from_='whatsapp:+14155238886',
            body=message
        )
        print("Message sent to", to_number, "with SID:", message.sid)

# List of predefined recipients' WhatsApp numbers
recipients = ['whatsapp:+1234567890', 'whatsapp:+9876543210']

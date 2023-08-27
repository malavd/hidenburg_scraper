import email_handler
import supabase_handler

welcome_email_html = None

def update_welcome_email_flag(email, welcome_flag = 1):
    set_welcome_email_flag = {'welcome_email_flag': welcome_flag}
    supabase_handler.update_email_recipient(email=email, json_data=set_welcome_email_flag)

def welcome_email_checker_sender():
    email_subject = 'Welcome to Vishal\'s web scraper for Hindenburg'
    # read welcome email template
    with open('email_templates/welcome_email.html', 'r') as f:
        welcome_email_html = f.read()

    # Get all email recipients in the DB
    email_recipients = supabase_handler.get_email_recipients()
    # Send welcome email to recipients who haven't received one yet
    for email_dict in email_recipients:
        if email_dict['subscribed'] == 1 and email_dict['welcome_email_flag'] == 0:
            tmp_email = email_dict['email']
            tmp_first_name = email_dict['first_name']
            print(tmp_email, tmp_first_name)
            # send welcome email
            try:
                email_handler.send_email(subject=email_subject, html_content=welcome_email_html.format(FirstNameTemplate=tmp_first_name), recipient_email=tmp_email)
            except Exception as e:
                print('Exception in send email', e)
            # update email recipient's welcome flag to 1
            update_welcome_email_flag(email=tmp_email, welcome_flag=1)
        else:
            print('No new welcome emails to send')

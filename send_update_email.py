import email_handler
import supabase_handler


def send_email_update_all(new_post_title_list):
    update_email_html = None
    tmp_email = None
    new_post_title_str = '<ul>'
    email_subject = 'There\'s a new article on Hindenburg'
    # read welcome email template
    with open('email_templates/new_post_update_email.html', 'r') as f:
        update_email_html = f.read()

    # Get all email recipients in the DB
    email_recipients = supabase_handler.get_email_recipients()

    # Format the article list
    for idx, post in enumerate(new_post_title_list):
        new_post_title_str+='<li>'+post+'</li>'
        if idx == len(new_post_title_list):
            new_post_title_str+='</ul>'

    # Send update email to recipients who are subscribed
    for email_dict in email_recipients:
        tmp_email = email_dict['email']
        tmp_first_name = email_dict['first_name']
        if email_dict['subscribed'] == 1:
            print('Subscribed emails: ', tmp_email, tmp_first_name)
            # send the update email with new article info.
            try:
                email_handler.send_email(subject=email_subject, html_content=update_email_html.format(FirstNameTemplate=tmp_first_name, NewPostTitleListTemplate=new_post_title_str), recipient_email=tmp_email)
            except Exception as e:
                print('Exception in update email', e)
        else:
            print('Can\'t send email to '+tmp_email+' because they are unsubscribed.')

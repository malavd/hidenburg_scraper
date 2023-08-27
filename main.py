# This is a scraper for Hidenberg research

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle
import supabase_handler
import email_handler
import send_welcome_email
import send_update_email
import datetime

debug_flag = 0

script_start_datetime = datetime.datetime.now().strftime('%m-%d-%Y: %H:%M:%S')
print('Script has started')
print('Debug flag is set to: ', debug_flag)
page_url = 'https://hindenburgresearch.com'

def get_url_html(page_url=page_url):
    req = Request(url=page_url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read()

def save_to_pickle(var, var_name):
    with open(var_name+'.pkl', 'wb') as f:
        pickle.dump(var, f)

def read_from_pickle(var_name):
    with open(var_name+'.pkl', 'rb') as f:
        return pickle.load(f)

def read_html_pickle():
    # make an HTTP request
    #html = get_url_html(page_url)

    # save the request to a pickle file
    #save_to_pickle(html, 'hidenberg_page')

    # read HTML from the pickle file
    html_pkl = read_from_pickle('hidenberg_page')

    #print(html_pkl)

    #soup = BeautifulSoup(html_pkl, 'html.parser')
    #print(soup)
    return html_pkl

# get all articles in the SUPABASE DB
def get_supabase_post_list():
    query_result = supabase_handler.get_post_id()
    print('Query result: ', query_result)
    supabase_post_list = list()

    if query_result is not None and len(query_result) > 0:
        for q in query_result:
            print('This is the post ID in query results', q)
            supabase_post_list.append(q['post_id'])

    return supabase_post_list

'''
Tags that I'll need:

<h2 class="post-title">text</h2>
<time class="entry-date published" datetime="text"></time>
<time class="updated" datetime="text"></time>
'''

# def get_post_attributes():
#     title = soup.find_all("h2", class_="post-title")
#     entry_date = soup.find_all("time", class_="entry-date published")
#     update_date = soup.find_all("time", class_="updated")
#     return [title, entry_date, update_date]

# print(get_post_attributes()[0][1].text.strip())
# print(get_post_attributes()[1][1].attrs['datetime'])
# print(get_post_attributes()[2][1].attrs['datetime'])

'''
Parameters:
    soup: BeautifulSoup object with the parsed HTML
Output: 
    post_dict: A dictionary of posts with post_id as the key and post_title, entry_date, and update_date as nested keys
'''

def generate_post_attributes(soup):

    div_post_preview = soup.find_all('div', class_='post-preview')
    post_dict = dict()

    for tag in div_post_preview:
        post_id = tag.attrs['id']
        post_title = tag.text.strip()
        for t in tag.find_all('time'):
            
            if t.attrs['class'][0] == 'entry-date':
                entry_date = t.attrs['datetime']
            if t.attrs['class'][0] == 'updated':
                update_date = t.attrs['datetime']
            
        #print(post_id, post_title, entry_date, update_date)
        post_dict[post_id] = {
            'post_title': post_title, 'entry_date': entry_date, 'update_date': update_date
            }
    return post_dict
    #entry_date = tag.find_all('datetime', class_='entry-date published')
    
    #print('===========>', title)
    #rint(entry_date)

def notify_users_email(new_post_title_list):
    print('Sending email to the receipients....')        
    send_update_email.send_email_update_all(new_post_title_list)
    print('Email sent to the recipients!')
    return None

if __name__ == "__main__":
    if debug_flag == 1:
        print('DEBUG mode is on. Reading from Pickle...')
        html_pkl = read_html_pickle()
        soup = BeautifulSoup(html_pkl, 'html.parser')
    else:
        html_resp = get_url_html()
        print('Length of the HTML response: ', len(html_resp))
        soup = BeautifulSoup(html_resp, 'html.parser')

    article_dict = generate_post_attributes(soup)

    supabase_post_list = get_supabase_post_list()
    
    # Send welcome emails to users who are new
    send_welcome_email.welcome_email_checker_sender()

    print('This is the list of articles in the DB:', supabase_post_list)

    new_post_title_list = list()
    ## check if the article scraped already exists in the database
    for post_id in article_dict.keys():
        if post_id in supabase_post_list:
            # post already exists, do nothing.
            print('post-id already exists')
        else:
            # post doesn't exist in SUPABASE. Update and send notification
           print('There is a new post ID!', post_id)
           post_id_data = article_dict[post_id]
           # append to the list of new post titles
           new_post_title_list.append(post_id_data['post_title'])
           # Update the DB with new posts
           supabase_handler.update_articles_post(post_id = post_id,
                                                 post_title=post_id_data['post_title'],
                                                 entry_date=post_id_data['entry_date'],
                                                 update_date=post_id_data['update_date'])
    
    print('New post title list: ', new_post_title_list)
    if len(new_post_title_list) > 0:
        # If there are new posts, notify users
        notify_users_email(new_post_title_list)
           
    print('Updating the run datetime in DB')
    supabase_handler.update_run()
    # send the daily update email to the default email
    email_handler.send_email('Daily scraper operational update', 'Hidenburg scraper was run today at {script_start_datetime}'.format(script_start_datetime=script_start_datetime))
    print('Script finished')

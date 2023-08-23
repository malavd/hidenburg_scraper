# This is a scraper for Hidenberg research

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle
import supabase_handler

debug_flag = 1
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
    supabase_post_list = list()

    for q in query_result:
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
    
if __name__ == "__main__": 

    if debug_flag == 1:
        html_pkl = read_html_pickle()
        soup = BeautifulSoup(html_pkl, 'html.parser')
    else:
        html_resp = get_url_html()
        soup = BeautifulSoup(html_resp, 'html.parser')

    article_dict = generate_post_attributes(soup)

    supabase_post_list = get_supabase_post_list()

    print(supabase_post_list)

    ## check if the article scraped already exists in the database
    for post_id in article_dict.keys():
        print(post_id)
        if post_id in supabase_post_list:
            # post already exists, do nothing.
            print('post-id already exists')
        else:
            # post doesn't exist in SUPABASE. Update and send notification
           post_id_data = article_dict[post_id]
           supabase_handler.update_articles_post(post_id = post_id,
                                                 post_title=post_id_data['post_title'],
                                                 entry_date=post_id_data['entry_date'],
                                                 update_date=post_id_data['update_date'])
           
    
    supabase_handler.update_run()
    
    #print(article_dict.keys())

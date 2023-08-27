import os
import requests
import datetime

articles_endpoint = 'https://yjntbfaqnrkgwwbxtwyi.supabase.co/rest/v1/articles'
runs_endpoint = 'https://yjntbfaqnrkgwwbxtwyi.supabase.co/rest/v1/runs'
email_recipients_endpoint = 'https://yjntbfaqnrkgwwbxtwyi.supabase.co/rest/v1/email_recipients'

datetime_now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def get_key():
    key = os.getenv('SUPABASE_KEY')
    return key

def get_headers():
    headers = {
    'apikey': os.getenv('SUPABASE_KEY', ''),
    'Authorization': 'Bearer ' + os.getenv('SUPABASE_KEY', ''),
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal',
    }
    return headers

def update_run():
    headers = get_headers()
    
    json_data = {
    'dummy': 1,
    }

    resp = requests.post(runs_endpoint, headers=headers, json=json_data)
    return None

def update_articles_post(**post_dict):
    headers = get_headers()
    json_data = post_dict
    requests.post(articles_endpoint, headers=headers, json=json_data)
    return None

def get_post_id(post_id=''):
    headers = get_headers()
    query = ''
    if post_id != '':
        query = '?post_id=eq.'+post_id
    # params = {
    # 'post_id': 'post-123'
    # }

    response = requests.get(articles_endpoint+query, headers=headers)
    #print(response.status_code)
    if response.status_code == 200 and response.text != '[]':
        return response.json()
    else:
        return None

def get_email_recipients():
    headers = get_headers()
    response = requests.get(email_recipients_endpoint, headers=headers)
    return response.json()

def update_email_recipient(email, json_data):
    headers = get_headers()
    query = '?email=eq.'+email
    resp = requests.patch(email_recipients_endpoint+query, headers=headers, json=json_data)
    return resp

# print(get_post_id('post-123'))0
# print(get_post_id())
# print(update_run())
#update_articles_post(post_id = 'post-123455', post_title = 'test title 5', entry_date = datetime_now, update_date = datetime_now)
#print(get_email_recipients())
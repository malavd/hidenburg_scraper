import os
import requests
import datetime

articles_endpoint = 'https://yjntbfaqnrkgwwbxtwyi.supabase.co/rest/v1/articles'
runs_endpoint = 'https://yjntbfaqnrkgwwbxtwyi.supabase.co/rest/v1/runs'
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


# print(get_post_id('post-123'))
# print(get_post_id())
# print(update_run())
#update_articles_post(post_id = 'post-123455', post_title = 'test title 5', entry_date = datetime_now, update_date = datetime_now)
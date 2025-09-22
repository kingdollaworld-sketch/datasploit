#!/usr/bin/env python

try:
    from ..core.style import style
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style

import os
import requests
import sys
import urllib.request, urllib.parse, urllib.error

from termcolor import colored
from bs4 import BeautifulSoup

# Control whether the module is enabled or not
ENABLED = True
MODULE_NAME = "Username Tinder"
REQUIRES = ()

def banner():
    return f"Running {MODULE_NAME}"

def fetch_content(username):
    r = requests.get('https://gotinder.com/@{}'.format(username))
    content = BeautifulSoup(r.text, 'html.parser')
    return content

def check_useranme_exists(content):
    if content.find(id='card-container'):
        return True
    else:
        return False

def parse_page(content):
    name = content.find(id='name')
    age = content.find(id='age')
    photo = content.find(id='user-photo')
    teaser = content.find(id='teaser')
    userinfo = {
        'name': name.get_text(strip=True) if name else '',
        'age': age.get_text().strip(',\xa0') if age else '',
        'picture': photo.get('src') if photo else '',
        'teaser': teaser.get_text(strip=True) if teaser else '',
    }
    return userinfo

def download_photo(username, url):
    file_path = str('profile_pic/{}'.format(username))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    path = file_path + "/tinder." + url.split('.')[-1]
    urllib.request.urlretrieve(url, path)

def main(username):
    userinfo = {}
    content = fetch_content(username)
    if check_useranme_exists(content):
        userinfo = parse_page(content)
        download_photo(username, str(content.find(id='user-photo').get('src')))
    return userinfo

def output(data, username=""):
    if len(data) == 0:
        print('username not found')
    else:
        for k, v in data.items():
            print('{k}: {v}'.format(k=k.capitalize(), v=v))

if __name__ == "__main__":
    #try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    #except Exception as e:
    #    print(e)
    #    print("Please provide a username as argument")

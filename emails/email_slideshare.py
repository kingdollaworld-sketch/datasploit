#!/usr/bin/env python

try:
    from ..core.style import style
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style

import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True
MODULE_NAME = "Email Slideshare"
REQUIRES = ()

def banner():
    return f"Running {MODULE_NAME}"

def main(email):
    req = requests.get('http://www.slideshare.net/search/slideshow?q=%s' % email)
    soup = BeautifulSoup(req.text, "lxml")
    atag = soup.findAll('a', {'class': 'title title-link antialiased j-slideshow-title'})
    slides = {}
    for at in atag:
        slides[at.text] = at['href']
    return slides

def output(data, email=""):
    if data:
        print("Found %s published slides\n" % len(data))
        for tl, lnk in data.items():
            print(str(tl).strip() + " : http://www.slideshare.net" + str(lnk).strip())
    else:
        print(colored('[-] No Associated Slides found.', 'red'))

if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")

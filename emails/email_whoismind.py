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
MODULE_NAME = "Email Whoismind"
REQUIRES = ()

def banner():
    return f"Running {MODULE_NAME}"

def main(email):
    req = requests.get('http://www.whoismind.com/email/%s.html' % email)
    soup = BeautifulSoup(req.text, "lxml")
    atag = soup.findAll('a')
    domains = []
    for at in atag:
        if 'href' in at and at.text in at['href']:
            domains.append(at.text)
    domains = list(set(domains))
    return domains

def output(data, email=""):
    if len(data) == 0:
        print(colored("[-] No domains found", 'red'))
    else:
        for domain in data:
            if domain:
                print(domain)

if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")

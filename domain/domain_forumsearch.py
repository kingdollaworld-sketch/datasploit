#!/usr/bin/env python

try:
    from ..core.style import style
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style

import requests
from bs4 import BeautifulSoup
import sys
import re
from termcolor import colored
import time

ENABLED = True
MODULE_NAME = "Domain Forum Search"
REQUIRES = ()

def boardsearch_forumsearch(domain):
    time.sleep(0.3)
    req = requests.get(
        'http://boardreader.com/index.php?a=l&q=%s&d=0&extended_search=1&q1=%s&ltype=all&p=50' % (domain, domain))
    soup = BeautifulSoup(req.text, "lxml")
    text = soup.findAll('bdo', {"dir": "ltr"})
    links = {}
    for lk in text:
        links[lk.text] = re.search("'(.+?)'", lk.parent['onmouseover']).group(1)
    return links

def banner():
    return f"Running {MODULE_NAME}"

def main(domain):
    return boardsearch_forumsearch(domain)

def output(data, domain=""):
    print("[+] Associated Forum Links\n")
    for tl, lnk in data.items():
        print("%s (%s)" % (lnk, tl))
    print("\n-----------------------------\n")

if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")

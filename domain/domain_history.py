#!/usr/bin/env python

try:
    from ..core.style import style
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style

import sys
import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
import time

ENABLED = True
MODULE_NAME = "Domain History"
REQUIRES = ()

def netcraft_domain_history(domain):
    ip_history_dict = {}
    time.sleep(0.3)
    endpoint = "http://toolbar.netcraft.com/site_report?url=%s" % domain
    req = requests.get(endpoint)

    soup = BeautifulSoup(req.text, 'html.parser')
    urls_parsed = soup.findAll('a', href=re.compile(r'.*netblock\?q.*'))
    for url in urls_parsed:
        if urls_parsed.index(url) != 0:
            ip_history_dict[str(url).split('=')[2].split(">")[1].split("<")[0]] = str(url.parent.findNext('td')).strip(
                "<td>").strip("</td>")
    return ip_history_dict

def banner():
    return f"Running {MODULE_NAME}"

def main(domain):
    return netcraft_domain_history(domain)

def output(data, domain=""):
    for x in data.keys():
        print("%s: %s" % (data[x], x))
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

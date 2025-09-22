#!/usr/bin/env python

try:
    from ..core.style import style
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style

import sys
import whois
from termcolor import colored
import time

ENABLED = True
MODULE_NAME = "Domain Whois"
REQUIRES = ()

def whoisnew(domain):
    try:
        w = whois.whois(domain)
        return dict(w)
    except Exception:
        return {}

def banner():
    return f"Running {MODULE_NAME}"

def main(domain):
    return whoisnew(domain)

def output(data, domain=""):
    for k in ('creation_date', 'expiration_date', 'updated_date'):
        if k in data:
            date = data[k][0] if isinstance(data[k], list) else data[k]
            if data[k]:
                data[k] = date.strftime('%m/%d/%Y')
    print(data)
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

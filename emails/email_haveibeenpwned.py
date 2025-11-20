#!/usr/bin/env python

try:
    from ..core.style import style
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style

import sys
import requests
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True
MODULE_NAME = "Email HaveIBeenPwned"
REQUIRES = ()

def banner():
    return f"Running {MODULE_NAME}"

def main(email):
    req = requests.get(
        "https://haveibeenpwned.com/api/v2/breachedaccount/%s" % email,
        headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"}
    )
    if req.status_code == 404:
        return {}
    if 'Attention Required! | CloudFlare' in req.text:
        print("CloudFlare detected")
        return {}
    if req.text.strip():
        try:
            return req.json()
        except ValueError:
            return {}
    return {}

def output(data, email=""):
    if data:
        print(colored("Pwned at %s Instances\n" % len(data), 'green'))
        for x in data:
            print("Title: %s\nBreachDate: %s\nPwnCount: %s\nDescription: %s\nDataClasses: %s\n" % (
                x.get('Title', ''),
                x.get('BreachDate', ''),
                x.get('PwnCount', ''),
                x.get('Description', ''),
                ", ".join(x.get('DataClasses', []))
            ))
    else:
        print(colored("[-] No breach status found.", 'red'))

if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")

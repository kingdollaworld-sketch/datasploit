#!/usr/bin/env python

try:
    from ..core.style import style
    from ..core.config import get_config_value
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style
    from core.config import get_config_value

import requests
import sys
import time
from termcolor import colored

ENABLED = True
WRITE_TEXT_FILE = True
MODULE_NAME = "Domain Email Hunter"
REQUIRES = ("emailhunter",)

def emailhunter(domain):
    collected_emails = []
    time.sleep(0.3)
    emailhunter_api = get_config_value('emailhunter')
    url = "https://api.emailhunter.co/v1/search?api_key=%s&domain=%s" % (emailhunter_api, domain)
    res = requests.get(url)
    try:
        parsed = res.json()
    except ValueError:
        print('CAPTCHA has been implemented, skipping this for now.')
        return collected_emails

    if 'emails' in parsed:
        for email in parsed['emails']:
            collected_emails.append(email['value'])
    elif parsed.get('status') == "error":
        print(colored(style.BOLD + '[-] %s\n' % parsed.get('message') + style.END, 'red'))
    return collected_emails

def banner():
    return f"Running {MODULE_NAME}"

def main(domain):
    if get_config_value('emailhunter') is not None:
        return emailhunter(domain)
    else:
        return [False, "INVALID_API"]

def output(data, domain=""):
    if isinstance(data, list) and len(data) == 2 and data[1] == "INVALID_API":
        print(colored(style.BOLD + '\n[-] Emailhunter API key not configured, skipping Email Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        for x in data:
            print(str(x))

def output_text(data):
    return "\n".join(data)

if __name__ == "__main__":
        domain = sys.argv[1]
        banner()
        result = main(domain)
        if result:
            output(result, domain)

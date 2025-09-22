#!/usr/bin/env python

try:
    from ..core.style import style
    from ..core.config import get_config_value
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style
    from core.config import get_config_value

import requests
import sys
from termcolor import colored
import time

ENABLED = True
MODULE_NAME = "Domain Shodan"
REQUIRES = ("shodan_api",)

def shodandomainsearch(domain):
    time.sleep(0.3)
    endpoint = "https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}" % (
    get_config_value('shodan_api'), domain)
    req = requests.get(endpoint)
    try:
        return req.json()
    except ValueError:
        return {}

def banner():
    return f"Running {MODULE_NAME}"

def main(domain):
    if get_config_value('shodan_api') is not None:
        return shodandomainsearch(domain)
    else:
        return [False, "INVALID_API"]

def output(data, domain=""):
    if isinstance(data, list) and len(data) == 2 and data[1] == "INVALID_API":
        print(colored(style.BOLD + '\n[-] Shodan API Key not configured. Skipping Shodan search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        if 'matches' in data:
            for x in data['matches']:
                print("IP: %s\nHosts: %s\nDomain: %s\nPort: %s\nData: %s\nLocation: %s\n" % (
                    x.get('ip_str', ''),
                    x.get('hostnames', []),
                    x.get('domains', []),
                    x.get('port', ''),
                    x.get('data', '').replace("\n", ""),
                    x.get('location', {})
                ))
        print("-----------------------------\n")

if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")

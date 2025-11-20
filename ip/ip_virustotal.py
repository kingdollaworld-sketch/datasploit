#!/usr/bin/env python

try:
    from ..core.style import style
    from ..core.config import get_config_value
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style
    from core.config import get_config_value

import sys
import requests
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True
MODULE_NAME = "IP Virustotal"
REQUIRES = ("virustotal_public_api",)

def banner():
    return f"Running {MODULE_NAME}"

def main(ip):
    api_key = get_config_value('virustotal_public_api')
    if api_key is None:
        return [False, "INVALID_API"]

    params = {'ip': ip, 'apikey': api_key}
    url = "https://www.virustotal.com/vtapi/v2/ip-address/report"
    response = requests.get(url, params=params)
    try:
        return response.json()
    except ValueError:
        return {}

def output(data, ip=""):
    if isinstance(data, list) and data[1] == "INVALID_API":
        print(colored(style.BOLD + '\n[-] VirusTotal API Key not configured. Skipping VirusTotal Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
        return

    if not data:
        print("[-] No data returned from VirusTotal.")
        return

    for key, value in data.items():
        print(f"{key}: {value}")
    print("")

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        banner()
        result = main(ip)
        output(result, ip)
    except Exception as e:
        print(e)
        print("Please provide an IP Address as argument")

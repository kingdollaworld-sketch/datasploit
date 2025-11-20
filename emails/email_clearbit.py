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
MODULE_NAME = "Email Clearbit"
REQUIRES = ("clearbit_apikey",)

def banner():
    return f"Running {MODULE_NAME}"

def main(email):
    clearbit_apikey = get_config_value('clearbit_apikey')
    if clearbit_apikey is not None:
        headers = {"Authorization": "Bearer %s" % clearbit_apikey}
        req = requests.get("https://person.clearbit.com/v1/people/email/%s" % (email), headers=headers)
        try:
            person_details = req.json()
        except ValueError:
            return {}

        if isinstance(person_details, dict) and person_details.get("error") == "queued":
            print("This might take some more time, Please run this script again, after 5 minutes.")
        else:
            return person_details
    else:
        return [False, "INVALID_API"]

def output(data, email=""):
    print(data)
    if isinstance(data, list) and data[1] == "INVALID_API":
        print(colored(style.BOLD + '\n[-] Clearbit API Key not configured. Skipping Clearbit Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        for x in data.keys():
            print('%s details:' % x)
            if isinstance(data[x], dict):
                for y in data[x].keys():
                    if data[x][y] is not None:
                        print("%s:  %s" % (y, data[x][y]))
            elif data[x] is not None:
                print("\n%s:  %s" % (x, data[x]))

        print("\n-----------------------------\n")

if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")

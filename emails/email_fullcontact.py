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

ENABLED = True
MODULE_NAME = "Email Fullcontact"
REQUIRES = ("fullcontact_api",)

def banner():
    return f"Running {MODULE_NAME}"

def main(email):
    fullcontact_api = get_config_value('fullcontact_api')
    if fullcontact_api is None:
        return [False, "INVALID_API"]

    req = requests.get(
        "https://api.fullcontact.com/v2/person.json",
        params={'email': email},
        headers={"X-FullContact-APIKey": fullcontact_api}
    )
    try:
        return req.json()
    except ValueError:
        return {}

def output(data, email=""):
    if isinstance(data, list) and data[1] == "INVALID_API":
        print(colored(style.BOLD + '\n[-] Full-Contact API Key not configured. Skipping Fullcontact Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
        return

    if data.get("status") != 200:
        print('Error Occured - Encountered Status Code: %s. Please check if Email_id exist or not?' % data.get("status", ""))
        return

    contact_info = data.get("contactInfo", {}) or {}
    if contact_info:
        print("Name: %s" % contact_info.get('fullName', ''))

    print("\nOrganizations:")
    for org in data.get("organizations", []) or []:
        primary = " - Primary" if org.get('isPrimary') else ""
        title = org.get('title', '')
        name = org.get('name', '')
        start = org.get('startDate', '')
        end = org.get('endDate', '') or 'Unknown Date'
        if title:
            print("\t%s at %s - (From %s to %s)%s" % (title, name, start, end, primary))
        else:
            print("\t%s - (From %s to %s)%s" % (name, start, end, primary))

    websites = contact_info.get('websites', []) or []
    if websites:
        print("\nWebsite(s):")
        for site in websites:
            print("\t%s" % site.get('url', ''))

    chats = contact_info.get('chats', []) or []
    if chats:
        print('\nChat Accounts')
        for chat in chats:
            print("\t%s on %s" % (chat.get('handle', ''), chat.get('client', '')))

    print("\nSocial Profiles:")
    for profile in data.get("socialProfiles", []) or []:
        print("\t%s:" % profile.get('type', '').upper())
        for key, value in profile.items():
            if key not in ('type', 'typeName', 'typeId'):
                print('\t%s: %s' % (key, value))
        print('')

    print("Other Details:")
    demographics = data.get("demographics", {}) or {}
    if demographics:
        print("\tGender: %s" % demographics.get('gender', ''))
        print("\tCountry: %s" % demographics.get('country', ''))
        print("\tTentative City: %s" % demographics.get('locationGeneral', ''))

    print("Photos:")
    for photo in data.get("photos", []) or []:
        print("\t%s: %s" % (photo.get('typeName', ''), photo.get('url', '')))

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

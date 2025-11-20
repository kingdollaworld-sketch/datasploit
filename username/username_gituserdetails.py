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
MODULE_NAME = "Username Git User Details"
REQUIRES = ()

def banner():
    return f"Running {MODULE_NAME}"

def main(username):
    req = requests.get("https://api.github.com/users/%s" % username)
    return req.json()

def output(data, username=""):
    if "message" in data and data["message"] == "Not Found":
        print('Git account do not exist on this username.')
    else:
        print("Login: %s" % data['login'])
        print("avatar_url: %s" % data['avatar_url'])
        print("id: %s" % data['id'])
        print("Repos: %s" % data['repos_url'])
        print("Name: %s" % data['name'])
        print("Company: %s" % data['company'])
        print("Blog: %s" % data['blog'])
        print("Location: %s" % data['location'])
        print("Hireable: %s" % data['hireable'])
        print("Bio: %s" % data['bio'])
        print("On GitHub: %s" % data['created_at'])
        print("Last Activity: %s" % data['updated_at'])
        print("\n-----------------------------\n")

if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        print("Please provide a username as argument")

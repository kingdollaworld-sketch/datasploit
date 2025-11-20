#!/usr/bin/env python

try:
    from ..core.style import style
    from ..core.config import get_config_value
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style
    from core.config import get_config_value

import sys

# Control whether the module is enabled or not
ENABLED = True
MODULE_NAME = "Template"
REQUIRES = ()

def banner():
    return f"Running {MODULE_NAME}"

def main(username):
    # Use the username variable to do some stuff and return the data
    print(username)
    return []

def output(data, username=""):
    # Use the data variable to print(out to console as you like)
    for i in data:
        print(i)

if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        print("Please provide a username as argument")

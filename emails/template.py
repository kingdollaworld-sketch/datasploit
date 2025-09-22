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

def main(email):
    # Use the email variable to do some stuff and return the data
    print(email)
    return []

def output(data, email=""):
    # Use the data variable to print(out to console as you like)
    for i in data:
        print(i)

if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")

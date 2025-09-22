#!/usr/bin/env python

try:
    from ..core.style import style
    from ..core.config import get_config_value
except ImportError:  # pragma: no cover - legacy script execution
    from core.style import style
    from core.config import get_config_value

import re
import requests
import sys
from termcolor import colored

ENABLED = True
MODULE_NAME = "Domain Google Tracking"
REQUIRES = ("spyonweb_access_token",)

'''
Author: @khasmek

Original Idea: @jms_dot_py

Original article -
http://www.automatingosint.com/blog/2017/07/osint-website-connections-tracking-codes/

Original code -
https://github.com/automatingosint/osint_public/blob/master/trackingcodes/website_connections.py
'''

def banner():
    return f"Running {MODULE_NAME}"

def clean_tracking_code(tracking_code):
    if tracking_code.count("-") > 1:
        return tracking_code.rsplit("-", 1)[0]
    return tracking_code

def extract_tracking_codes(domain):
    seen_codes = set()
    connections = {}
    site = domain if domain.startswith(("http://", "https://")) else "http://" + domain
    try:
        response = requests.get(site)
    except requests.RequestException:
        connections['err'] = str(colored(style.BOLD + '\n[!] Failed to reach site.\n' + style.END, 'red'))
        return connections

    content = response.text
    google_adsense_pattern = re.compile(r"pub-[0-9]{1,}", re.IGNORECASE)
    google_analytics_pattern = re.compile(r"ua-\d+-\d+", re.IGNORECASE)

    extracted_codes = google_adsense_pattern.findall(content)
    extracted_codes.extend(google_analytics_pattern.findall(content))

    for code in extracted_codes:
        code = clean_tracking_code(code)
        normalized = code.lower()
        if normalized not in seen_codes:
            seen_codes.add(normalized)
            connections.setdefault(code, []).append(domain)

    return connections

def spyonweb_request(data, request_type="domain"):
    params = {'access_token': get_config_value('spyonweb_access_token')}
    response = requests.get(f'https://api.spyonweb.com/v1/{request_type}/{data}', params=params)
    if response.status_code == 200:
        result = response.json()
        if result.get('status') != "not_found":
            return result
    return None

def spyonweb_analytics_codes(connections):
    for code in list(connections.keys()):
        if code.lower().startswith("pub"):
            request_type = "adsense"
        elif code.lower().startswith("ua"):
            request_type = "analytics"
        else:
            continue

        results = spyonweb_request(code, request_type)
        if not results:
            continue

        if results.get('message') == 'request quota exceeded':
            connections[code].append('conn refused')
            continue

        items = results.get('result', {}).get(request_type, {}).get(code, {}).get('items', [])
        for domain in items:
            connections[code].append(domain)

    return connections

def main(domain):
    if get_config_value('spyonweb_access_token') is None:
        return [colored(style.BOLD + '[!] Error: No SpyOnWeb API token found. Skipping' + style.END, 'red')]

    connections = extract_tracking_codes(domain)
    if 'err' in connections:
        return [connections]

    if connections:
        tracking_codes = {'Tracking Codes': list(connections.keys())}
        dirty_domains = spyonweb_analytics_codes(connections)
        common_domains = {k: sorted(set(v)) for k, v in dirty_domains.items()}
        return [common_domains, tracking_codes]

    return [colored(style.BOLD + '\n[!] No tracking codes found!\n' + style.END, 'red')]

def output(data, domain=""):
    for item in data:
        if isinstance(item, dict):
            for key, value in item.items():
                if key == 'err':
                    print('\nERRORS:')
                    print(value)
                elif key == 'Tracking Codes':
                    print('\nTracking Codes:')
                    for code in value:
                        print('\t' + str(code))
                else:
                    entries = list(value)
                    if 'conn refused' in entries:
                        print(colored(style.BOLD + '\n[!] Error: Connection requests exceeded!\n' + style.END, 'red'))
                        entries = [entry for entry in entries if entry != 'conn refused']
                    print(f"{key}:")
                    for url in entries:
                        print('\t' + str(url))
        else:
            print(item)

if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")

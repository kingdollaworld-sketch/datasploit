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
MODULE_NAME = "IP Shodan"
REQUIRES = ("shodan_api",)

def banner():
    return f"Running {MODULE_NAME}"

def main(ip):
    shodan_api = get_config_value('shodan_api')
    if shodan_api is None:
        return [False, "INVALID_API"]
    endpoint = f"https://api.shodan.io/shodan/host/{ip}?key={shodan_api}"
    req = requests.get(endpoint)
    try:
        return req.json()
    except ValueError:
        return {}

def output(data, ip=""):
    if isinstance(data, list) and data[1] == "INVALID_API":
        print(colored(style.BOLD + '\n[-] Shodan API Key not configured. Skipping Shodan search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
        return

    if 'error' in data:
        print('No information available for that IP.')
        return

    asn = data.get('asn', '')
    print(colored(style.BOLD + '\n----------- Per Port Results -----------' + style.END, 'blue'))
    for entry in data.get('data', []):
        port = entry.get('port', 'unknown')
        print(colored(style.BOLD + '\nResponse from Open Port: %s' + style.END, 'green') % port)

        if 'title' in entry:
            print(colored(style.BOLD + '[+] HTML Content:\t' + style.END, 'green') + 'Yes (Please inspect manually on this port)')
        if 'http' in entry:
            print(colored(style.BOLD + '[+] HTTP port present:\t' + style.END, 'green'))
            http_info = entry['http']
            print('\tTitle: %s' % http_info.get('title'))
            print('\tRobots: %s' % http_info.get('robots'))
            print('\tServer: %s' % http_info.get('server'))
            print('\tComponents: %s' % http_info.get('components'))
            print('\tSitemap: %s' % http_info.get('sitemap'))
        if 'ssh' in entry:
            print(colored(style.BOLD + '[+] SSH port present:\t' + style.END, 'green'))
            ssh_info = entry['ssh']
            print('\tType: %s' % ssh_info.get('type'))
            print('\tCipher: %s' % ssh_info.get('cipher'))
            print('\tFingerprint: %s' % ssh_info.get('fingerprint'))
            print('\tMac: %s' % ssh_info.get('mac'))
            print('\tKey: %s' % ssh_info.get('key'))
        if 'ssl' in entry:
            print('\tSSL Versions: %s' % entry['ssl'].get('versions'))
        if 'asn' in entry and not asn:
            asn = entry.get('asn', '')
        if entry.get('opts') and 'vulns' in entry['opts']:
            for vuln in entry['opts']['vulns'].values():
                print(vuln)
        if 'product' in entry:
            print('Product: %s' % entry['product'])
        if 'version' in entry:
            print('Version: %s' % entry['version'])

    print(colored(style.BOLD + '\n----------- Basic Info -----------' + style.END, 'blue'))
    print('Open Ports: %s' % data.get('ports'))
    print('Latitude: %s' % data.get('latitude'))
    print('Hostnames: %s' % data.get('hostnames'))
    print('Postal Code: %s' % data.get('postal_code'))
    print('Country Code: %s' % data.get('country_code'))
    print('Organization: %s' % data.get('org'))
    if asn:
        print('ASN: %s' % asn)
    if 'vulns' in data:
        print(colored(style.BOLD + 'Vulnerabilties: %s' + style.END, 'red') % data['vulns'])
    print("")

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        banner()
        result = main(ip)
        if result:
            output(result, ip)
    except Exception as e:
        print(e)
        print("Please provide an IP Address as argument")

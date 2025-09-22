Writing custom modules/scripts for dataSploit
=============================================

dataSploit has been made with a modular approach in mind. We wanted to make things simple for even a novice user to understand. Thus, writing a new module is as simple as adding a new script to a module folder and that's it. dataSploit takes care of the rest. There are a few simple guidelines to follow when writing a new module/script. Please read the documentation below to get a better understanding of how dataSploit is structured.

Following is the tree structure of a basic git clone of the dataSploit repository:

```bash
datasploit/
├── active_default_file_check.py
├── active_scan.py
├── base.html
├── check_urls.txt
├── config.template.ini
├── contributors.txt
├── datasploit_config.py
├── datasploit.py
├── docs
│   ├── apiGeneration.md
│   ├── contributors.md
│   ├── home.md
│   ├── index.md
│   ├── setupGuide.md
│   └── Usage.md
├── domain
│   ├── domain_censys.py
│   ├── domain_checkpunkspider.py
│   ├── domain_dnsrecords.py
│   ├── domain_emailhunter.py
│   ├── domain_forumsearch.py
│   ├── domain_github.py
│   ├── domain_GooglePDF.py
│   ├── domain_history.py
│   ├── domain_pagelinks.py
│   ├── domain_pastes.py
│   ├── domain_shodan.py
│   ├── domain_subdomains.py
│   ├── domain_wappalyzer.py
│   ├── domain_whois.py
│   ├── domain_wikileaks.py
│   ├── domain_zoomeye.py
│   ├── __init__.py
│   └── template.py
├── emails
│   ├── email_basic_checks.py
│   ├── email_clearbit.py
│   ├── email_fullcontact.py
│   ├── email_haveibeenpwned.py
│   ├── email_pastes.py
│   ├── email_scribd.py
│   ├── email_slideshare.py
│   ├── email_whoismind.py
│   ├── __init__.py
│   └── template.py
├── __init__.py
├── ip
│   ├── __init__.py
│   ├── ip_shodan.py
│   ├── ip_virustotal.py
│   ├── ip_whois.py
│   └── template.py
├── LICENSE
├── mkdocs.yml
├── osint_runner.py
├── README.md
├── reports
│   └── README
├── requirements.txt
├── roadmap.txt
├── username
│   ├── __init__.py
│   ├── template.py
│   ├── username_gitscrape.py
│   ├── username_gituserdetails.py
│   ├── username_keybase.py
│   ├── username_profilepic.py
│   ├── username_twitterdetails.py
│   └── username_usernamesearch.py
└── usernameOsint.py
```

Out of the box, 4 main modules have been provided, as can be seen from the tree structure above, namely:

1. domain
2. emails
3. ip
4. username

Each of these folder houses scripts of it's own kind, i.e., scripts working on domain name as input are located in the domain folder and so on. You may have also noticed, each script in a module has a naming convention, i.e., a common prefix followed by an underscore and followed by the script name (e.g., domain_shodan.py). Please note this is required to be followed when adding a new script to the module. This way, dataSploit can dynamically pick up the script at runtime when triggered from the module's Osint script. 

### Writing a new script for an existing module

To write a new script for a module, there is a `template.py` located in each module directory to help you get started quickly. Following is the contents of the template.py file in the domain module:

```python
#!/usr/bin/env python

import base
import sys

# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    pass


def main(domain):
    # Use the domain variable to do some stuff and return the data
    print(domain)
    return []


def output(data, domain=""):
    # Use the data variable to print(out to console as you like)
    for i in data:
        print(i)


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
```

In short there are 3 functions that need to be implemented for a script:

1. `def banner()`
	This function should return a plain string describing what the collector is about to do. The shared runner prints the message with consistent formatting, so avoid direct `print()` or colour codes here.
		
2. `def main(input)`
	This function is a mandatory implementation. The parameter input to this function is what is passed as command line argument to the scripts. All data processing needs to be done in this function and it needs to return the data from this function. Please note, it is advised not to output anything in this function. The return value from here gets passed onto the next function for display.
		
3. `def output(data, input="")`
	This function is another mandatory implementation. It is used to handle how the data returned by the main function above is to be rendered on the console. The parameter data is the returned data from the mail function. The parameter input is an optional parameter and holds the value of the command line argument passed to the script. 

There is also another important variable in the script towards the top named `ENABLED`. By default, even in the template ENABLED is set to True. This variable can be used like a switch to control whether the script gets picked up for execution when running using either the parent datasploit.py script or either one of the Osint.py scripts.

Once you are done with modifying the template.py file and finalizing your code, you need to simply rename the file using the predefined format, i.e., the module prefix then an underscore and then the script name. For example, writing a new script for the domain module, the file needs to be renamed as `domain_scriptname.py`. Once this is done, the script will get automatically picked up by `datasploit.py`.

### Adding a new module to dataSploit

Adding a new module is also pretty straight forward. For example, let's say we want to add a module named mobile to dataSploit. Given below are the steps to add a new module.

1. Create a directory in the datasploit folder named mobile and move to the newly created directory.

	```bash
	mkdir mobile
	cd mobile
	```
	
2. Older versions relied on a `base.py` shim. This is **no longer required**—place your collector directly inside the new package (e.g. `domain/`, `emails/`, `ip/`, or `username/`).

3. Also in the same directory, create another file called `__init__.py`. This might be a good time to decide a prefix that will be used to name scripts in this module, for this document purpose we'll be picking the prefix name mobile.

    ```bash
    touch __init__.py
    vi __init__.py
    ```
    
    And add the following contents to the file:

    ```python
    """Mobile collectors for DataSploit."""

    __all__ = []
    ```
    
    *The core runner now auto-discovers modules. Store your collectors in the
    appropriate package with names like `mobile_<source>.py`, and set
    `ENABLED`, `REQUIRES`, and optional `MODULE_NAME`/`WRITE_TEXT_FILE`
    attributes within each module.*

4. No additional orchestrator script is required. The shared runner in `core/` automatically discovers collectors by filename. Once the package exists, create any number of `mobile_<source>.py` collectors, set the metadata (`ENABLED`, `MODULE_NAME`, `REQUIRES`), and they will be executed when you run `datasploit.py` or target them directly.

That's all. The new module is ready to be triggered via `python datasploit.py -i <target>` or by running its individual collectors (e.g. `python mobile/mobile_example.py <target>`).

The possibilities of extending dataSploit are endless. New modules and scripts are easily integrable as mentioned above. We look forward to seeing contribution from the community to help increase the capabilites of dataSploit.

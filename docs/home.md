# Overview of the tool:
* Performs OSINT on a domain / email / username / phone and find out information from different sources.
* Correlates and collaborate the results, show them in a consolidated manner. 
* Tries to find out credentials, api-keys, tokens, subdomains, domain history, legacy portals, etc. related to the target. 
* Use specific script / launch automated OSINT for consolidated data.
* Available in both GUI and Console.
 
Following API configs are useful for domain-oriented collectors:
* shodan_api
* censysio_id
* censysio_secret
* zoomeyeuser
* zoomeyepass
* clearbit_apikey
* emailhunter

Other modules:
* github_access_token
* jsonwhois


## Before running the program, please make sure that you have:
* Copied `config.template.ini` to `config.ini`
* Entered all the required APIs in the `config.ini` file, as mentioned above. 


## Usage
To launch an automated OSINT run:

```
python datasploit.py -i <target>
```

You can also run a standalone collector. For example, if you only want to enumerate subdomains:

```
python domain/domain_subdomains.py <domain_name>
```

## SETUP and Contribution
* Copy `config.template.ini` to `config.ini`
```
cp config.template.ini config.ini
```
* Configure respective API keys. Documentation for generating these keys will be shared very shortly. Believe us, we are working hard to get things in place. 
* Sources for which API keys are missing, will be simply skipped for the search. 

### Config files


### Python dependencies

```
pip install -r requirements.txt
```

If you have updated the code and want to push the pip dependencies in the requirements.txt 

```
pip freeze > requirements.txt
```

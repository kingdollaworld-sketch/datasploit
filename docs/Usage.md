Datasploit allows you to perform OSINT on a domain_name, email_id, username and phoneNumber. In order to launch any script, lets first understand the nomenclature of these scripts:

* All the scripts meant to perform osint on domain starts with the keyword ***'domain_'***. Eg. domain_subdomains, domain_whois, etc. In similar manner, scripts for osint on email_id starts with ***'email_'***, eg. email_fullcontact. 
* Scripts with an *underscore* are standalone scripts and collect data of one specific kind. They can still be executed directly for focused checks (e.g. `python domain/domain_subdomains.py example.com`).
* `datasploit.py` is the orchestrator. Point it at any supported target and it will classify the input and execute the relevant collectors automatically.

Run the orchestrator with the `-i/--input` flag, or supply a file via `-f/--file`:
```
python datasploit.py -i example.com
python datasploit.py -f targets.txt -o text
```
The `-o text` switch writes per-collector text reports to the working directory. JSON/HTML reporting can be added in a similar fashion by extending the shared runner.

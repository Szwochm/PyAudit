# PyAudit
These Python scripts are created with the intent to help an Analyst quickly gather information from logs, pcaps, events, etc 

**pyAudit.py**
Interactive shell that offer auditing functionality to cyber analysts.

Features: 

-Enumerating all installed applications and versions. Saving those results to a csv textfile and to database for further usage

Plans:

- Connecting to various vuln db APIs to see any CVE's related to applications and their versions
- Service enumeration
- User login enumeration
- Allowing other python auditing scripts to be run for further analysis such as the ones below

**Usage:** python pyAudit.py

# dupMacs
**dupMacs.py**
Takes a Pcap file and reads the raw data. The raw data is used to create an object that holds packet information at the various OSI levels. If a mac address is mapped to more than one ip address, the program will return the mac, as well as each ip address mapped to it.

**Notes:** Needs to be  tested. Only programmed to catch duplicate mac mappings sent via TCP packets. I should expand it to ARP, UDP at a minimum in the future

**Usage:** python dupMacs.py --pcap example-01.pcap 

# findWindowsRDP
**findWindowsRDP.py**
Queries WMI to return all Windows events that fit the search parameters

**Notes:** Reference: https://stackoverflow.com/questions/11219213/read-specific-windows-event-log-event -- I plan on adding more functionality to it in the future such as searching by timeframe, generating a visible alert,

**Usage:** python findWindowsRDP.py




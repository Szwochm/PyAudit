# PyAudit
These Python scripts are created with the intent to help an Analyst quickly gather information from logs, pcaps, events, etc 

**dupMacs.py**
Takes a Pcap file and reads the raw data. The raw data is used to create an object that holds packet information at the various OSI levels. If a mac address is mapped to more than one ip address, the program will return the mac, as well as each ip address mapped to it.

**Notes:** Needs to be  tested. Only programmed to catch duplicate mac mappings sent via TCP packets. I should expand it to ARP, UDP at a minimum in the future

**Usage:** python dupMacs.py --pcap example-01.pcap 


**findWindowsRDP.py**
Queries WMI to return all Windows events that fit the search parameters

**Notes:** Most of the code is from https://stackoverflow.com/questions/11219213/read-specific-windows-event-log-event -- I plan on adding more functionality to it in the future such as searching by timeframe, generating a visible alert,

**Usage:** python findWindowsRDP.py




# junos-command
Run a console command simultaneously on many network devices running the Juniper Junos operating system

#### Work
========
UNIX, Windows, etc

#### Dependencies
============
* ncclient - Netconf interface to Juniper devices. 
* PyYaml - YAML parsers for python.
* getpass - used to obsecure password prompt.

#### Configuration
=============
Sample config.yaml:
firewalls:
 - 10.16.50.11
 - 10.16.50.21

routers:
 - 10.16.50.20

#### Usage
=====
	[root@demo junos-command]# ./junos-command.py -h
	usage: junos-command.py [-h] -z ZONE -c COMMAND [-o OUTPUT]
	
	Run a command on many Juniper Junos OS devices via Netconf.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -z ZONE, --zone ZONE  category of network devices to run command against.
	  -c COMMAND, --command COMMAND
	                        command in quotes.
	  -o OUTPUT, --output OUTPUT
	                        file to output results.

junos-command.py --zone firewalls --command "show chassis hardware"

==================
	[root@demo junos-command]# ./junos-command.py -z firewalls -c "show chassis hardware"
	
	Using YAML Key: firewalls
	Executing Command: show chassis hardware
	
	Enter your network username: root
	Password: 
	
	
	
	>>>>>>>>>> 10.16.50.11 Start <<<<<<<<<
	Hardware inventory:
	Item             Version  Part number  Serial number     Description
	Chassis                                1c2fw16d0fg2      JUNOSV-FIREFLY
	Midplane        
	System IO       
	Routing Engine                                           JUNOSV-FIREFLY RE
	FPC 0                                                    Virtual FPC
	  PIC 0                                                  Virtual GE
	Power Supply 0  
	>>>>>>>>>> 10.16.50.11 End <<<<<<<<<
	
	>>>>>>>>>> 10.16.50.21 Start <<<<<<<<<
	Hardware inventory:
	Item             Version  Part number  Serial number     Description
	Chassis                                7bdcfwefad31      JUNOSV-FIREFLY
	Midplane        
	System IO       
	Routing Engine                                           JUNOSV-FIREFLY RE
	FPC 0                                                    Virtual FPC
	  PIC 0                                                  Virtual GE
	Power Supply 0  
	>>>>>>>>>> 10.16.50.21 End <<<<<<<<<


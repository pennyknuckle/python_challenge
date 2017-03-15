Nate_DB is a simple program with the capability to search through text for IPs, perform RDAP and GeoIP lookups, and filter through the resulting data.  

This program was written for, and tested in, Python 2.7.13. All development and testing was done in Windows 10.

Usage: 
	python natedb.py
	
You will then be prompted for a file name. This can be a relative or absolute path. 

Once a valid filename has been entered, Nate_DB will load valid IP addresses into the database. It will not load local or invalid IPs. This step may take some time. 

After Nate_DB has loaded every IP from the file, the user will receive a command prompt for querying Nate_DB. 'help' displays all valid commands within the DB. 

Some example queries: 

<NateDBQuery>:help		(displays help) 

<NateDBQuery>:ls		(lists all ips available in the database)

<NateDBQuery>:ip = <ip address> 	(displays all available info for an IP)

<NateDBQuery>:country_code = US  	(displays all IPs with country_code of US. This works for all GeoIP parameters)

<NateDBQuery>:region_name = Bogota D.C.   (same as above. Note that multi word searches should not be enclosed in quotes or have spaces escaped)

<NateDBQuery>:ip.rdap = <ip address> (displays the RDAP info only for an IP)

<NateDBQuery>:ip.geoip = <ip address> (displays the GeoIP info only for an IP)

Note that none of the above have leading spaces. Trailing spaces are OK. 


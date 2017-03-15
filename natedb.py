#Swimlane Python Practical 
#Written by Nate Marx for Swimlane

import re
import urllib2
import json
import sys



if sys.version_info[:3] > (2,7,13): #make sure it is not being run in Python 3. As of 3/14/17, Python 2.7.13 is the latest python2. 
	resp = raw_input('This program is written for Python 2.7 (2.7.13). The version appears to be incorrect. To override and run anyway, type \'run\'\n')
	if(resp != 'run'):
		print "Exiting!"
		sys.exit(1)


DB_Usage = "Welcome to Nate_DB!\r\nValid commands are as follows:\r\n\tls: List all database entries, names, and country codes.\r\n\tip = <ip address>: display all information available for a given IP\r\n\t<geoIP parameter> = <value>: display all IPs matching a certain geoIP parameter\r\n\tip.rdap = <value>: display just the RDAP data in the database for a given IP.\r\n\tip.geoip = <value>: display just the GeoIP data in the database for a given IP.\r\n\tquit: Exit Nate_DB"
def parseIPs(filename): #this function takes a file and puts everything that looks like an ip (4 sets of 1-3 numbers separated by dots) into a list, which it returns
	fil = open(filename, 'r')	
	ips = []
	regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}') #compile it to save time
	for line in fil: 
		result = regex.match(line)
		if(result != None):
			ips.append(result.group())
	fil.close()
	return ips
	
def makeValidIPs(ips): #this function takes a list of IPs and removes all local and invalid IPs from it. 
	ret = []
	for element in ips: 
		split_ip = element.split('.')
		split_ip = [int(i) for i in split_ip] #convert to int
		if len(split_ip) == 4: #this shouldn't ever hit, but just in case
			if all( i <= 255 and i >= 0 for i in split_ip): #check for invalid IPs
				if (split_ip[0] != 10 and split_ip[0] != 0 and not(split_ip[0]==172 and split_ip[1]>=16 and split_ip[1]<=31) and not(split_ip[0]==192 and split_ip[1]==168)):
					ret.append(element)
	return ret
			

def rdapQuery(ip): #this function takes an IP and returns the RDAP response as a dictionary
	return json.loads(urllib2.urlopen("https://rdap.arin.net/bootstrap/ip/"+ip).read())

def geoIPQuery(ip): #this function takes an IP and returns the GeoIP response as a dictionary 
	return json.loads(urllib2.urlopen("https://freegeoip.net/json/"+ip).read())
	
def buildDB(ips): #this function takes a list of valid ips and returns a dictionary of two element lists, where each ip is the key to a list of [rdap response, geoip response]
	db = {}
	for ip in ips: 
		print "Performing RDAP and GeoIP lookup on "+ip
		try:
			db[ip] = [rdapQuery(ip), geoIPQuery(ip)]
		except urllib2.HTTPError: 
			print "IP address "+ip+" is not returning valid data and will not be entered into the database"
	return db

def queryDB(db, query): #this function queries the database and returns the response as a string.  
	split_query = query.split(' ', 2) #separate the query into parts 
	if split_query[0] == "help":
		return DB_Usage
	if split_query[0] == "ls": 
		str = "IP Addresses in database are:\r\nIP\t\tName\t\tCountry Code\r\n" 
		for key in db: 
			str+= key + "\t" + db[key][0]["name"] + "\t" +  db[key][1]["country_code"] + "\n"
		return str
	if len(split_query) != 3:
		return "Invalid query. Type help for more options."
	split_query[2] = split_query[2].strip()
	if split_query[1] != "=": #this is the only valid type of query
		return "Invalid query. Type help for more options."
	if split_query[0] == "ip": #list all data available for an IP, in human readable format
		if not (split_query[2] in db): #do we have data for this ip?
			return "IP not found in database."
		else:
			return json.dumps(db[split_query[2]], indent = 4, sort_keys=True)
	elif split_query[0] in ["country_code", "city", "country_name", "metro_code", "region_code","region_name", "time_zone","zip_code","latitude","longitude"]:	#lists all IPs with a certain thing from GeoIP
		str = "Results for " + split_query[0] + " of " + split_query[2] + " are\n"
		for key in db: 
			if(db[key][1][split_query[0]] == split_query[2]):
				str += key + "\t" + db[key][0]["name"]+"\n"
		if (str != "Results for " + split_query[0] + " of " + split_query[2] + "are\n"):
			return str
		else: 
			return split_query[0] + " " + split_query[2] + " was not found in the database."
	elif split_query[0] == "ip.rdap":
		if not (split_query[2] in db): #do we have data for this ip?
			return "IP not found in database."
		else:
			return json.dumps(db[split_query[2]][0], indent = 4, sort_keys=True)
	elif split_query[0] == "ip.geoip":
		if not (split_query[2] in db): #do we have data for this ip?
			return "IP not found in database."
		else:
			return json.dumps(db[split_query[2]][1], indent = 4, sort_keys=True)
	else: 
		return "Invalid query. Type help for more options."
			
def main():
	good_file = False
	while(not good_file):		
		file = raw_input("Welcome to the Nate_DB. No database currently loaded. Type a file name to load IPs from a file.\r\n<NateDB>: ")
		if(file == "quit"):
			sys.exit(0)
		try:
			fil = open(file)
			fil.close()
			good_file = True
		except IOError: 
			print "Invalid file, try again"

	print "Parsing IPs, please wait"
	ips = parseIPs(file)
	valid_ips = makeValidIPs(ips)

	db = buildDB(valid_ips)

	print "Welcome to the Nate_DB. Database successfully loaded. Type help for a list of commands."
	sys.stdout.write("\r\n<NateDBQuery>: ")
	quit = False
	while(not quit):
		query = raw_input("")
		if query == "quit": 
			quit = True
		else:
			print queryDB(db, query)
			sys.stdout.write("<NateDBQuery>:")
			

main()

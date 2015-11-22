import commands
import csv, json, math, decimal, random, copy, sys, socket, time
from collections import defaultdict
from datetime import datetime


OUTPUTDIR = "/Users/vads/SSL/cert/"

# Reads the given url csv file and loads into a 
def readURLs(file):
	datadict = defaultdict(dict)
	urls = []
	
	with open(file, 'rb') as datasetfile:
		dataset = csv.reader(datasetfile)
		for instance in dataset:
			urls.append(instance[1])

	return urls

urls = readURLs("top-1m.csv")
index = 1
DEFAULTSSLPORT = 443
for url in urls:
	if index > 2000:
		break
	cmd = "echo 'x' | gtimeout 3 openssl s_client -connect " + url + ":443 " + " 1> " + OUTPUTDIR + url + ".cert 2>/dev/null"
	print "%d %s" % (index, commands.getstatusoutput(cmd))
	index += 1

#openssl s_client -connect google.com:443 > cert 2>/dev/null
#openssl x509 -in cert -noout -enddate 
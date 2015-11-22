import csv, json, commands, re, requests, sys
from collections import defaultdict

API_URL = "https://api.ssllabs.com/api/v2/analyze"

def isSHA1(url):
	cmd = "gtimeout 2 openssl s_client -connect " + url + ":443 < /dev/null 2>/dev/null | openssl x509 -text -in /dev/stdin | grep 'Signature Algorithm'"
	(status, outtext) = commands.getstatusoutput(cmd)
	if status != 0:
		return False
	if re.search('sha1WithRSAEncryption', outtext) != None:
		return True
	return False

def getSysLabsScore(url):
	payload = {'host': url, 'publish': 'off', 'startNew': 'off', 'fromCache': 'on', 'all': 'done'}
	response = requests.get(API_URL, params=payload)
	data = response.json()
	if data.get('status', None) == 'READY' and data != None and data.get('endpoints', None) != None and len(data['endpoints']) != 0:
		if data['endpoints'][0].get('grade', None) != None:
			return data['endpoints'][0]['grade']
	return None

output_file, jsonfilename = sys.argv[1:]
#jsonfilename = output_file.split('.')[0] + '.json'

csvfile = open(output_file, 'r')

#jsonfile = open(jsonfilename, 'wb')
fieldnames = ('url', 'days', 'expirationdate')
reader = csv.DictReader(csvfile, fieldnames)
output = []

index = 0
for each in reader:
	row = {}
	row['u'] = each['url']
	row['e'] = each['expirationdate']
	row['sha1'] = isSHA1(each['url'])
	row['s'] = getSysLabsScore(each['url'])
	#print "%s %s %s" % (row['u'], row['sha1'], row['s'])
	output.append(row)
	index += 1
	# write as json for every 100 units processed
	if index % 100 == 0:
		a = {}
		print "writing to file : %s" % index
		a['Data'] = output
		jsonfile = open(jsonfilename, 'wb')
		json.dump(a, jsonfile)

a = {}
a['Data'] = output
jsonfile = open(jsonfilename, 'wb')
json.dump(a, jsonfile)

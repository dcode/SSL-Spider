import csv, json, commands, re, requests
from collections import defaultdict

API_URL = "https://api.ssllabs.com/api/v2/analyze"
globallist = []
THREAD_COUNT = 50

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
	if data != None and data.get('endpoints', None) != None and len(data['endpoints']) != 0:
		return data['endpoints'][0]['grade']
	return None

class myThread (threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
    def run(self):
        process_data(self.threadID, self.q)
        

def process_data(threadID, q):
    while not exitFlag:
        queueLock.acquire()
        if ( not q.empty() ) and q.qsize() != 0:
            data = q.get()
            queueLock.release()
            processURL(data)
            #print "Yet to complete : %d" % q.qsize()
        else:
            queueLock.release()

def processURL(urlInfoObject):
    urlInfoObject['sha1'] = isSHA1(urlInfoObject['u'])
    urlInfoObject['s'] = getSysLabsScore(urlInfoObject['u'])
    globallist.append(urlInfoObject)

output_file = "outcopy.csv"
jsonfilename = output_file.split('.')[0] + '.json'
csvfile = open(output_file, 'r')
fieldnames = ('url', 'days', 'expirationdate')
reader = csv.DictReader(csvfile, fieldnames)
output = []
index = 0
for each in reader:
	row = {}
	row['u'] = each['url']
	row['e'] = each['expirationdate']
	print "%s %s %s" % (row['u'], row['sha1'], row['s'])
    output.append(row)
    index += 1
    if index > 100:
        break

threadList = [i for i in range(THREAD_COUNT)]
queueLock = threading.Lock()
workQueue = Queue.Queue(len(output))
threads = []
threadID = 1

# Create new threads
for threadID in threadList:
    thread = myThread(threadID, workQueue)
    thread.start()
    threads.append(thread)



# Fill the queue
queueLock.acquire()

LIMIT = len(urls)

i=0
for item in output:
    if i < LIMIT:        
        workQueue.put(item)
    i+=1

queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()

a = {}
a['Data'] = globallist
print "writing to file"
jsonfile = open(jsonfilename, 'w')
json.dump(a, jsonfile)

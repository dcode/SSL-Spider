import Queue, csv
import threading
import time
import csv, json, math, decimal, random, copy, sys, socket, time
from collections import defaultdict
from datetime import datetime
from OpenSSL import SSL
import socket
import sys 
from datetime import datetime

# Dumped from MAC OS X El Capitan's keychain
CA_CERTS = "dummycert.pem"
#OUTPUT_FILE = "SSLAudit.txt"
#ERROR_FILE = "SSLAudit_Error.txt"
THREAD_COUNT = 50
DEFAULTSSLPORT = 443

output_file_handle = sys.stdout
error_file_handle = sys.stderr#open(ERROR_FILE, 'w')
output_string = ""

exitFlag = 0

def pyopenssl_check_callback(connection, x509, errnum, errdepth, ok):
    ''' callback for pyopenssl ssl check'''
    if not ok:
        return True
    return ok


def pyopenssl_check_expiration(asn1):
    ''' Return the numbers of day before expiration. False if expired.'''
    try:
        expire_date = datetime.strptime(asn1, "%Y%m%d%H%M%SZ")
    except:
        print >> sys.stderr, 'Certificate date format unknown.'

    expire_in = expire_date - datetime.now()
    return expire_in.days, expire_date

# Reads the given url csv file and loads into a 
def readURLs(file):
    datadict = defaultdict(dict)
    urls = []
    
    with open(file, 'rb') as datasetfile:
        dataset = csv.reader(datasetfile)
        for instance in dataset:
            urls.append(instance[1])

    return urls

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

def processURL(url):
    global output_string
    # Connect to the host and get the certificate
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((url, DEFAULTSSLPORT))
    except Exception as e:
        error_file_handle.write("%s,%s\n" % (url, e))
    sock.settimeout(None)
    # Use SSL and read the certificates for the given urls
    # Assumes that the SSL port is 443 across all servers
    try:
        ctx = SSL.Context(SSL.TLSv1_2_METHOD)
        ctx.set_verify(SSL.VERIFY_NONE | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                       pyopenssl_check_callback)
        #ctx.load_verify_locations(CA_CERTS)

        ssl_sock = SSL.Connection(ctx, sock)
        ssl_sock.set_connect_state()
        ssl_sock.set_tlsext_host_name(url)
        ssl_sock.do_handshake()

        x509_chain = ssl_sock.get_peer_cert_chain()
        if x509_chain:
          depth = 0
          for item in x509_chain:
            event = {
              "url": url,
              "sha256": item.digest("sha256").replace(":", ""),
              "depth": depth,
              "md5":  item.digest("md5").replace(":", ""),
              "commonName": item.get_subject().commonName,
              "notBefore": datetime.strptime(item.get_notBefore(), "%Y%m%d%H%M%SZ").isoformat() + "Z",
              "notAfter": datetime.strptime(item.get_notAfter(), "%Y%m%d%H%M%SZ").isoformat() + "Z"
            }

            output_file_handle.write(json.dumps(event)+"\n")
            depth += 1

        ssl_sock.shutdown()
    except SSL.Error as e:
        error_file_handle.write("%s,%s\n" % (url, e))

    sock.close()

input_file = sys.argv[1]
#print input_file
urls = readURLs(input_file)
threadList = [i for i in range(THREAD_COUNT)]
queueLock = threading.Lock()
workQueue = Queue.Queue(len(urls))
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
for url in urls:
    if i < LIMIT:        
        workQueue.put(url)
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
#exit(0)

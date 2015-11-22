import csv, json, math, decimal, random, copy, sys, socket, time
from collections import defaultdict
from datetime import datetime
#from OpenSSL import SSL
import ssl

# Citations:
# https://gist.github.com/crashdump/5683952

# CA_CERTS below is a dummy one that I created for MAC OS X since Apple's OPENSSL looks at the System key chain
CA_CERTS = "/etc/hg-dummy-cert.pem"

# Reads the given url csv file and loads into a 
def readURLs(file):
	datadict = defaultdict(dict)
	urls = []
	
	with open(file, 'rb') as datasetfile:
		dataset = csv.reader(datasetfile)
		for instance in dataset:
			urls.append(instance[1])

	return urls

def pyssl_check_expiration(cert):
    ''' Return the numbers of day before expiration. False if expired. '''
    if 'notAfter' in cert:
        try:
            expire_date = datetime.strptime(cert['notAfter'],
                                            "%b %d %H:%M:%S %Y %Z")
        except:
            print 'Certificate date format unknow.'
        expire_in = expire_date - datetime.now()
        if expire_in.days > 0:
            return expire_in.days
        else:
            return False

urls = readURLs("top-1m.csv")
index = 1
DEFAULTSSLPORT = 443
for url in urls:
	if index > 1000:
		break
	# Use SSL and read the certificates for the given urls
	# Assumes that the SSL port is 443 across all servers
	
    # Check the DNS name
	try:
		socket.getaddrinfo(url, DEFAULTSSLPORT)[0][4][0]
	except socket.gaierror as e:
		print e

    # Connect to the host and get the certificate
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((url, DEFAULTSSLPORT))

	print "urls %s connected" % url
	try:
		ssl_sock = ssl.wrap_socket(sock,cert_reqs=ssl.CERT_REQUIRED,ca_certs=CA_CERTS, ciphers=("HIGH:-aNULL:-eNULL:""-PSK:RC4-SHA:RC4-MD5"))
		cert = ssl_sock.getpeercert()
		print pyssl_check_expiration(cert)
		sock = ssl_sock.unwrap()
	except ssl.SSLError as e:
		print e
	sock.close()

	

	index += 1

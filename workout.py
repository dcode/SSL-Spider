import csv, json, math, decimal, random, copy, sys, socket, time
from collections import defaultdict
from datetime import datetime
from OpenSSL import SSL
import socket

from ssl import wrap_socket, CERT_NONE, PROTOCOL_SSLv23
from ssl import SSLContext  # Modern SSL?
from ssl import HAS_SNI  # Has SNI?


CA_CERTS = "/etc/hg-dummy-cert.pem"

def pyopenssl_check_callback(connection, x509, errnum, errdepth, ok):
	''' callback for pyopenssl ssl check'''
	if x509.has_expired():
		print 'Error: Certificate has expired!'
	else:
		print pyopenssl_check_expiration(x509.get_notAfter())

	if not ok:
		return False
	return ok


def pyopenssl_check_expiration(asn1):
	''' Return the numbers of day before expiration. False if expired.'''
	try:
		expire_date = datetime.strptime(asn1, "%Y%m%d%H%M%SZ")
	except:
		print 'Certificate date format unknown.'

	expire_in = expire_date - datetime.now()
	return expire_in.days

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
index = 0
DEFAULTSSLPORT = 443
for url in urls:
	print "url  %s" % url
	if index > 1000:
		break
	index += 1
	# Connect to the host and get the certificate
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(2)
	try:
		sock.connect((url, DEFAULTSSLPORT))
	except Exception as e:
		print "exception for %s : %s" % (url, e)
		continue
	print "\t connected"
	sock.settimeout(None)
	# Use SSL and read the certificates for the given urls
	# Assumes that the SSL port is 443 across all servers
	try:
		ctx = SSL.Context(SSL.TLSv1_METHOD)
		ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                       pyopenssl_check_callback)
		ctx.load_verify_locations(CA_CERTS)

		ssl_sock = SSL.Connection(ctx, sock)
		ssl_sock.set_connect_state()
		ssl_sock.set_tlsext_host_name(url)
		ssl_sock.do_handshake()

		x509 = ssl_sock.get_peer_certificate()
		x509name = x509.get_subject()
		print "url: %s, expires in : %s" % (url, pyopenssl_check_expiration(x509.get_notAfter()))
        #if x509name.commonName != HOST:
        #    print 'Error: Hostname does not match!'
		ssl_sock.shutdown()
	except SSL.Error as e:
		print "ssl error for %s %s" % (url, e)

	sock.close()

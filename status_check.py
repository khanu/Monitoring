#!/usr/bin/python
  
import urllib2,sys
import socket
import time

#Define Graphite server and open socket
#def sendMetric(name, value, timestamp):
#    sock = socket.socket()
#    sock.connect( ("graphite.nyumc.org", 2103) )
#    sock.send("%s %d %d\n" % (name, value, timestamp))
#    sock.close()

#def now():
#    return int(time.time())

url = sys.argv[1]
server = (url.split('/')[2]).split('.')[0]

try:
    urllib2.urlopen(url)
except (urllib2.HTTPError, urllib2.URLError) as e:
    if "sycl" in server or "promis" in server:
        print "sycl or promis and error"
    else:
        if "nyulmc" in url:
            print "nyulmc"
        else:
            print "error"
else:
    if "sycl" in server:
        print "sycl and no error"
    else:
        print "no error"

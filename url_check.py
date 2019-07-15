#!/usr/bin/python
  
import urllib2,sys
import socket
import time


url = sys.argv[1]
server = (url.split('/')[2]).split('.')[0]
print server
try:
    urllib2.urlopen(url)
except (urllib2.HTTPError, urllib2.URLError) as e:
    print e.args

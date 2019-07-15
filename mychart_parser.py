#!/usr/bin/python
import codecs, os
import re
#import wget
import urllib2
import time
import socket

#Define Graphite server and open socket
def sendMetric(name, value, timestamp):
    sock = socket.socket()
    sock.connect( ("graphite.nyumc.org", 2003) )
    sock.send("%s %d %d\n" % (name, value, timestamp))
    sock.close()

def now():
    return int(time.time())

#Remove previously downloaded js file
if os.path.exists('promis-popup.js'):
    os.remove('promis-popup.js')

#Download Promis popup.js from Mychart page
url = 'https://mychart.nyulmc.org/mychart/en-US/scripts/Mobile-Integration/promis-popup.js'
#wget.download(url, bar=None)
filehandle = urllib2.urlopen(url)
datatowrite = filehandle.read()
with open('/Users/khanu/Py/promis-popup.js', 'wb') as f:
    f.write(datatowrite)
txtFile = codecs.open('promis-popup.js', 'r', 'utf-8')

#Look for var url value and send '1' for expected value and '0' for anything else
for line in txtFile:
    lines = repr(line)
    matchobject = re.match(r"[^/]+[var]\s?[url]\s=\s+(?P<promis_url>.*)\;", lines)
    if matchobject:
        if matchobject.groupdict()['promis_url'] != '"https://promis.nyulmc.org/proms/current/web"':
            sendMetric("Promis.var_url", 1, now())
        else:
            sendMetric("Promis.var_url", 0, now())

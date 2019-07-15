#!/usr/bin/python

'''
Script that checks if the Redis cluster is in sync and sends status to Graphite
'''

import sys
import subprocess
import time
import socket
from collections import Counter
import collections
import argparse


__author__      = "Khanu Dev"
__copyright__   = "Copyright 2019, NYUMC"



# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env", required=True,
	help="Environment")
args = vars(parser.parse_args())
 

#Get server list for given env
def serverlist(argument):
	switcher ={
		'dev' : ['rdilcdcdvm001', 'rdilcdcdvm002'],
		'qa' : ['rdilcdcqvm001', 'rdilcdcqvm002', 'rdilbdcqvm001', 'rdilbdcqvm002'],
		'stg' : ['rdilcdcsvm001', 'rdilcdcsvm002', 'rdilcdcsvm003'],
		'prod' : ['rdilcdcpvm001', 'rdilcdcpvm002', 'rdilcdcpvm003', 'rdilbdcpvm001', 'rdilbdcpvm002', 'rdilbdcpvm003']
		}
	return switcher.get(argument)

servers = serverlist(args['env'])

key_dict = {}


#Define Graphite server and open socket
def sendMetric(name, value, timestamp):
    sock = socket.socket()
    sock.connect( ("mcalcdcpvm001.nyumc.org", 2103) )
    sock.send("%s %d %d\n" % (name, value, timestamp))
    sock.close()

def now():
    return int(time.time())


for server in servers:
	try:
		cmd = "redis-cli -p 22122 -h %s --scan |wc -l" % server
		keys = subprocess.check_output(cmd, shell=True)
		key_dict[server] = int(keys)
		sendMetric("redis.%s.%s.status" % (args['env'],server), int(keys), now())
	except socket.error, exc:
        	print "Caught exception socket.error : %s" % exc

uniqueValues = set(key_dict.values())
keyList = [ k for k in key_dict.keys() if key_dict[k] == collections.Counter(key_dict.values()).most_common()[-1][0] ]

try:
	if len(uniqueValues) > 1:
		sendMetric("redis.%s.status" % sys.argv[2], 0, now())
	else:
		sendMetric("redis.%s.status" % sys.argv[2], 1, now())
except socket.error, exc:
	print "Caught exception socket.error : %s" % exc

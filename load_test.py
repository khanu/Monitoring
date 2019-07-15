#!/usr/bin/python
import re, os 
import subprocess
from subprocess import call

logfile = 'sample_log'
url_list = []

if os.path.exists('url_list'):
	os.remove('url_list')

siege_list = open('url_list', 'w')

#Regex for Apache log

log_parts = [
    r'(?P<symfony>\S+)',                  # symfony %h
    r'(?P<host>\S+)',                  # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]

pattern = re.compile(r'\s+'.join(log_parts)+r'\s*\Z')
fhandle = open(logfile, 'r')

for line in fhandle:
        match = pattern.match(line)
        if match:
                output = match.groupdict()
		url_list.append(output['referer'])

while '-' in url_list:
	url_list.remove('-');


for url in url_list:
	siege_list.write("%s\n" % url)


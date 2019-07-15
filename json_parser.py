#!/usr/bin/python 

import json

with open('strings.json') as f:
    d = json.load(f)
    print(d)

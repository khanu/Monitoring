#!/usr/bin/python

import xml.etree.ElementTree as ET

tree = ET.parse("/Users/khanu/stash/helpix/pom.xml")
#root = tree.getroot()
artifactlist = tree.findall('project/licenses/license')

for item in artifactlist:
    print 'Artifact ID:', item.find('name').text

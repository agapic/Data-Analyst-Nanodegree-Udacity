#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Determine the key type of the tag and display the frequency in the result "keys"

def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter("tag"):
            k = tag.attrib['k']
            if lower.match(k):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.match(k):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.match(k):
                keys['problemchars'] = keys['problemchars'] + 1
                print k
            else:
                keys['other'] = keys['other'] + 1
        pass

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('nyc.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    test()

   # {'lower': 3267447, 'lower_colon': 5033452, 'other': 111495, 'problemchars': 2}
    # The problematic chars were #B29C87, #B29C87
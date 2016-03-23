import xml.etree.ElementTree as ET
import pprint

# Determine the frequency of each first-level tag
def count_tags(filename):
    tags = {}
    for event, node in ET.iterparse(filename):
        tag = node.tag
        if tag and not tag in tags.keys():
            tags[tag] = 0
        tags[tag] = tags[tag] + 1
    return tags

def run():
    tags = count_tags("nyc.osm")
    pprint.pprint(tags)

if __name__ == "__main__":
    run()

 #    {'bounds': 1,
 # 'member': 84089,
 # 'nd': 11295460,
 # 'node': 8702216,
 # 'osm': 1,
 # 'relation': 8189,
 # 'tag': 8412396,
 # 'way': 1432097}
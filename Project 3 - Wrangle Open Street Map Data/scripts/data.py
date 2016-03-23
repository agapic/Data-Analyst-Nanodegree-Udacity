import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json
import phonenumbers

OSMFILE = "nyc.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')

# Matches very last word in a street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
zip_code_re = re.compile(r'^\d{5}(?:[-\s]\d{4})?$')
fix_zipcode_state_short = re.compile(r'^[A-Z]{2}\s\d{5}(?:[-\s]\d{4})?$')

tags = {}

expected_street_types = ['Ridge', 'Hills', 'Bottom', 'Union', 'Brook', 'Causeway', 'Heights', 'Station', 'Hill', 'Branch', 'Lodge',
            'Isle', 'Burg', 'Dam', 'Cove', 'Landing', 'Shores', 'Trailer', 'Path', 'Haven', 'Key', 'Island', 'Camp',
            'Ferry', 'River', 'Ville', 'Creek', 'Alley', 'Course', 'Prairie', 'Corner', 'Mill', 'Glen', 'Arcade',
            'Mills', 'Plains', 'Rest', 'Bypass', 'Circle', 'Walk', 'Fork', 'Run', 'Extension', 'Park', 'Lakes', 'Ford',
            'Grove', 'Courts', 'Cape', 'Spur', 'Fort', 'Ranch', 'Orchard', 'Harbor', 'Light', 'Plaza', 'Shore', 'Green',
            'Islands', 'Loop', 'Square', 'Stream', 'Point', 'Pines', 'Viaduct', 'Mall', 'Shoal', 'Pass', 'Place', 'Row',
            'Mountain', 'Boulevard', 'Inlet', 'Bayou', 'Forest', 'Way', 'Meadows', 'Tunnel', 'Dale', 'Trail', 'Pike',
            'Lane', 'Center', 'Corners', 'Mount', 'Summit', 'Turnpike', 'Flats', 'Parkway', 'Road', 'Loaf', 'Divide',
            'Hollow', 'Locks', 'Canyon', 'Oval', 'Avenue', 'Stravenues', 'Vista', 'Court', 'Lake', 'Field', 'Forge',
            'Expressway', 'Beach', 'Forks', 'Highway', 'Neck', 'Valley', 'Manor', 'Annex', 'Track', 'Wells', 'Falls',
            'Bluff', 'Fall', 'Bend', 'Knolls', 'Fields', 'Village', 'Drive', 'Freeway', 'Estates', 'Radial', 'Crossing',
            'Junction', 'Cliffs', 'Gardens', 'View', 'Bridge', 'Trace', 'Rapids', 'Spring', 'Shoals', 'Mission', 'Port',
            'Club', 'Street', 'Terrace', 'Plain', 'Rest', 'Springs', 'Crescent', 'Gateway', 'East', 'North', 'South',
            'West', "Southwest", "Slip", "Piers", "Driveway", "Promenade", "Americas", "Finest", "Esplanade", "Farm",
            "Close", "Bush", "Commons", "Concourse", "Cross", "Mews"]

street_type_mapping = { "Ave" : "Avenue",
            "St" : "Street",
            "Rd" : "Road",
            "Steet" : "Street",
            "Pkwy" : "Parkway",
            "Pky" : "Parkway",
            "Blvd" : "Boulevard",
            "Blv" : "Boulevard",
            "Avene" : "Avenue",
            "Aveneu" : "Avenue",
            "Avenue,#39" : "Avenue",
            "Streeet" : "Street",
            "Turnlike" : "Turnpike",
            "Tunrpike" : "Turnpike",
            "Tpke": "Turnpike",
            "Tirnpike": "Turnpike",
            "S": "South",
            "Pl": "Place",
            "Plance" : "Place",
            "Dr": "Drive",
            "Ct": "Court",
            "Bellerose": "Avenue",
            "Hwy": "Highway"
            }

ignored_street_types = ["Roadbed", "X", "Y", "Z", "Woodside", "", "E", "Floor", "F", "Dien", "D", "Ctr" ]
ignored_tags = ["fixme", "keywo"]

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# Map invalid street types to correct ones and strip off non alphabetical characters off of the end of street types
# Returns False if the street type is unmappable or is not in expected, meaning it will be ignored.
def sanitize_street_type(street_type):
    if not street_type[-1].isalpha():
        return street_type[:-1]
    elif street_type in street_type_mapping.keys():
        return street_type_mapping[street_type]
    else:
        return False

# Takes in a good or bad zip code and spits out a correct one.
# Sanitize zip codes to return a 5 digit zip code. Example: "NY, 12345" -> "12345"
def sanitize_zipcode(zip_code):
    zip_code = zip_code.strip()
    m = zip_code_re.search(zip_code)
    if m:
        return zip_code
    elif zip_code[0:3] == 'New':
        zip_code = zip_code[-5:]
        return zip_code
    elif fix_zipcode_state_short.search(zip_code):
        zip_code = zip_code[3:]
        return zip_code

# Creating a JSON object from the node data; these are the documents that will be imported into MongoDB
def shape_element(element):
    # Initialize empty node object
    node = {}

    if element.tag == "node" or element.tag == "way" :
        # Begin iterating through first level tags
        for key in element.attrib.keys():
            val = element.attrib[key]
            node["type"] = element.tag
            # Create the { "created" {} } subdocument to store characteristics about the node's creation
            if key in CREATED:
                if "created" not in node.keys():
                    node["created"] = {}
                node["created"][key] = val
            # Store the geographical coordinates for the node as a position with a lat/lon pair
            elif "lat" in element.keys() and "lon" in element.keys():
                node["pos"] = [float(element.get('lat')), element.get('lon')]
            else:
                node[key] = val
        # Begin iterating through second level tags
        for tag in element.iter("tag"):
            tag_key = tag.attrib['k']
            tag_val = tag.attrib['v']
            # If the tag has problem chars, skip to the next tag
            if problemchars.match(tag_key):
                continue
            # If the tag is in ignored tags, skip to the next tag
            elif tag_key[0:5].lower() in ignored_tags:
                continue
            # Insert the sanitized zipcode into the address subdocument
            elif tag_key == "addr:postcode":
                if "address" not in node.keys():
                    node["address"] = {}
                node["address"]["zipcode"] = sanitize_zipcode(tag_val)
            # Check various problematic address types and either fix them or continue on to the next tag if they're ignored
            elif tag_key == "addr:street":
                if "address" not in node.keys():
                    node["address"] = {}
                m = street_type_re.search(tag_val)
                if m:
                    street_type = m.group().lower().title()
                    if str(street_type[0]).isdigit() or len(street_type) < 2 or street_type in ignored_street_types:
                        continue
                    if street_type in expected_street_types:
                        node["address"]["street"] = tag_val
                    if sanitize_street_type(street_type):
                        node["address"]["street"] = tag_val.rsplit(' ', 1)[0] + ' ' + sanitize_street_type(street_type)
            # Using the python phonenumbers library, turn every single phone number type into a string of 10 digits
            elif tag_key == "contact:phone":
                node["phone"] = phonenumbers.parse(tag.attrib['v'], "US").national_number
            # For every other valid tag, insert it into the object. Example: tag_key = "amenity" and tag_val = "restaurant"
            elif lower.match(tag_key):
                node[tag_key] = tag_val
        # Construct a list of node_refs for a given node
        for nd in element.iter("nd"):
            if 'node_refs' not in node:
              node['node_refs'] = []
            node['node_refs'].append(nd.attrib['ref'])
        return node
    else:
        return None

# Begin inserting the documents into a json file
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    # Shape element and write out a sanitized node to a json file
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('nyc.osm', False)
    return
    #pprint.pprint(data)

if __name__ == "__main__":
    test()

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

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

expected = ['Ridge', 'Hills', 'Bottom', 'Union', 'Brook', 'Causeway', 'Heights', 'Station', 'Hill', 'Branch', 'Lodge',
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

mapping = { "Ave" : "Avenue",
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

ignored = ["Roadbed", "X", "Y", "Z", "Woodside", "", "E", "Floor", "F", "Dien", "D", "Ctr" ]
ignored_tags = ["fixme", "keywo"]

def is_street_name(elem):
    return (elem.attrib['k'] == 'addr:street')

def is_zip_code(elem):
    return (elem.attrib['k'] == 'addr:postcode')


def audit_zip_code(zip_code):
    zip_code = zip_code.strip()
    m = zip_code_re.search(zip_code)
    if zip_code[0:3] == 'New':
        zip_code = zip_code[-5:]
        return zip_code
    if fix_zipcode_state_short.search(zip_code):
        zip_code = zip_code[3:]
        return zip_code
    if m:
        return zip_code

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group().lower().title()
        if len(street_type) < 2: return
        if not street_type[-1].isalpha():
            street_type = street_type[:-1]
        if str(street_type[0]).isdigit():
            return
        if street_type in mapping.keys():
            street_type = mapping[street_type]
        if street_type not in expected and street_type not in ignored:
            street_types[street_type].add(street_name)

def audit():
    for event, elem in ET.iterparse(OSMFILE, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'][0:5].lower() not in ignored_tags:
                    if tag.attrib['k'] not in tags.keys():
                        tags[tag.attrib['k']] = 0
                    tags[tag.attrib['k']] = tags[tag.attrib['k']] + 1
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_zip_code(tag):
                    audit_zip_code(tag.attrib['v'])
    pprint.pprint(dict(street_types))
    print len(street_types)

if __name__ == "__main__":
    audit()
    pprint.pprint(tags)


# OpenStreetMap Project -- Data Wranglign with MongoDB
# Andrew Gapic

Map Area: New York, New York, United States

Data retrieved from: https://s3.amazonaws.com/metro-extracts.mapzen.com/new-york_new-york.osm.bz2 on March 5th, 2016.


## 1. Problems Encountered in the Map

Being the highest populated city in the United States makes New York a great candidate for having bad data. The two main issues I recognized from the data given on New York City inaccurate street and zip code data. Another minor issue was phone number data which was fixed easily thanks to a the <b>phonenumbers python library</b>.

### Inaccurate Street Names
New York City had a very diverse set of street types. I used the website https://access.ewu.edu/mail-services/references/abbreviations-for-street-designators and parsed out the street types and added them to expected_street_types. Google Maps was used to spot check the many street types that were missing from that data. Regular expressions was used to take care of things such as "Ave., AVE., AvE, etc." Additionally there were many nonsensical street types, such as "X", "D", and "Floor" for example. These could not be spot checked with Google Maps or other sources so they were ignored. In total, there were 51 additional street types that were ignored. (see ignored_street_types.txt) Some were actually plazas as opposed to streets, others atriums. This is clearly not street data.

### Inaccurate/Inconsistent Zip Codes

In the United States, there are two lexically valid zipcodes: 5 consecutive numbers, or 5 consecutive numbers, a hypen, and 4 more consecutive numbers.

A regular expression was used to check if a zip code was lexically valid. There were no semantic checks on whether a zip code actually belonged in New York as opposed to somewhere else. This is a drawback of the data analysis and should be accounted for. Examples of various zip codes that were fixed were "NY 12345" and "New York, NY 12345". In some circumstances, some zip codes were in the form "12345;54321". Since I had no knowledge as to which one they were referring to, I ignored them. One zip code was even a phone number. Here is the aggregate list of ignored zip codes in the end:

11
2
12
74
11
61
56
320
(718) 778-0140
320
11201;11231
3
11231;11230
11214;11223
NJ
83
NJ
83
111743
111756

## 2. Data Overview

There are 6 key python files used here; consisting of answers from lesson 6 from the Data Wrangling with MongoDB course. These would be parse_map.py, tag_types.py, users.py, 
* parse_map.py - Display occurrences of tags. Note this was in the audit phase, so there is likely less data than this in the final product.
        {'bounds': 1,
        'member': 84089,
        'nd': 11295460,
        'node': 8702216,
        'osm': 1,
        'relation': 8189,
        'tag': 8412396,
        'way': 1432097}
* tag_types.py - Determine problem tags, lowercase tags, lower_colon tags, and other
          {'lower': 3267447, 'lower_colon': 5033452, 'other': 111495, 'problemchars': 2}
         Note: The problematic tag keys were #B29C87, #B29C87
* users.py - Unique users
* audit.py - Audit streets, zip codes, and get an aggregate count of the other types. See file for more information
* data.py - The core of the application. Its purpose is to convert the OSM data, clean it, and then convert to JSON.
* queries.py - The aggregrate queries made to MongoDB. More details on this will be discussed later in this section.

#### File sizes

`nyc.osm - 2.2GB`

`nyc.osm.json - 2.2GB`

#### Number of documents

    > db.nycosm.find().count()
    10134313

#### Number of nodes
    > db.nycosm.find({"type":"node"}).count()
    8702056

#### Number of ways
    > db.nycosm.find({"type":"way"}).count()
    1431660

#### Number of unique users
    > db.nycosm.distinct("created.user").length
    3521

#### Top Contributing User
    > db.nycosm.aggregate([{"$group": {"_id":"$created.user", "count": {"$sum":1}}}, {"$sort": 
     {"count":-1}}, {"$limit":1}])
     { "_id" : "Rub21_nycbuildings", "count" : 4894645 }
     
#### Number of users with only 1 contribution

    > db.nycosm.aggregate([{"$group": {"_id":"$created.user", "count": {"$sum":1}}}, {"$group":
    {"_id":"$count", "num_users":{"$sum":1}}}, {"$sort": {"_id":1}}, {"$limit":1}])
    { "_id" : 1, "num_users" : 910 }
    


### Additional Data Exploration using MongoDB Queries

#### Top 3 religions
    {"$match": {"religion": {"$exists": 1}}},
    {"$group": {"_id": "$religion", "count": {"$sum":1}}},
    {"$sort": {"count": -1}},
    {"$limit": 3}
    
    [{u'_id': u'christian', u'count': 4054},
     {u'_id': u'jewish', u'count': 369},
     {u'_id': u'muslim', u'count': 34}]

#### Top 10 Leisure Activities

    [{"$match": {"leisure": {"$exists": 1}}},
    {"$group": {"_id": "$leisure", "count": {"$sum":1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}]

#### Top 10 Restaurants with a Name

    [{"$match":{"amenity":{"$exists":1}, "name":{"$exists":1}, "amenity":"restaurant"}},
    {"$group":{"_id":"$name", "count":{"$sum":1}}},
    {"$sort":{"count":-1}},
    {"$limit":10}]
    
    [{u'_id': u"Applebee's", u'count': 16},
     {u'_id': u'IHOP', u'count': 13},
     {u'_id': u'Outback Steakhouse', u'count': 11},
     {u'_id': u"Chili's", u'count': 9},
     {u'_id': u'Bareburger', u'count': 8},
     {u'_id': u'Red Lobster', u'count': 7},
     {u'_id': u'Chipotle', u'count': 7},
     {u'_id': u'Ruby Tuesday', u'count': 7},
     {u'_id': u'Applebees', u'count': 6},
     {u'_id': u'Pizza Hut', u'count': 6}]


## 3 Additional Ideas

Throughout this project, I was fairly skeptical of the concept of Open Street Map. It has one major flaw -- it assumes the user enters correct data. As shown from this report, this is far from the case. Some of the data is so peculiar and strange that it makes me wonder if a bot were responsible for a large amount of the data. Additionally, a lot of the data appears to be incomplete. Both of these will now be discussed.

* Contribution Statistics

It's fairly evident that a single user is not responsible for a large amount of these entries. The highest contribution rate from a user was 48.3% (Rub21_nycbuildings). This user had <b>4894645</b> entries and it's pretty unlikely that a human made these many entries manually.

Upon further inspection, see the top 10 users here below. They contribute to 77.44% of all of the entries. One user is even named woodpeck_fixbot, which looks very suspicious. Only one user -- CoreyFarwell -- has a username that stands out from the rest. Something else that stands out is the fact that ingalls apparently has TWO nicknames (ingalls_nycbuildings and ingalls). But these facts alone don't tell us much about what's going on. 

A way to improve this would be to somehow disallow bots from using OSM by having a more well known and respected user community or force each entry to adhere to some standards. For example, disallow having a phone number has a zip code, disallow having a street called "1". Some sort of data sanitization into the input of OpenStreetMaps would go a long way 

        { "_id" : "Rub21_nycbuildings", "count" : 4894645 }
        { "_id" : "ingalls_nycbuildings", "count" : 935966 }
        { "_id" : "woodpeck_fixbot", "count" : 651937 }
        { "_id" : "ediyes_nycbuildings", "count" : 272560 }
        { "_id" : "lxbarth_nycbuildings", "count" : 234972 }
        { "_id" : "NJDataUploads", "count" : 229033 }
        { "_id" : "ingalls", "count" : 191952 }
        { "_id" : "CoreyFarwell", "count" : 171652 }
        { "_id" : "celosia_nycbuildings", "count" : 134621 }
        { "_id" : "ebrelsford_nycbuildings", "count" : 130491 }
    
* Complete data

A large proportion of the data is missing useful information -- the kind of information that we actually want to know more about. For example, doing a quick query of the top 10 amenities gives us the following:

    { "_id" : "parking", "count" : 6259 }
    { "_id" : "bicycle_parking", "count" : 4867 }
    { "_id" : "school", "count" : 4660 }
    { "_id" : "place_of_worship", "count" : 4561 }
    { "_id" : "restaurant", "count" : 2837 }
    { "_id" : "fast_food", "count" : 932 }
    { "_id" : "cafe", "count" : 876 }
    { "_id" : "bank", "count" : 739 }
    { "_id" : "fire_station", "count" : 677 }
    { "_id" : "bench", "count" : 566 }

I'm interested in knowing more restaurants AND fast food. Combined they make up <b> 0.03719%</b> of the rows in the database. According to Wikipedia, New York City's land area is 304.8 square miles. If we were to assume the data was complete, then there would be one restaurant or fast food joint in a 0.08 mile radius. This sounds reasonable, except that (according to Wikipedia) New York City is the sixth densest city in the United States and has 27016 people per square meter. Therefore, there would be roughly 1 restaurant/fastfood joint for 2161.28 people. This is highly unlikely and points to the data being incomplete.

Additionally, running the query `> db.nycosm.aggregate([{"$match":{"address":{"$exists":0}, "type": "node"}},{"$group":{"_id":"$address", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])` gives us 8562175 node fields that have no address, or <b> 84.49 percent </b>.  

Another issue is the recency of the data; a lot of the data has a timestamp from 2009. Things change rapidly -- within a year, a Pizza Hut franchise can shut down and be converted to a parking lot, for example. Therefore, there can be a lot of bad outdated data. It would be infeasible to determine if a single row of data is invalid. Additionally, it may not be the best idea to filter tags with a timestamp of the current year, as you might be missing a lot of good data. A reasonable compromise would be to determine a minimum timestamp that is acceptable when wrangling the data. Admittedly, this is a major fallback for this data analysis as timestamp was neglected throughout the process.

If OpenStreetMap forces the user to meet a specific standard when submitting information (i.e., if the address is an amenity, include more relevant information on what type of amenity, what the name is), then there may be significantly less information to work from via the users. Additionally, the users who use bots to map GPS coordinates from their vehicles to OpenStreetMap would be nonexistent in node tags (though it should still be acceptable in way tags, as mapping out coordinates on a highway is pretty useful). The tradeoff is strikingly obvious -- does OpenStreetMap want there to be less data but more descriptive data, or more data that meets the bare minimum requirements. 


## Conclusion

I think the whole idea behind OpenStreetMap is not to be an encyclopedia of addresses and maps, but rather a way for people to contribute to an open source map. It's fun, it's neat, and people get to contribute. This is the fundamental idea behind OSM and the tradeoffs for creating specific standards and essentially dictating what the user can enter are not worth it. The idea is to give users nearly complete autonomy with regards to what they can enter or not. Furthermore, a data scientist should be cautioned when using OpenStreetMaps as a reliable source of information. It's good as a precursor to get a high level idea for what a specific boundary entails, but shouldn't necessarily be used to make important business decisions.


```python

```

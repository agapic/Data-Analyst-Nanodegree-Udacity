import pprint
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

# Iterate documents from the cursor
def aggregate(db, pipeline):
    return [doc for doc in db.nycosm.aggregate(pipeline)]

if __name__ == "__main__":
    # Top three religions
    db = get_db('nycosm')
    pipeline = [{"$match": {"religion": {"$exists": 1}}},
                {"$group": {"_id": "$religion", "count": {"$sum":1}}},
                {"$sort": {"count": -1}},
                {"$limit": 3}]
    result = aggregate(db, pipeline)
    pprint.pprint(result)

    # Top 10 leisure areas
    pipeline = [{"$match": {"leisure": {"$exists": 1}}},
                {"$group": {"_id": "$leisure", "count": {"$sum":1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}]
    result = aggregate(db, pipeline)
    pprint.pprint(result)

    # Top 10 amenities
    pipeline = [{"$match":{"amenity":{"$exists":1}, "name":{"$exists":1}, "amenity":"restaurant"}},
                {"$group":{"_id":"$name", "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":10}]
    result = aggregate(db, pipeline)
    pprint.pprint(result)

import pymongo

def db(name='Users', collection='data'):
  cluster = pymongo.MongoClient('Mongo URL')
  
  db = cluster.get_database(name)
  
  udata = db.get_collection(collection)
  return udata

udb = db()

def readSet(uid, val, default=0, db=udb):
    # Query MongoDB using uid as filter (no projection)
    document = db.find_one({"uid": uid})

    # Check if nested field exists in document
    nested_value = document
    nested_fields = val.split('.')
    for field in nested_fields:
        if isinstance(nested_value, dict) and field in nested_value:
            nested_value = nested_value[field]
        else:
            # If nested field does not exist, insert field with default value in database
            nested_value = default
            break
    else:
        # If all nested fields exist, return found value
        return nested_value

    # If document not found or nested field does not exist, insert field with default value in database
    db.update_one({"uid": uid}, {"$set": {val: default}}, upsert=True)
    return default


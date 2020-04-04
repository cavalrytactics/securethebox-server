import os
import pymongo
import time
from bson.json_util import dumps
import json

client = pymongo.MongoClient(
    "mongodb+srv://"+os.environ["MONGODB_USER"]+":"+os.environ["MONGODB_PASSWORD"]+"@"+os.environ["MONGODB_CLUSTER"])
    
# with client.production_securethebox.subscriptions.watch() as stream:
#     while stream.alive:
#         change = stream.try_next()
#         print("Current resume token: %r" % (stream.resume_token,))
#         if change is not None:
#             print("Change document: %r" % (change,))
#             continue
#         time.sleep(10)
        
change = {
    '_id': {
        '_data': '825E86B219000000012B022C0100296E5A10048D65799A5823439FA9AFE9D8B5F3075346645F696400645E86AF761C9D4400003D20C50004'
    }, 
    'operationType': 'replace', 
    'fullDocument': {
        'service': 'testddddkkkk', 
        'result': 'false'
    }, 
    'ns': {
        'db': 'production_securethebox', 
        'coll': 'subscriptions'
    }, 
    'documentKey': {
    }
}

print(change["fullDocument"]["result"])

"""
agent.py is used to fetch tweets from live stream and
store them to db.
"""

import datetime
from twitter import twitterClient
from tools import getConfig
import time
import logging
from models.zombie import Zombie

from pymongo import MongoClient
client = MongoClient()

config = getConfig()
db = client.config['db_name']

logging.debug(db)

tClient = twitterClient(config_dict=config['twitter'])

now = datetime.datetime.now()

todo = db.schedule.find({'start_date': {'$lt': now},
                         'end_date': {'$gte': now}})


logging.basicConfig(level=logging.DEBUG)

logging.debug("Fetching data at %s" % time.ctime())
fetched = tClient.fetch(todo)

#TODO: move to specific object
history = db.zombie
for f in fetched:
    # avoid duplicated tweet
    zz = Zombie()
    #import pdb; pdb.set_trace()
    # rewrite...
    found = history.find({'oid': f['oid']})
    if found.count() == 0:
        try:
            zz.create_zombie(f)
            #history.insert(f)
        except:
            pass

"""
while True:

    now = datetime.datetime.now()
    print now

    todo = db.schedule.find({'date_start': {'$lt': now},
                             'date_end': {'$gte': now}})

    #logging.debug("Fetching data at %s" % time.ctime())
    fetched = tClient.fetch(todo)

    #TODO: move to specific object
    history = db.history
    for f in fetched:
        # avoid duplicated twitt
        found = history.find({'oid': f['oid']})
        if found.count() == 0:
            try:
                history.insert(f)
            except:
                pass

    time.sleep(30)
"""

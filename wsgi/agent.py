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
from mongoengine import *


logging.basicConfig(level=logging.DEBUG)
config = getConfig()

client = connect(config['db_url'])
db = client.config['db_name']

tClient = twitterClient(config_dict=config['twitter'])

now = datetime.datetime.now()

todo = db.schedule.find({'start_date': {'$lt': now},
                         'end_date': {'$gte': now}})

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

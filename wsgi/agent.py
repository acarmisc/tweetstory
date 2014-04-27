"""
agent.py is used to fetch twitts from live stream and
store them to db.
"""

import datetime
from twitter import twitterClient
from tools import getConfig, dbConnect


config = getConfig()
db = dbConnect(config['db_url'], config['db_name'])
tClient = twitterClient(config_dict=config['twitter'])

#while True:

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

#   time.sleep(30)

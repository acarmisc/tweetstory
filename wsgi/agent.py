"""
agent.py is used to fetch tweets from live stream and
store them to db.
"""

import datetime
from twitter import twitterClient
from tools import getConfig
import logging
from models.zombie import Zombie
from models.schedule import Schedule


config = getConfig()

tClient = twitterClient(config_dict=config['twitter'])

now = datetime.datetime.utcnow()

#TODO: prevent duplicate hashtag query
todo = Schedule.objects(start_date__lte=now,
                        end_date__gte=now)

logging.basicConfig(level=logging.DEBUG)

logging.debug("Fetching data at %s" % now)
fetched = tClient.fetch(todo)


for f in fetched:
    found = Zombie.objects(oid=f['oid'])
    if len(found) == 0:
        try:
            zz = Zombie()
            zz.create_zombie(f)
        except:
            pass

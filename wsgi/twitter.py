import os
import tweepy
import time
import pymongo
import ConfigParser


auth = tweepy.OAuthHandler('HUIx9DPeNg3JRhQttArw', 'ZBLfb6ifYbg1S2EeGPi8yoYVZNemQNFmh1Hu2OXRHM')
auth.set_access_token('14421751-IYMHYtG8DBuHYrDkK3Bpf0BftfJo4xseCynkmvFsE', 'XPWW8ZCMC0Ebs5MMNUjPRUVIKIXnYi7AUqPzzIrLWhQ8R')

api = tweepy.API(auth)

config = ConfigParser.RawConfigParser()

if config.read('config.ini'):
    db_url = config.get('mongodb', 'db_url')
    db_name = config.get('mongodb', 'db_name')
else:
    db_url = os.environ['OPENSHIFT_MONGODB_DB_URL']
    db_name = os.environ['OPENSHIFT_APP_NAME']

conn = pymongo.Connection(db_url)
db = conn[db_name]

while True:
    time.sleep(5)
    results = api.search(q="#ballaro")

    for result in results:

        hashtags = []
        for h in result.entities['hashtags']:
            hashtags.append({'tag': h['text']})

        tostore = {'text': result.text,
                   'author': result.author.screen_name,
                   'avatar': result.user.profile_image_url_https,
                   'hashtags': hashtags,
                   'created_at': result.created_at}

        history = db.history
        cid = False
        try:
            cid = history.insert(tostore)
            print cid
        except:
            pass

        print tostore

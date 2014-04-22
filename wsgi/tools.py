import ConfigParser
import os
import pymongo


def getConfig():
    config = ConfigParser.RawConfigParser()

    if config.read('config.ini'):
        db_url = config.get('mongodb', 'db_url')
        db_name = config.get('mongodb', 'db_name')
    else:
        db_url = os.environ['OPENSHIFT_MONGODB_DB_URL']
        db_name = os.environ['OPENSHIFT_APP_NAME']

    consumer_key = os.environ['twitter_consumer_key']
    consumer_secret = os.environ['twitter_consumer_secret']
    key = os.environ['twitter_key']
    secret = os.environ['twitter_secret']

    data = {'db_url': db_url,
            'db_name': db_name,
            'twitter': {
                'consumer_key': consumer_key,
                'consumer_secret': consumer_secret,
                'key': key,
                'secret': secret
            }}

    return data


def dbConnect(db_url, db_name):
    conn = pymongo.Connection(db_url)
    db = conn[db_name]

    return db

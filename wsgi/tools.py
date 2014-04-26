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

    t_api_key = os.environ['t_api_key']
    t_api_secret = os.environ['t_api_secret']
    t_acc_token = os.environ['t_acc_token']
    t_acc_secret = os.environ['t_acc_secret']

    data = {'db_url': db_url,
            'db_name': db_name,
            'twitter': {
                't_api_key': t_api_key,
                't_api_secret': t_api_secret,
                't_acc_token': t_acc_token,
                't_acc_secret': t_acc_secret
            }}

    return data


def dbConnect(db_url, db_name):
    conn = pymongo.Connection(db_url)
    db = conn[db_name]

    return db

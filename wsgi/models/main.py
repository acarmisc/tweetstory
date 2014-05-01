from flask.ext.mongoengine import MongoEngine


def getDb(config):
    me = MongoEngine()
    c = me.connect(config['db_name'], host=config['db_url'])
    db = c.config['db_name']

    return db

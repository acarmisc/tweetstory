from tools import getConfig, dbConnect
import logging


config = getConfig()
db = dbConnect(config['db_url'], config['db_name'])

logging.basicConfig(level=logging.DEBUG)


class User(object):

    def __init__(self, username=False, first_name=False,
                 last_name=False, email=False, password=False,
                 twitter_id=False):

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.twitter_id = twitter_id

    def __repr__(self):
        return '<User %r>' % self.username

    def get_or_create(self):
        found = self.get(username=self.username)
        if not found:
            self.create()

        return self.username

    def get_all(self):
        res = db.users.find()

        return res

    def get(self, username=False):
        if username:
            found = db.users.find({'username': username})

            if found.count() > 0:
                return found
        else:
            return False

    def create(self):

        try:
            db.users.insert(self.__dict__)
            return True
        except:
            logging.error("Error writing new user to database")
            return False

    def check_exists(self):
        found = db.users.find({'username': self.username,
                               'password': self.password})
        if found.count() > 0:
            return found[0]
        else:
            return False

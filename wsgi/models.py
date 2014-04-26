from tools import getConfig, dbConnect
import logging


config = getConfig()
db = dbConnect(config['db_url'], config['db_name'])

logging.basicConfig(level=logging.DEBUG)


class User(object):

    def __init__(self, username, first_name=False,
                 last_name=False, email=False, password=False):

        username = username
        first_name = first_name
        last_name = last_name
        email = email

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get_or_create(self, username):
        if not self.get(username):
            self.create()

        return True

    @staticmethod
    def get(self, username=False):
        if username:
            found = db.users.find({'username': username})

            if found.count() > 0:
                return found
        else:
            return False

    @staticmethod
    def create(self):
        try:
            db.users.create(self)
        except:
            logging.error("Error writing new user to database")

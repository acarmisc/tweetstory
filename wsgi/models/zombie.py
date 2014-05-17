from tools import getConfig, _logger
from zombietweet import db
import datetime


config = getConfig()
_logger = _logger('Models')


class Zombie(db.Document):
    oid = db.StringField(max_length=255, required=True)
    text = db.StringField(max_length=255, required=True)
    author = db.StringField(max_length=255, required=True)
    avatar = db.StringField(required=True)
    hashtags = db.ListField()
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    screen_name = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'hashtags', 'oid'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.oid

    def __repr__(self):
        return '<Zombie %r>' % self.oid

    def getDelta(self, start_date):
        difference = abs((self.created_at - start_date).seconds / 60)
        return difference

    def create_zombie(self, data):
        zombie = Zombie()
        zombie.oid = str(data['oid'])
        zombie.text = data['text']
        zombie.author = data['author']
        zombie.avatar = data['avatar']
        zombie.hashtags = data['hashtags']
        zombie.created_at = data['created_at']
        zombie.screen_name = data['screen_name']

        zombie.save()

        return True

    def get_by_schedule(self, schedule):
        schedule = schedule[0]
        found = Zombie.objects(hashtags__icontains=schedule.hashtag,
                               created_at__gte=schedule.start_date,
                               created_at__lte=schedule.end_date).limit(100)
        return found

    def pack_json(self, llist):
        nlist = []
        for ll in llist:
            nel = {
                'oid': ll.oid,
                'screen_name': ll.screen_name,
                'author': ll.author,
                'created_at': ll.created_at.strftime("%Y-%m-%d %H:%I:%S"),
                'avatar': ll.avatar,
                'id': ll.id.__str__()
            }
            nlist.append(nel)

        return {'zombies': nlist}

    def text_parsed(self):
        from ttp import ttp
        p = ttp.Parser()
        result = p.parse(self.text)
        #TODO: should be done better!
        return result.html.replace('search.twitter.com', 'twitter.com')

    def text_parsed_test(self):
        import re
        URL_REGEX = re.compile(r'''((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')

        return URL_REGEX.sub(r'<a target="_blank" href="\1">\1</a>', self.text)

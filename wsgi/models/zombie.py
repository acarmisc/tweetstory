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
    retweet_count = db.IntField()
    media = db.ListField()

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
        zombie.retweet_count = data['retweet_count']
        zombie.media = data['media']

        zombie.save()

        return True

    def get_by_schedule(self, schedule, slot=False):
        schedule = schedule[0]
        slot = slot or False
        items_per_page = 10
        if slot:
            offset = (int(slot) - 1) * items_per_page

            found = Zombie.objects(hashtags__icontains=schedule.hashtag,
                                   created_at__gte=schedule.start_date,
                                   created_at__lte=schedule.end_date).skip( offset ).limit( items_per_page )
        else:
            #TODO: pagination also for web
            found = Zombie.objects(hashtags__icontains=schedule.hashtag,
                                   created_at__gte=schedule.start_date,
                                   created_at__lte=schedule.end_date).limit(600)

        return found

    def pack_json(self, llist):
        nlist = []
        for ll in llist:
            nel = {
                'oid': ll.oid,
                'screen_name': ll.screen_name,
                'author': ll.author,
                'created_at': ll.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'avatar': ll.avatar,
                'text': ll.text,
                'id': ll.id.__str__()
            }
            nlist.append(nel)

        return {'zombies': nlist}

    def count_links(self, zombies):
        import re
        links = []
        for z in zombies:
            found = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', z.text)
            links += found

        return len(links)

    def get_links(self, zombies):
        import re

        links = []
        for z in zombies:
            found = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', z.text)
            for l in found:
                links.append({'link': l, 'oid': z.oid, 'text': z.text})

        return links

    def count_users(self, zombies):
        users = []
        for z in zombies:
            users += z.author

        users = sorted(set(users))
        return len(users)

    def count_images(self, zombies):
        images = []
        for z in zombies:
            images += z.media

        images = sorted(set(images))
        return len(images)

    def get_photos(self, zombies):
        photos = []
        l = []
        for z in zombies:
            for m in z.media:
                if m not in l:
                    photos.append({'image': m, 'text': z.text})
                    l.append(m)

        return photos

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

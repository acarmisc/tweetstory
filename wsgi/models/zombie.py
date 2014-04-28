from tools import getConfig, _logger
from mytwistory import db
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

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'hashtags', 'oid'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.oid

    def __repr__(self):
        return '<Zombie %r>' % self.oid

    def create_zombie(self, data):
        zombie = Zombie()
        zombie.oid = str(data['oid'])
        zombie.text = data['text']
        zombie.author = data['author']
        zombie.avatar = data['avatar']
        zombie.hashtags = data['hashtags']
        zombie.created_at = data['created_at']

        zombie.save()

        return True

    def get_by_schedule(self, schedule):
        import pdb; pdb.set_trace()
        """
        ffilter = {'$or': [{'hashtags': {'tag': schedule['hashtag']}},
                  {'hashtags': {'tag': schedule['hashtag'].lower()}}]}
        """
        schedule = schedule[0]
        found = Zombie.objects(hashtags__icontains=schedule.hashtag,
                               created_at__gte=schedule.start_date,
                               created_at__lte=schedule.end_date)
        return found

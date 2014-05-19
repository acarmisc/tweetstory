from flask import session
from tools import getConfig, _logger
from zombietweet import db
import datetime


config = getConfig()
_logger = _logger('Models')


class Event(db.Document):
    description = db.StringField(required=True)
    host = db.StringField(max_length=20, required=True)
    type = db.StringField(max_length=255, required=True)
    media = db.StringField(max_length=255, required=True)
    resource_type = db.StringField(max_length=255, required=False)
    resource_id = db.StringField(max_length=255, required=False)
    uid = db.StringField(max_length=255, required=False)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(),
                                  required=True)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'host', 'type'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return '<Event %r>' % self.type

    def remember(self, data=None):
        event = Event()

        if data:
            event.description = data['description']
            event.type = data['type']
            event.media = data['media']
            event.resource_type = data['resource_type']
            event.resource_id = data['resource_id']

        event.host = data['request'].remote_addr

        #TODO: session does not exists in api request
        if 'uid' in session:
            event.uid = session['uid']

        event.save()

        return True

    def get_views_by_schedule(self):
        statistics = {}
        events = Event.objects(resource_id=self.resource_id,
                               resource_type=self.resource_type,
                               description='description')

        statistics['views'] = events.count()

        return statistics

    def get_by_logged_user(self, uid):
        found = Event.objects(uid=uid)

        return found

    def pack_json(self, llist):
        nlist = []
        for ll in llist:
            nel = {
                'id': ll.id.__str__(),
                'created_at': ll.created_at.strftime("%Y-%M-%d %H:%I:%S"),
                'description': ll.description,
                'type': ll.type,
                'media': ll.uid,
                'uid': ll.uid,
            }
            nlist.append(nel)

        return {'events': nlist}

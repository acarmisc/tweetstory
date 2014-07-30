from flask.ext.mongoengine.wtf import model_form
from flask import session
from lib.tools import getConfig, _logger
from zombietweet import db
import datetime


config = getConfig()
_logger = _logger('Models')


class Schedule(db.Document):
    subject = db.StringField(max_length=255, required=True)
    hashtag = db.StringField(max_length=255, required=True)
    start_date = db.DateTimeField(required=False)
    end_date = db.DateTimeField(required=False)
    uid = db.StringField(max_length=255)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(),
                                  required=True)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'hashtag', 'subject'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.subject

    def __repr__(self):
        return '<Schedule %r>' % self.subject

    def create_schedule(self, request, rest=False, delta=0):
        schedule = Schedule()

        if not rest:
            form = ScheduleForm(request.form)

            if request.method == 'POST' and form.validate():
                schedule.subject = form.subject.data
                #TODO: Trim!!!
                schedule.hashtag = form.hashtag.data.replace("#", "")
                schedule.start_date = form.start_date.data - datetime.timedelta(0, delta)
                schedule.end_date = form.end_date.data - datetime.timedelta(0, delta)
                schedule.uid = session['uid']
        else:
            start_date = datetime.datetime.strptime(request['start_date'], '%Y-%m-%d %H:%M:%S')
            end_date = datetime.datetime.strptime(request['end_date'], '%Y-%m-%d %H:%M:%S')

            schedule.subject = request['subject']
            schedule.hashtag = request['hashtag'].replace("#", "")
            schedule.start_date = start_date - datetime.timedelta(0, delta)
            schedule.end_date = end_date - datetime.timedelta(0, delta)
            schedule.uid = session['user']

        res = schedule.save()
        # in produzione sbaglia data
        return res

    def delete(self):
        if Schedule.objects(id=self.id).delete():
            return True
        else:
            return False

    def get_by_logged_user(self, uid, timeadapt=None):
        found = Schedule.objects(uid=uid).order_by('created_at DESC')

        if timeadapt:
            found = self.to_my_time(found)
        return found

    def get_by_id(self):
        return Schedule.objects.get(id=self.id)

    def to_my_time(self, llist):
        for ll in llist:
            ll.start_date = ll.start_date + datetime.timedelta(0, session['utc_offset'])
            ll.end_date = ll.end_date + datetime.timedelta(0, session['utc_offset'])
        return llist

    def get_last(self, limit=False):
        found = Schedule.objects().limit(limit)
        return found

    def count_zombies(self):
        #FIXME: should be done better
        from models.zombie import Zombie
        schedule = Schedule(id=self.id)
        zombie = Zombie()

        schedule = schedule.get_by_id()
        zombies = zombie.get_by_schedule(schedule)
        return zombies.count()

    def pack_json(self, llist):
        nlist = []
        for ll in llist:
            nel = {
                'id': ll.id.__str__(),
                'created_at': ll.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'end_date': ll.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                'hashtag': ll.hashtag,
                'start_date': ll.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'subject': ll.subject,
                'uid': ll.uid,
            }
            nlist.append(nel)

        return {'schedules': nlist}

    def get_running(self):
        now = datetime.datetime.utcnow()
        todo = Schedule.objects(start_date__lte=now,
                                end_date__gte=now)

        return todo

    def get_author(self):
        from models.user import User
        user = User(username=self.uid)
        return user.get_by_username()

    def count_images(self):
        from models.zombie import Zombie
        schedule = Schedule(id=self.id)
        zombie = Zombie()

        schedule = schedule.get_by_id()

        zombies = zombie.get_by_schedule(schedule)
        return zombie.count_images(zombies)

    def get_media(self):
        from models.zombie import Zombie
        schedule = Schedule(id=self.id)
        schedule = schedule.get_by_id()

        zombie = Zombie()
        zombies = zombie.get_by_schedule(schedule)

        photos = zombie.get_photos(zombies)

        return photos


ScheduleForm = model_form(Schedule)

ScheduleSimpleForm = model_form(Schedule,
                                only=['subject', 'hashtag',
                                      'start_date', 'end_date'])

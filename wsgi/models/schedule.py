from flask.ext.mongoengine.wtf import model_form
from flask import session
from tools import getConfig, _logger
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

        schedule.save()

        return True

    def delete(self):
        if Schedule.delete():
            return True
        else:
            return False

    def get_by_logged_user(self, uid, timeadapt=None):
        found = Schedule.objects(uid=uid)

        if timeadapt:
            found = self.to_my_time(found)
        return found

    def get_by_id(self, id):
        found = Schedule.objects(id=id)
        return found

    def to_my_time(self, llist):
        for ll in llist:
            ll.start_date = ll.start_date + datetime.timedelta(0, session['utc_offset'])
            ll.end_date = ll.end_date + datetime.timedelta(0, session['utc_offset'])
        return llist

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


ScheduleForm = model_form(Schedule)

ScheduleSimpleForm = model_form(Schedule,
                                only=['subject', 'hashtag',
                                      'start_date', 'end_date'])

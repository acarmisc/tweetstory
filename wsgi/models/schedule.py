from flask.ext.mongoengine.wtf import model_form
from flask import session
from tools import getConfig, _logger
from zombietweet import db
import datetime


config = getConfig()
_logger = _logger('Models')


class Schedule(db.Document):
    subject = db.StringField(max_length=255, required=True)
    hashtag = db.StringField(max_length=255, required=False)
    start_date = db.DateTimeField(default=datetime.datetime.utcnow(),
                                  required=True)
    end_date = db.DateTimeField(default=datetime.datetime.utcnow(),
                                required=True)
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

    def create_schedule(self, request):
        schedule = Schedule()

        if 'form' in request:
            form = ScheduleForm(request.form)

            if request.method == 'POST' and form.validate():
                schedule.subject = form.subject.data
                schedule.hashtag = form.hashtag.data
                schedule.start_date = form.start_date.data
                schedule.end_date = form.end_date.data
                schedule.uid = session['uid']
        else:
            schedule.subject = request['subject']
            schedule.hashtag = request['hashtag']
            schedule.start_date = request['start_date']
            schedule.end_date = request['end_date']
            schedule.uid = session['user']

        schedule.save()

        return True

    def get_by_logged_user(self, uid):
        found = Schedule.objects(uid=uid)
        return found

    def get_by_id(self, id):
        found = Schedule.objects(id=id)
        return found


ScheduleForm = model_form(Schedule)

ScheduleSimpleForm = model_form(Schedule,
                                only=['subject', 'hashtag',
                                      'start_date', 'end_date'])

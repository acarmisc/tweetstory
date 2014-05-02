from flask.ext.mongoengine.wtf import model_form

from tools import getConfig, _logger
from mytwistory import db
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
    uid = db.StringField(max_length=255, required=True)
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
        form = ScheduleForm(request.form)
        import pdb; pdb.set_trace()
        if request.method == 'POST' and form.validate():
            schedule = Schedule()
            schedule.subject = form.subject.data
            schedule.hashtag = form.hashtag.data
            schedule.start_date = form.start_date.data
            schedule.end_date = form.end_date.data
            schedule.uid = form.uid.data

            schedule.save()

        return True

    def get_by_logged_user(self, uid):
        found = Schedule.objects(uid=uid)
        return found

    def get_by_id(self, id):
        found = Schedule.objects(id=id)
        return found


ScheduleForm = model_form(Schedule)

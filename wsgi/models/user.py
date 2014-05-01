from flask.ext.mongoengine.wtf import model_form

from tools import getConfig, _logger
from mytwistory import db
import datetime


config = getConfig()
_logger = _logger('Models')


class User(db.Document):
    username = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=False)
    first_name = db.StringField(max_length=255, required=False)
    last_name = db.StringField(max_length=255, required=False)
    email = db.StringField(max_length=255, required=False)
    twitter_id = db.StringField(max_length=255, required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    last_login = db.DateTimeField(required=False)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'username'],
        'ordering': ['-created_at']
    }

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username

    def create_user(self, request):
        form = self.UserForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User()
            user.username = form.username.data
            user.password = form.password.data
            user.email = form.email.data

            user.save()

        return True

    def check_exists(self):
        found = User.objects(username=self.username,
                             password=self.password)

        if len(found) > 0:
            return found[0]
        else:
            return False

    def UserForm():
        return model_form(User)

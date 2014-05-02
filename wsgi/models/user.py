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
    email = db.EmailField()
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

    def create_user(self):
        self.save()

        return True

    def create_from_request(self, request):
        form = UserForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User()
            user.username = form.username.data
            user.password = form.password.data
            user.email = form.email.data

            user.create_user()

        return True

    def check_exists(self):
        found = User.objects(username=self.username,
                             password=self.password)

        if len(found) > 0:
            return found[0]
        else:
            return False

    def get_or_create(self):
        found = self.check_exists()
        if not found:
            self.to_mongo()
            self.save()
            return self.username
        else:
            return found.username

    def get_all(self):
        return User.objects()

UserForm = model_form(User)

UserSmallForm = model_form(User, only=['first_name', 'last_name', 'username',
                                       'password', 'email'])

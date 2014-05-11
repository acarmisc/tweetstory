from flask.ext.mongoengine.wtf import model_form
from tools import getConfig, _logger
from zombietweet import db
import datetime
import uuid


config = getConfig()
_logger = _logger('Models')


class User(db.Document):
    username = db.StringField(max_length=255, required=True, unique=True)
    password = db.StringField(max_length=255, required=False)
    first_name = db.StringField(max_length=255, required=False)
    last_name = db.StringField(max_length=255, required=False)
    email = db.EmailField()
    twitter_id = db.StringField(max_length=255, required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    last_login = db.DateTimeField(required=False)
    token = db.StringField(max_length=255, required=True)
    time_zone = db.StringField(max_length=255)
    utc_offset = db.IntField()
    profile_image_url = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'username'],
        'ordering': ['-created_at']
    }

    @property
    def __unicode__(self):
        return self.username

    @property
    def __repr__(self):
        return '<User %r>' % self.username

    def get_my_now(self):
        now = datetime.datetime.now()
        return now + datetime.timedelta(0, self.utc_offset)

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

    def get_by_id(self):
        return User.objects.get(id=self.id)

    def get_or_create(self):
        found = self.check_exists()
        self.token = uuid.uuid4().hex
        if not found:
            self.to_mongo()
            self.save()
            return self
        else:
            return found

    def get_all(self):
        return User.objects()

    def get_by_username(self):
        return User.objects.get(username=self.username)

    def get_token(self):
        return User.objects.get(username=self.username).token

UserForm = model_form(User)

UserSmallForm = model_form(User, only=['first_name', 'last_name',
                                       'email', 'time_zone', 'utc_offset',
                                       'token'])


class Group(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {'allow_inheritance': True,
            'indexes': ['-created_at', 'name'],
            'ordering': ['-created_at']
            }

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Group %r>' % self.name

    def create_group(self):
        self.save()

        return True

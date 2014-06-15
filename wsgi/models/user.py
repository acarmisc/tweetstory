from flask.ext.mongoengine.wtf import model_form
from lib.tools import getConfig, _logger
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
    first_login = db.BooleanField(default=True)

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

    def update_user(self):
        try:
            self.update(set__first_name=self.first_name,
                        set__last_name=self.last_name,
                        set__email=self.email,
                        set__first_login=False)
        except RuntimeError:
            pass

        return True

    def get_or_create(self):
        found = self.check_exists()
        self.token = uuid.uuid4().hex
        if not found:
            self.to_mongo()
            self.save()
            return self
        else:
            #TODO: update user data from live
            #get_live_userdata
            return found

    def get_all(self):
        return User.objects()

    def get_by_username(self):
        return User.objects.get(username=self.username)

    def get_token(self):
        return User.objects.get(username=self.username).token

    def get_last(self, limit=False):
        return User.objects().limit(limit)

    def count_schedule(self):
        from models.schedule import Schedule
        return Schedule.objects(uid=self.username).count()

    def count_followers(self):
        return Relationship.objects(username=self.id).count()

    def get_followers(self):
        return Relationship.objects(username=self.id)

    def count_likes(self):
        return 0

    def get_live_userdata(self):
        from twitter import twitterClient
        config = getConfig()
        tClient = twitterClient(config_dict=config['twitter'])

        mydata = tClient.get_user(self.username)
        return mydata

    def check_following(self, follower):
        relation = Relationship(username=self.id, follower=follower)

        return relation.exists()

    def get_events(self, limit=False):
        from models.event import Event
        from models.schedule import Schedule

        event = Event(uid=self.username)
        events = []
        for e in event.get_my_events('events'):
            if e.resource_type == 'user':
                resource_name = User(id=e.resource_id).get_by_id().username
                url_prefix = '/user/' + e.resource_id
            elif e.resource_type == 'schedule':
                resource_name = Schedule(id=e.resource_id).get_by_id().subject
                url_prefix = '/show/' + e.resource_id

            el = {
                'owner': e.uid,
                'description': e.description,
                'resource_type': e.resource_type,
                'resource_id': e.resource_id,
                'resource_name': resource_name,
                'created_at': e.created_at,
                'url': url_prefix
            }
            events.append(el)

        return events

    def get_from_twitter(self):
        from zombietweet import tClient
        user = tClient.get_user(self.username)

        return user


UserForm = model_form(User)

UserSmallForm = model_form(User, only=['first_name', 'last_name',
                                       'email', 'time_zone', 'utc_offset',
                                       'token'])


class Relationship(db.Document):
    follower = db.ReferenceField('User')
    username = db.ReferenceField('User')
    type = db.StringField(max_length=255, required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

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
        return '<Relationship %r>' % self.username

    def get_by_data(self):
        return Relationship.objects(username=self.username, follower=self.follower)

    def create(self):
        check = Relationship.objects(username=self.username,
                                     follower=self.follower).count()

        if check < 1:
            try:
                self.save()
            except:
                return False
        else:
            return False

    def delete(self):
        if Relationship.delete():
            return True
        else:
            return False

    def exists(self):
        return True if Relationship.objects(username=self.username,
                                            follower=self.follower).count() > 0 else False

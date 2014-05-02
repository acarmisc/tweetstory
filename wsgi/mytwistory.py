from flask import Flask, render_template, request, \
    session, redirect, url_for, flash
from tools import getConfig, _logger
from twitter import twitterClient
from flask.ext.mongoengine import MongoEngine

config = getConfig()
_logger = _logger('Core')

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MONGODB_SETTINGS'] = {'DB': config['db_name'],
                                  'host': config['db_url']}

tClient = twitterClient(config_dict=config['twitter'])
twitter = tClient.authenticate()

db = MongoEngine(app)

from models.user import User, UserForm
from models.schedule import Schedule, ScheduleForm
from models.zombie import Zombie

""" basic functions """


@app.route("/")
def welcome():
    form = UserForm()
    if 'logged_in' in session:
        return redirect(url_for('list'))

    return render_template('login.html', form=form)


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                             next=None))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))


@app.route('/post_login')
def post_login():
    user = User(username=session['twitter_user'],
                twitter_id=session['twitter_id'])

    session['user'] = user.get_or_create()
    session['logged_in'] = True

    return redirect(url_for('list'))


@app.route('/login_local', methods=['POST'])
def login_local():
    user = User(username=request.form.get('username'),
                password=request.form.get('password'))

    check = user.check_exists()
    if check:
        # get more data from check
        session['user'] = check.username
        session['logged_in'] = True
        flash('You were signed in as %s' % session['user'])
        return redirect(url_for('list'))
    else:
        flash('Login failed')
        return redirect(url_for('/'))


@app.route('/signup', methods=['POST'])
def signup():
    user = User()

    if user.create_user(request):
        return redirect(url_for('users'))
    else:
        return redirect(url_for('/'))


@app.route("/list")
def list():
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    schedules = Schedule()
    results = schedules.get_by_logged_user(session['user'])
    form = ScheduleForm()

    return render_template('list.html', entries=results, form=form)


@app.route('/save', methods=['POST'])
def save():
    schedule = Schedule()
    schedule.create_schedule(request)

    return list()


@app.route("/show/<id>", methods=['GET'])
def show(id=None):
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    # getting schedule
    schedule = Schedule()
    schedule = schedule.get_by_id(id)

    # getting zombie related to specific schedule
    zombie = Zombie()
    zombies = zombie.get_by_schedule(schedule)

    # should return schedule and zombies
    return render_template('show.html', schedule=schedule, zombies=zombies)


""" Twitter login part """


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = url_for('post_login')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    session['twitter_id'] = resp['user_id']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


""" basic admin """


@app.route('/users')
def users():
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    u = User()
    users = u.get_all()

    return render_template('users.html', users=users)


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yXaRGXHH!jmN]LWX/d?RT'
    app.run(debug=True)

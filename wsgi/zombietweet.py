from flask import Flask, render_template, request, \
    session, redirect, url_for, flash
from tools import getConfig, _logger
from twitter import twitterClient
from flask.ext.mongoengine import MongoEngine
import datetime


__version__ = 0.3

config = getConfig()
_logger = _logger('Core')

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MONGODB_SETTINGS'] = {'DB': config['db_name'],
                                  'host': config['db_url']}
app.config['TWITTER'] = config['twitter']


db = MongoEngine(app)

import schedules
import admin
import api

import twitter_security

""" basic functions """


@app.route("/")
def welcome():
    if 'logged_in' in session:
        return redirect(url_for('list'))

    return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    context = {}

    schedule = Schedule()
    user = User()

    context['last_schedules'] = schedule.get_last(8)
    context['last_users'] = user.get_last(8)
    context['running'] = schedule.get_running()

    return render_template('dashboard.html', context=context)


""" security """


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))


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

    user = tClient.get_user(resp['screen_name'])
    user = {
        'time_zone': user.time_zone,
        'utc_offset': user.utc_offset,
        'profile_image_url': user.profile_image_url
    }

    session['twitter_data'] = user

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route('/post_login')
def post_login():
    user = User(username=session['twitter_user'],
                twitter_id=session['twitter_id'],
                time_zone=session['twitter_data']['time_zone'],
                utc_offset=session['twitter_data']['utc_offset'],
                profile_image_url=session['twitter_data']['profile_image_url'])

    user = user.get_or_create()
    session['user'] = user.username
    session['user_id'] = user.id.__str__()
    session['utc_offset'] = user.utc_offset or 0
    session['uid'] = session['user']
    session['logged_in'] = True
    session['profile_image_url'] = user.profile_image_url

    if user.first_login:
        flash('This is your first login. Please fill up the fields.')
        return redirect(url_for('get_user', id=user.id))
    else:
        return redirect(url_for('list'))


""" schedules """


@app.route("/list")
def list():
    from models.schedule import ScheduleSimpleForm
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    schedules = Schedule()
    results = schedules.get_by_logged_user(session['user'], timeadapt=True)

    form = ScheduleSimpleForm()
    now = datetime.datetime.utcnow() + \
        datetime.timedelta(0, session['utc_offset'])

    defaults = {
        'start_date': now.strftime("%Y-%m-%d %H:%M:%S")
    }

    return render_template('list.html', entries=results, form=form,
                           defaults=defaults)


@app.route('/save', methods=['POST'])
def save():
    schedule = Schedule()
    schedule.create_schedule(request, rest=False, delta=session['utc_offset'])

    return list()


@app.route('/delete_schedule/<id>', methods=['GET'])
def delete_schedule(id=None):
    schedule = Schedule()
    schedule = schedule.get_by_id(id)
    schedule.delete()

    return redirect(url_for('list'))


@app.route("/show/<id>", methods=['GET'])
def show(id=None):
    # getting schedule
    schedule = Schedule()
    schedule = schedule.get_by_id(id)

    # getting zombie related to specific schedule
    zombie = Zombie()
    zombies = zombie.get_by_schedule(schedule)

    # getting statistics
    # TODO: statics should be collected in one cycle!!
    statistics = {}
    event = Event(resource_id=id, resource_type='schedule')
    #statistics['views'] = event.get_views_by_schedule()
    statistics['stars'] = event.get_stars_by_schedule()
    statistics['links'] = zombie.count_links(zombies)
    statistics['users'] = zombie.count_users(zombies)
    statistics['images'] = zombie.count_images(zombies)
    statistics['zombies'] = zombies.count()

    photos = zombie.get_photos(zombies)
    links = zombie.get_links(zombies)

    # should return schedule and zombies
    return render_template('show.html', schedule=schedule[0],
                           zombies=zombies,
                           statistics=statistics,
                           photos=photos,
                           links=links)


@app.route("/share/<id>", methods=['GET'])
def share(id=None):
    return redirect(url_for('show', id=id))


""" basic admin """


@app.route('/users')
def users():
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    u = User()
    users = u.get_all()

    return render_template('users.html', users=users)


@app.route("/user/<id>", methods=['GET', 'POST'])
def get_user(id=None):
    from models.user import UserSmallForm
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    user = User(id=id)
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', None)
        user.last_name = request.form.get('last_name', None)
        user.email = request.form.get('email', None)
        user.update_user()

    user = user.get_by_id()

    form = UserSmallForm(obj=user)

    schedule = Schedule(uid=id)
    schedules = schedule.get_by_logged_user(session['user'], timeadapt=True)

    return render_template('user.html', user=user, form=form,
                           schedules=schedules)


@app.route("/save_user/<id>", methods=['POST'])
def save_user(id=None):
    return users()


""" PRO """


@app.route('/pro')
def pro():
    return render_template('pro/index.html')


""" API """
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify

auth = HTTPBasicAuth()


@app.route("/version")
def get_version():
    return jsonify({'version': __version__})


@auth.get_password
def get_password(username):
    user = User(username=username)

    if user.check_exists():
        return user.get_token()
    else:
        return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/api/whoiam/<username>')
def whoiam(username):
    user = User(username=username)
    token = user.get_token()
    return make_response(jsonify({'response': token}), 200)


@app.route('/api/post_login', methods=['POST'])
def api_post_login():
    if not request.json or not 'twitter_user' in request.json:
        return jsonify({'error': 'Malformed request'}), 400

    user = User(username=request.json.get('twitter_user', ""),
                twitter_id=request.json.get('twitter_id', ""),
                time_zone=request.json.get('time_zone', ""),
                utc_offset=request.json.get('utc_offset', ""),
                profile_image_url=request.json.get('profile_image_url', "")
                )

    logged_user = user.get_or_create()
    #TODO: to be checked
    return make_response(jsonify({'response': logged_user.get_token()}))


@app.route('/api/status')
@auth.login_required
def api_status():
    return make_response(jsonify({'response': 'Service online'}), 200)


@app.route('/api/get_schedules')
@auth.login_required
def get_schedules():
    Event().remember({'request': request,
                      'description': 'get_schedules',
                      'resource_type': 'schedule',
                      'resource_id': '',
                      'media': 'api',
                      'type': 'statistic',
                      'uid': auth.username()})

    schedules = Schedule()
    results = schedules.get_by_logged_user(auth.username())
    return jsonify(schedules.pack_json(results))


@app.route('/<path:fullurl>')
@auth.login_required
def get_zombies(fullurl):
    params = fullurl.split('/')
    id = params[2]
    if len(params) > 3:
        slot = params[3]
    else:
        slot = False

    Event().remember({'request': request,
                      'description': 'get_zombies',
                      'resource_type': 'zombies',
                      'resource_id': id,
                      'media': 'api',
                      'type': 'statistic',
                      'uid': auth.username()})

    schedule = Schedule()
    schedule = schedule.get_by_id(id)

    zombie = Zombie()
    results = zombie.get_by_schedule(schedule, slot=slot)
    return jsonify(zombie.pack_json(results))


@app.route('/api/create_schedule', methods=['POST'])
@auth.login_required
def api_create_schedule():
    if not request.json or not 'subject' in request.json:
        return jsonify({'error': 'Malformed request'}), 400

    Event().remember({'request': request,
                      'description': 'create_schedule',
                      'resource_type': 'schedule',
                      'resource_id': '0',
                      'media': 'api',
                      'type': 'statistic',
                      'uid': auth.username()})

    data = {
        'subject': request.json.get('subject', ""),
        'hashtag': request.json.get('hashtag', ""),
        'start_date': request.json.get('start_date', ""),
        'end_date': request.json.get('end_date', "")
    }
    session['user'] = auth.username()
    schedule = Schedule()
    schedule.create_schedule(data, rest=True)
    return get_schedules()


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yXaRGXHH!jmN]LWX/d?RT'
    app.run(debug=True)

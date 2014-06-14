from flask import Flask, render_template, \
    session, redirect, url_for, flash
from lib.tools import getConfig, _logger
from lib.twitter import twitterClient
from flask.ext.mongoengine import MongoEngine


__version__ = 0.3

config = getConfig()
_logger = _logger('Core')

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MONGODB_SETTINGS'] = {'DB': config['db_name'],
                                  'host': config['db_url']}

tClient = twitterClient(config_dict=config['twitter'])
twitter = tClient.authenticate()

db = MongoEngine(app)

import routes

""" basic functions """


@app.route("/")
def welcome():
    from models.user import UserSmallForm
    form = UserSmallForm()
    if 'logged_in' in session:
        return redirect(url_for('list'))

    return render_template('login.html', form=form)


@app.route("/dashboard")
def dashboard():
    from models.user import User
    from models.schedule import Schedule
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    context = {}

    schedule = Schedule()
    user = User()

    context['last_schedules'] = schedule.get_last(8)
    context['last_users'] = user.get_last(8)
    context['running'] = schedule.get_running()

    return render_template('dashboard.html', context=context)


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


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yXaRGXHH!jmN]LWX/d?RT'
    app.run(debug=True)

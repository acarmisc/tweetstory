from flask import Flask, render_template, request, session, redirect, url_for, flash
import datetime
from bson.objectid import ObjectId
import logging
from tools import getConfig, dbConnect
from twitter import twitterClient
from flask_oauth import OAuth
from models import User


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

config = getConfig()
db = dbConnect(config['db_url'], config['db_name'])

tClient = twitterClient(config_dict=config['twitter'])

logging.basicConfig(level=logging.DEBUG)


""" Twitter login part """

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=config['twitter']['t_api_key'],
    consumer_secret=config['twitter']['t_api_secret']
)

loggin.debug(config['twitter']['t_api_key'])
logging.debug(config['twitter']['t_api_secret'])


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                             next=None))


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


@app.route('/post_login')
def post_login():
    user = User(username=session['twitter_user'], twitter_id=session['twitter_id'])

    session['user'] = user.get_or_create()

    return redirect(url_for('list'))


""" Main applications logic starts here """


@app.route('/logout')
def logout():
    session.clear()
    return "clear"


@app.route('/login_local', methods=['POST'])
def login_local():
    pass


@app.route('/signup', methods=['POST'])
def signup():

    user = User(username=request.form.get('username', None),
                email=request.form.get('email', None),
                password=request.form.get('password', None))

    if user.create():
        return redirect(url_for('users'))
    else:
        return redirect(url_for('/'))


@app.route('/users')
def users():
    u = User()
    users = u.get_all()

    return render_template('users.html', users=users)


@app.route('/save', methods=['POST'])
def save():
    tostore = {
        'date_start': datetime.datetime.strptime(request.form.get('date_start', None),
                                                 "%Y-%m-%d %H:%M:%S"),
        'date_end': datetime.datetime.strptime(request.form.get('date_end', None),
                                               "%Y-%m-%d %H:%M:%S"),
        'subject': request.form.get('subject', None),
        'hashtag': request.form.get('hashtag', None)
    }

    db.schedule.insert(tostore)

    return list()


@app.route("/list")
def list():
    result = db.schedule.find().sort('created_at', -1)

    return render_template('list.html', entries=result)


@app.route("/show/<id>", methods=['GET'])
def show(id=None):

    schedule = db.schedule.find_one({'_id': ObjectId(id)})

    ffilter = {'$or': [{'hashtags': {'tag': schedule['hashtag']}},
                       {'hashtags': {'tag': schedule['hashtag'].lower()}}]}
    result = db.history.find(ffilter).sort('created_at', -1)

    return render_template('show.html', entries=result)


@app.route("/")
def welcome():
    return render_template('login.html')

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yXaRGXHH!jmN]LWX/d?RT'
    app.run(debug=True)

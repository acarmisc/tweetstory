from flask import Flask, render_template, request, session, redirect, url_for, flash
import datetime
from bson.objectid import ObjectId
import logging
from tools import getConfig, dbConnect
from twitter import twitterClient
from flask_oauth import OAuth


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

config = getConfig()
db = dbConnect(config['db_url'], config['db_name'])

tClient = twitterClient(config_dict=config['twitter'])

logging.basicConfig(level=logging.DEBUG)


"""
Twitter login part
"""

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=config['twitter']['consumer_key'],
    consumer_secret=config['twitter']['consumer_secret']
)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


""" Main applications logic starts here """


@app.route('/save', methods=['POST'])
def save():

    tostore = {
        'date_start': datetime.datetime.strptime(request.form['date_start'],
                                                 "%Y-%m-%d %H:%M:%S"),
        'date_end': datetime.datetime.strptime(request.form['date_end'],
                                               "%Y-%m-%d %H:%M:%S"),
        'subject': request.form['subject'],
        'description': request.form['description'],
        'hashtag': request.form['hashtag']
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
    return list()


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yXaR~XHH!jmN]LWX/d?RT'
    app.run(debug=True)

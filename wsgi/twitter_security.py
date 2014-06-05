from flask import Flask, render_template, request, \
    session, redirect, url_for, flash
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify

from twitter import twitterClient

from zombietweet import app, db

from models.user import User
from models.schedule import Schedule
from models.zombie import Zombie
from models.event import Event


tClient = twitterClient(config_dict=app.config['TWITTER'])
twitter = tClient.authenticate()


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                             next=None))


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
    session['utc_offset'] = user.utc_offset
    session['uid'] = session['user']
    session['logged_in'] = True
    session['profile_image_url'] = user.profile_image_url

    if user.first_login:
        flash('This is your first login. Please fill up the fields.')
        return redirect(url_for('get_user', id=user.id))
    else:
        return redirect(url_for('list'))

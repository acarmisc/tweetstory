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


""" security """


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yXaRGXHH!jmN]LWX/d?RT'
    app.run(debug=True)

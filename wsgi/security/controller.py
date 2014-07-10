from flask import session, redirect, url_for, flash, request, render_template
from lib.tools import _logger

from zombietweet import app, twitter
from models.user import User
from models.event import Event


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                             next=None))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))


@app.route('/first_login/<id>')
def first_login(id=None):
    from models.user import UserSmallForm
    if 'logged_in' not in session:
        return redirect(url_for('welcome'))

    user = User(id=id)
    user = user.get_by_id()

    form = UserSmallForm(obj=user)

    return render_template('first_login.html', user=user, form=form)


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
        return redirect(url_for('first_login', id=user.id))
    else:
        return redirect(url_for('list'))

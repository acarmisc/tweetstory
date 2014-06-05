from flask import Flask, render_template, request, \
    session, redirect, url_for, flash
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify

from zombietweet import app, db

from models.user import User
from models.schedule import Schedule
from models.zombie import Zombie
from models.event import Event


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

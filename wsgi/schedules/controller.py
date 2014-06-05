from flask import Flask, render_template, request, \
    session, redirect, url_for, flash
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import jsonify

import datetime

from zombietweet import app, db

from models.user import User
from models.schedule import Schedule
from models.zombie import Zombie
from models.event import Event


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
    statistics['views'] = event.get_views_by_schedule()
    statistics['stars'] = event.get_stars_by_schedule()
    statistics['links'] = zombie.count_links(zombies)
    statistics['users'] = zombie.count_users(zombies)
    statistics['images'] = zombie.count_images(zombies)

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

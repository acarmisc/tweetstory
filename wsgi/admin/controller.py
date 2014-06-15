from flask import render_template, request, \
    session, redirect, url_for, jsonify
from lib.tools import _logger

from zombietweet import app

from models.user import User
from models.schedule import Schedule
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
    schedules = schedule.get_by_logged_user(user.username, timeadapt=True)

    return render_template('user.html', user=user, form=form,
                           schedules=schedules)


@app.route("/user/checkFollowing", methods=['POST'])
def check_following():
    if not request.json:
        return jsonify({'error': 'Malformed request'}), 400

    user = User(id=request.json.get('username', None))
    if user.check_following(session['user_id']):
        return jsonify({'label': "Unfollow", 'action': "unfollow"})
    else:
        return jsonify({'label': "Follow", 'action': "follow"})


@app.route("/user/relate", methods=['POST'])
def relate_users():
    if not request.json:
        return jsonify({'error': 'Malformed request'}), 400

    from models.user import Relationship
    relation = Relationship(username=request.json.get('username', None),
                            follower=session['user_id'])
    relation.create()

    Event().remember({'request': request,
                    'description': 'follow',
                    'resource_type': 'user',
                    'resource_id': request.json.get('username'),
                    'media': 'core',
                    'type': 'events',
                    'uid': session['user_id']})

    return jsonify({'response': "Relation created."})


@app.route("/user/unrelate", methods=['POST'])
def unrelate_users():
    if not request.json:
        return jsonify({'error': 'Malformed request'}), 400

    from models.user import Relationship
    relation = Relationship(username=request.json.get('username', None),
                            follower=session['user_id'])
    relation = relation.get_by_data()
    relation.delete()

    Event().remember({'request': request,
                    'description': 'unfollow',
                    'resource_type': 'user',
                    'resource_id': request.json.get('username'),
                    'media': 'core',
                    'type': 'events',
                    'uid': session['user_id']})

    return jsonify({'response': "Relation deleted."})


@app.route("/user/get_from_twitter", methods=['POST'])
def get_from_twitter():
    if not request.json:
        return jsonify({'error': 'Malformed request'}), 400

    user = User(username=request.json.get('username')).get_from_twitter()

    result = {
        'description': user.description,
        'location': user.location,
        'head_bg': user.profile_background_image_url,
        'head_color': user.profile_background_color,
    }
    return jsonify({'response': result})


@app.route("/save_user/<id>", methods=['POST'])
def save_user(id=None):
    return users()

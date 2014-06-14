from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response, jsonify, session, request

from zombietweet import app

from models.user import User
from models.schedule import Schedule
from models.zombie import Zombie
from models.event import Event

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

import os
from flask import Flask, render_template
import pymongo
import ConfigParser


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route("/test")
def test():

    config = ConfigParser.RawConfigParser()

    if config.read('config.ini'):
        db_url = config.get('mongodb', 'db_url')
        db_name = config.get('mongodb', 'db_name')
    else:
        db_url = os.environ['OPENSHIFT_MONGODB_DB_URL']
        db_name = os.environ['OPENSHIFT_APP_NAME']

    conn = pymongo.Connection(db_url)
    db = conn[db_name]

    result = db.history.find()

    #turn the results into valid JSON
    #return jsonify({'results': result})
    return render_template('test.html', entries=result)


#need this in a scalable app so that HAProxy thinks the app is up
@app.route("/")
def blah():
    return "hello world"

if __name__ == "__main__":
    app.run()
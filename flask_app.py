from flask import Flask, render_template, request
from git.repo import Repo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="AGSolarEngineers",
    password="AGSolar2023DB",
    hostname="AGSolarEngineers.mysql.pythonanywhere-services.com",
    databasename="AGSolarEngineers$projects",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = Repo('./AGSolarEngineers')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    db = SQLAlchemy(app)
    app.run(host='127.0.0.1', port=8000, debug=True)
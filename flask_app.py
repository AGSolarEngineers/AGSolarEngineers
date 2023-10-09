from flask import Flask, redirect, render_template, request, url_for
from git.repo import Repo
from flask_sqlalchemy import SQLAlchemy
from api import api
app = Flask(__name__)

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="AGSolarEngineers",
#     password="AGSolar2023DB",
#     hostname="AGSolarEngineers.mysql.pythonanywhere-services.com",
#     databasename="AGSolarEngineers$projects",
# )
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

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
    print(api.theme)
    return render_template('index.html', theme=api.theme)

@app.route('/toggle-theme')
def toggle_theme():
    api.theme = 'light' if api.theme != 'light' else 'dark'
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
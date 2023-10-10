import math
from flask import Flask, redirect, render_template, request, url_for
from git.repo import Repo
from flask_sqlalchemy import SQLAlchemy
from api import api
from controller.estrutura import Estrutura
app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="AGSolarEngineers",
    password="AGSolar2023DB",
    hostname="AGSolarEngineers.mysql.pythonanywhere-services.com",
    databasename="AGSolarEngineers$projects",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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

@app.route('/estrutura', methods=('GET', 'POST'))
def estrutura():
    structure = Estrutura(0, 0, 0, False)
    default_module_length=1055
    default_module_amount = 300
    default_table_amount=1
    if request.method == "POST":
        module_length = request.form['txt_module_length']
        module_amount = request.form['txt_module_amount']
        table_amount = request.form['txt_table_amount']
        default_module_length = module_length
        default_module_amount = module_amount
        default_table_amount = table_amount
        try:
            request.form['chk_inverter']
            inverter_table = True
        except:
            inverter_table = False
        structure = Estrutura(int(module_length), int(module_amount), int(table_amount), inverter_table)
    return render_template('estrutura.html', default_module_length=default_module_length, default_module_amount=default_module_amount, default_table_amount=default_table_amount, structure=structure, active='Estrutura', theme=api.theme)

@app.route('/concreto', methods=('GET', 'POST'))
def concreto():
    default_base_amount = 0
    default_height_buried = 1.6
    default_ray_buried = 0.15
    default_height_exposed = 0.4
    default_ray_exposed = 0.2

    if request.method == "POST":
        base_amount = request.form['txt_base_amount']
        default_base_amount = float(base_amount)
        height_buried = request.form['txt_height_buried']
        default_height_buried = float(height_buried)
        ray_buried = request.form['txt_ray_buried']
        default_ray_buried = float(ray_buried)
        height_exposed = request.form['txt_height_exposed']
        default_height_exposed = float(height_exposed)
        ray_exposed = request.form['txt_ray_exposed']
        default_ray_exposed = float(ray_exposed)

    default_volume_buried = math.pi*(default_ray_buried**2.0)*default_height_buried
    default_volume_exposed = math.pi*(default_ray_exposed**2.0)*default_height_exposed
    default_volume_per_base = default_volume_buried+default_volume_exposed
    default_volume_total = math.ceil(default_base_amount*default_volume_per_base*1.1)
    default_feature = "H21"
        
    return render_template("concreto.html", active='Estrutura', default_base_amount=default_base_amount,
                            default_height_buried=default_height_buried, default_ray_buried=default_ray_buried, default_volume_buried=default_volume_buried, 
                            default_height_exposed=default_height_exposed, default_ray_exposed=default_ray_exposed, default_volume_exposed=default_volume_exposed, 
                            default_volume_per_base=default_volume_per_base, default_volume_total=default_volume_total, default_feature=default_feature, theme=api.theme)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
import math
from flask import Flask, redirect, render_template, request, url_for, session
from git.repo import Repo
from flask_sqlalchemy import SQLAlchemy
from model.power_plant import PowerPlant
from model.concrete import Concreto
from model.estrutura import Estrutura
from model.module import Module
from model.tables import Mesa
app = Flask(__name__)
app.secret_key = 'agsolar2023engenheiros'

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

# region database

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

# endregion

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = Repo('./AGSolarEngineers')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

@app.route('/', methods=['GET', 'POST'])
def index():
    session['url'] = url_for('index')
    if request.method == 'GET':
        return render_template('index.html', comments=Comment.query.all())
        # return render_template('index.html')
    comment = Comment(content=request.form['txt_comments']) # type: ignore
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle-theme')
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    print(session['theme'])
    if 'url' in session:
        return redirect(session['url'])
    return redirect(url_for('index'))

@app.route('/estrutura-kwp', methods=('GET', 'POST'))
def estrutura_kwp():
    session['url'] = url_for('estrutura_kwp')
    module = Module(1134, 2261, 540, 41.3, 13.08, 49.2, 13.9)
    power_plant = PowerPlant('', '7.0000', 'Av. dos Trabalhadores, 665, São João da Boa Vista - SP',
                             103.68, module, False)
    if request.method == "POST":
        power_plant.customers_name = request.form['txt_customers_name']
        power_plant.module.length = int(request.form['txt_module_length'])
        power_plant.power = float(request.form['txt_power_plant_total'])
        power_plant.module.power = int(request.form['txt_module_power'])
        power_plant.concrete.height_buried = float(request.form['txt_height_buried'])
        power_plant.concrete.ray_buried = float(request.form['txt_ray_buried'])
        power_plant.concrete.height_exposed = float(request.form['txt_height_exposed'])
        power_plant.concrete.ray_exposed = float(request.form['txt_ray_exposed'])
        inverter_table = request.form.getlist('chk_inverter')
        if inverter_table:
            power_plant.inverter_table = True
        power_plant.calculate_optmize()
        power_plant.concrete.calculate_volume()

    return render_template('estrutura_kwp.html', power_plant=power_plant)


@app.route('/estrutura-otimizar', methods=('GET', 'POST'))
def estrutura_otimizar():
    session['url'] = url_for('estrutura_otimizar')
    module = Module(1134, 2261, 540, 41.3, 13.08, 49.2, 13.9)
    power_plant = PowerPlant('', '7.0000', 'Av. dos Trabalhadores, 665, São João da Boa Vista - SP',
                             103.68, module, False)
    if request.method == "POST":
        power_plant.module.length = int(request.form['txt_module_length'])
        power_plant.module.power = int(request.form['txt_module_power'])
        power_plant.module_amount = int(request.form['txt_module_amount'])
        power_plant.concrete.height_buried = float(request.form['txt_height_buried'])
        power_plant.concrete.ray_buried = float(request.form['txt_ray_buried'])
        power_plant.concrete.height_exposed = float(request.form['txt_height_exposed'])
        power_plant.concrete.ray_exposed = float(request.form['txt_ray_exposed'])
        inverter_table = request.form.getlist('chk_inverter')
        if inverter_table:
            power_plant.inverter_table = True
        power_plant.calculate_module_amount_defined()
        power_plant.concrete.base_amount = power_plant.structures[-1].bom['5603112']['quantidade']*2
        power_plant.concrete.calculate_volume()
    return render_template('estrutura_otimizar.html', power_plant=power_plant)


@app.route('/estrutura-un', methods=('GET', 'POST'))
def estrutura_un():
    session['url'] = url_for('estrutura_un')
    module = Module(1134, 2261, 540, 41.3, 13.08, 49.2, 13.9)
    structure = Estrutura(module, 300, 1, False)
    if request.method == "POST":
        structure.module.length = int(request.form['txt_module_length'])
        structure.module_amount = int(request.form['txt_module_amount'])
        structure.table_amount = int(request.form['txt_table_amount'])
        inverter_table = request.form.getlist('chk_inverter')
        if inverter_table:
            structure.inverter_table = True
        structure.calculate()
    return render_template('estrutura_un.html',  structure=structure, active='Estrutura')

@app.route('/comercial/estrutura', methods=('GET', 'POST'))
def comercial_estrutura():
    session['url'] = url_for('comercial_estrutura')
    module = Module(1134, 2261, 540, 41.3, 13.08, 49.2, 13.9)
    power_plant = PowerPlant('', '7.0000', 'Av. dos Trabalhadores, 665, São João da Boa Vista - SP',
                             103.68, module, False)
    if request.method == "POST":
        power_plant.module.length = int(request.form['txt_module_length'])
        power_plant.module.power = int(request.form['txt_module_power'])
        power_plant.module_amount = int(request.form['txt_module_amount'])
        power_plant.concrete.height_buried = float(request.form['txt_height_buried'])
        power_plant.concrete.ray_buried = float(request.form['txt_ray_buried'])
        power_plant.concrete.height_exposed = float(request.form['txt_height_exposed'])
        power_plant.concrete.ray_exposed = float(request.form['txt_ray_exposed'])
        inverter_table = request.form.getlist('chk_inverter')
        if inverter_table:
            power_plant.inverter_table = True
        power_plant.calculate_module_amount_defined()
        power_plant.concrete.base_amount = power_plant.structures[-1].bom['5603112']['quantidade']*2
        power_plant.concrete.calculate_volume()
    return render_template('estrutura_otimizar.html', power_plant=power_plant)


@app.route('/mesas/', methods=('GET', 'POST'))
def tables():
    session['url'] = url_for('tables')
    module = Module(1134, 2261, 540, 41.3, 13.08, 49.2, 13.9)
    mesa = Mesa(module, 300)
    if request.method == "POST":
        module.length = int(request.form['txt_module_length'])
        module.power = int(request.form['txt_module_power'])
        mesa.module_amount = int(request.form['txt_module_amount'])
        mesa.module = module
        mesa.calculate_rows()
    return render_template('mesas.html', mesa=mesa)

@app.route('/concreto', methods=('GET', 'POST'))
def concreto():
    session['url'] = url_for('concreto')
    concreto = Concreto(0, 1.6, 0.15, 0.4, 0.2, 'H21')
    if request.method == "POST":
        concreto.base_amount = int(request.form['txt_base_amount'])
        concreto.height_buried = float(request.form['txt_height_buried'])
        concreto.ray_buried = float(request.form['txt_ray_buried'])
        concreto.height_exposed = float(request.form['txt_height_exposed'])
        concreto.ray_exposed = float(request.form['txt_ray_exposed'])
        concreto.calculate_volume()

    return render_template("concreto.html", active='Estrutura', concreto=concreto)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
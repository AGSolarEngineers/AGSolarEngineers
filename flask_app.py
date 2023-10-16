import math
from flask import Flask, redirect, render_template, request, url_for, session
from git.repo import Repo
from flask_sqlalchemy import SQLAlchemy
from controller.power_plant import PowerPlant
from model.estrutura import Estrutura
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

@app.route('/')
def index():
    session['url'] = url_for('index')
    return render_template('index.html', comments=Comment.query.all())

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
    default_module_length = 1134
    default_power_plant_total = 103.68
    default_module_power = 540
    default_module_amount = 0
    default_table_amount = 0
    power_plant_real = 0
    default_customers_name = ''
    BOM = []
    BOM_total = None
    structure = None
    
    default_base_amount = 0.0
    default_height_buried = 1.6
    default_ray_buried = 0.15
    default_height_exposed = 0.4
    default_ray_exposed = 0.2

    default_inverter_table = False

    if request.method == 'POST':
        customers_name = str(request.form['txt_customers_name'])
        default_customers_name = customers_name
        module_length = int(request.form['txt_module_length'])
        default_module_length = module_length
        power_plant_total = float(request.form['txt_power_plant_total'])
        default_power_plant_total = power_plant_total
        module_power = int(request.form['txt_module_power'])
        height_buried = request.form['txt_height_buried']
        default_height_buried = float(height_buried)
        ray_buried = request.form['txt_ray_buried']
        default_ray_buried = float(ray_buried)
        height_exposed = request.form['txt_height_exposed']
        default_height_exposed = float(height_exposed)
        ray_exposed = request.form['txt_ray_exposed']
        default_ray_exposed = float(ray_exposed)

        structure = PowerPlant(power_plant_total, module_power, module_length)

        try:
            request.form['chk_inverter']
            default_inverter_table = True
        except:
            default_inverter_table = False
        for modules in structure.mesas.mesas:
            if BOM_total is None:
                obj = Estrutura(structure.module_length, modules[1], modules[0], default_inverter_table)
                BOM_total = obj.get_bill()
            else:
                obj = Estrutura(structure.module_length, modules[1], modules[0], False)
                for chave in obj.get_bill()['BOM']:
                    if chave in BOM_total['BOM']:
                        BOM_total['BOM'][chave]['quantidade'] = obj.get_bill()['BOM'][chave]['quantidade']+BOM_total['BOM'][chave]['quantidade']
            BOM.append(obj)
        
        if BOM_total is not None:
            default_base_amount = BOM_total['BOM']['1']['quantidade']*2
        default_module_amount = structure.panels_amount
        default_table_amount = structure.mesas.mesas
        power_plant_real = structure.total_power

    default_volume_buried = math.pi*(default_ray_buried**2.0)*default_height_buried
    default_volume_exposed = math.pi*(default_ray_exposed**2.0)*default_height_exposed
    default_volume_per_base = default_volume_buried+default_volume_exposed
    default_volume_total = math.ceil(default_base_amount*default_volume_per_base*1.1)
    default_feature = "H21"

    return render_template('estrutura_kwp.html', default_customers_name=default_customers_name, default_inverter_table = default_inverter_table,
                           default_module_length=default_module_length, default_power_plant_total=default_power_plant_total, default_module_power=default_module_power, 
                           default_module_amount=default_module_amount, default_table_amount=default_table_amount, power_plant_real=power_plant_real, structure=structure, BOM=BOM, BOM_total=BOM_total,
                           default_base_amount=default_base_amount, default_height_buried=default_height_buried, default_ray_buried=default_ray_buried, default_volume_buried=default_volume_buried, 
                        default_height_exposed=default_height_exposed, default_ray_exposed=default_ray_exposed, default_volume_exposed=default_volume_exposed, 
                        default_volume_per_base=default_volume_per_base, default_volume_total=default_volume_total, default_feature=default_feature)

@app.route('/estrutura-un', methods=('GET', 'POST'))
def estrutura():
    session['url'] = url_for('estrutura')
    structure = Estrutura(0, 0, 0, False)
    default_module_length=1134
    default_module_amount = 300
    default_table_amount=1
    default_inverter_table = False
    if request.method == "POST":
        module_length = request.form['txt_module_length']
        module_amount = request.form['txt_module_amount']
        table_amount = request.form['txt_table_amount']
        default_module_length = module_length
        default_module_amount = module_amount
        default_table_amount = table_amount
        try:
            request.form['chk_inverter']
            default_inverter_table = True
        except:
            default_inverter_table = False
        structure = Estrutura(int(module_length), int(module_amount), int(table_amount), default_inverter_table)
    return render_template('estrutura_un.html', default_module_length=default_module_length, default_module_amount=default_module_amount, default_table_amount=default_table_amount, default_inverter_table=default_inverter_table, structure=structure, active='Estrutura')

@app.route('/comercial/estrutura', methods=('GET', 'POST'))
def comercial_estrutura():
    session['url'] = url_for('comercial_estrutura')
    structure = Estrutura(0, 0, 0, False)
    default_module_length = 1055
    default_module_amount = 300
    default_module_power = 540
    default_power_plant_total = 103.68
    power_plant_real = default_power_plant_total
    default_table_amount = 1
    default_inverter_table = False
    if request.method == "POST":
        module_length = request.form['txt_module_length']
        module_power = request.form['txt_module_power']
        power_plant_total = request.form['txt_power_plant_total']
        default_module_length = module_length
        default_module_power = module_power
        default_power_plant_total = power_plant_total
        try:
            request.form['chk_inverter']
            default_inverter_table = True
        except:
            default_inverter_table = False
        power_plant = PowerPlant(float(power_plant_total), int(module_power), int(default_module_length))
        default_module_amount = power_plant.panels_amount
        default_table_amount = 1
        power_plant_real = power_plant.total_power
        structure = Estrutura(int(module_length), int(default_module_amount), int(default_table_amount), default_inverter_table)
    return render_template('comercial_estrutura.html', default_module_length=default_module_length, default_module_amount=default_module_amount, default_table_amount=default_table_amount, default_power_plant_total=default_power_plant_total,
                           structure=structure, default_inverter_table=default_inverter_table, default_module_power=default_module_power, power_plant_real=power_plant_real,
                           active='Estrutura')

@app.route('/mesas/', methods=('GET', 'POST'))
def tables():
    session['url'] = url_for('tables')
    obj = Mesa(0, 0, 0)
    default_module_length = 1134
    default_module_amount = 300
    default_module_power = 540
    if request.method == "POST":
        module_length = request.form['txt_module_length']
        default_module_length = module_length
        module_amount = request.form['txt_module_amount']
        default_module_amount = module_amount
        module_power = request.form['txt_module_power']
        default_module_power = module_power
        obj = Mesa(int(module_length), int(module_amount), int(module_power))
    return render_template('mesas.html', default_module_length=default_module_length, default_module_amount=default_module_amount, default_module_power=default_module_power, tables=obj, active='Estrutura')

@app.route('/concreto', methods=('GET', 'POST'))
def concreto():
    session['url'] = url_for('concreto')
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
                            default_volume_per_base=default_volume_per_base, default_volume_total=default_volume_total, default_feature=default_feature)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
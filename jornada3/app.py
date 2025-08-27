from flask import Flask, render_template, session
from datetime import timedelta
from utils.conexion_db import init, create_admin_user
from routes.login import login_bp
from routes.registro import registro_bp
from routes.eventos import eventos_bp
from routes.alquiler import alquiler_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

with app.app_context():
    init()
    create_admin_user()

app.register_blueprint(login_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(alquiler_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def mostrar_login():
    return render_template('login.html')

@app.route('/registro')
def mostrar_registro():
    return render_template('registro.html')

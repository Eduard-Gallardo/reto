from flask import Blueprint, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from utils.conexion_db import get_db_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM usuario WHERE nombre = ? OR email = ?", (nombre, nombre)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = user['nombre']
            session['rol'] = user['rol'] 
            flash('¡Inicio de sesión exitoso!', 'success')

            if user['rol'] == 'Administrador':
                return redirect(url_for('dashboard.mostrar_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('mostrar_login'))

    return "Método no permitido", 405
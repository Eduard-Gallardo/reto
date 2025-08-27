from flask import Blueprint, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash
from utils.conexion_db import get_db_connection

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        estrato = request.form['estrato']
        rol = request.form['rol']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO usuario (nombre, email, estrato, rol, password) VALUES (?, ?, ?, ?, ?)",
                (nombre, email, estrato, rol, hashed_password)
            )
            conn.commit()
            conn.close()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login.login'))
        except sqlite3.IntegrityError:
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('registro.registro'))
    return "Método no permitido", 405
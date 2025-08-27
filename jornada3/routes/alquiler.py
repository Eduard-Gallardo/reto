from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.conexion_db import get_db_connection

alquiler_bp = Blueprint('alquiler', __name__)

@alquiler_bp.route('/alquiler')
def mostrar_alquiler():
    conn = get_db_connection()
    bicicletas = conn.execute("SELECT * FROM bicicleta WHERE estado = 'Disponible'").fetchall()
    conn.close()
    return render_template('alquiler.html', bicicletas=bicicletas)

@alquiler_bp.route('/alquilar', methods=['POST'])
def alquilar_bicicleta():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Debes iniciar sesión para alquilar una bicicleta.', 'warning')
        return redirect(url_for('mostrar_login'))

    bicicleta_id = request.form['bicicleta_id']
    usuario_nombre = session['username']
    
    conn = get_db_connection()
    try:
        usuario = conn.execute('SELECT id FROM usuario WHERE nombre = ?', (usuario_nombre,)).fetchone()
        usuario_id = usuario['id']
        conn.execute('INSERT INTO alquiler (usuario_id, bicicleta_id) VALUES (?, ?)',
                     (usuario_id, bicicleta_id))
        conn.execute("UPDATE bicicleta SET estado = 'Alquilada' WHERE id = ?", (bicicleta_id,))
        conn.commit()
        flash('Bicicleta alquilada exitosamente!', 'success')
    except Exception as e:
        flash(f'Ocurrió un error: {e}', 'error')
    finally:
        conn.close()

    return render_template('alquiler.html', bicicletas=conn.execute("SELECT * FROM bicicleta WHERE estado = 'Disponible'").fetchall())
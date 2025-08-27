from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.conexion_db import get_db_connection
import sqlite3

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/eventos')
def mostrar_eventos():
    conn = get_db_connection()
    eventos = conn.execute('SELECT * FROM evento WHERE fecha > CURRENT_TIMESTAMP').fetchall()
    conn.close()
    return render_template('eventos.html', eventos=eventos)

@eventos_bp.route('/inscribirse', methods=['POST'])
def inscribirse_evento():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Debes iniciar sesión para inscribirte.', 'warning')
        return redirect(url_for('mostrar_login'))

    evento_id = request.form['evento_id']
    usuario_nombre = session['username']
    
    conn = get_db_connection()
    try:
        usuario = conn.execute('SELECT id FROM usuario WHERE nombre = ?', (usuario_nombre,)).fetchone()
        usuario_id = usuario['id']
        conn.execute('INSERT INTO inscripciones_evento (usuario_id, evento_id) VALUES (?, ?)',
                     (usuario_id, evento_id))
        conn.commit()
        flash('Te has inscrito en el evento exitosamente!', 'success')
    except sqlite3.IntegrityError:
        flash('Ya estás inscrito en este evento.', 'warning')
    except Exception as e:
        flash(f'Ocurrió un error: {e}', 'error')
    finally:
        conn.close()

    return redirect(url_for('eventos.mostrar_eventos'))
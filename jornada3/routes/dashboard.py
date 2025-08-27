from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.conexion_db import get_db_connection
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def mostrar_dashboard():
    conn = get_db_connection()
    bicicletas = conn.execute("SELECT * FROM bicicleta").fetchall()
    bicicletas_alquiladas = conn.execute('''
        SELECT 
            b.id,
            b.marca,
            b.color,
            u.nombre as usuario,
            a.fecha_prestamo,
            b.estado as estado_bicicleta,
            a.fecha_devolucion
        FROM alquiler a
        JOIN bicicleta b ON a.bicicleta_id = b.id
        JOIN usuario u ON a.usuario_id = u.id
        ORDER BY a.fecha_prestamo DESC
    ''').fetchall()
    
    conn.close()
    
    prestamos_procesados = []
    for prestamo in bicicletas_alquiladas:
        fecha_prestamo = datetime.strptime(prestamo['fecha_prestamo'], '%Y-%m-%d %H:%M:%S')
        diferencia = datetime.now() - fecha_prestamo
        horas = int(diferencia.total_seconds() / 3600)
        
        estado_simulado = "En curso"
        if prestamo['fecha_devolucion']:
            estado_simulado = "Devuelto"
        elif horas > 24:
            estado_simulado = "Retrasado"

        prestamos_procesados.append({
            'marca': prestamo['marca'],
            'color': prestamo['color'],
            'usuario': prestamo['usuario'],
            'tiempo': f"{horas} h",
            'estado': estado_simulado
        })

    return render_template('dashboard.html', bicicletas=bicicletas, bicicletas_prestadas=prestamos_procesados)


@dashboard_bp.route('/crear_bicicleta', methods=['POST'])
def crear_bicicleta():
    if request.method == 'POST':
        marca = request.form['marca']
        color = request.form['color']
        estado = request.form['estado']
        tarifa_inicial = request.form['tarifa_inicial']
        tarifa_adicional = request.form['tarifa_adicional']
        
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO bicicleta (marca, color, estado, tarifa_inicial, tarifa_adicional) VALUES (?, ?, ?, ?, ?)",
                (marca, color, estado, tarifa_inicial, tarifa_adicional)
            )
            conn.commit()
            flash('Bicicleta creada exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error al crear la bicicleta: {e}', 'error')
        finally:
            conn.close()

    return redirect(url_for('dashboard.mostrar_dashboard'))


@dashboard_bp.route('/crear_evento', methods=['POST'])
def crear_evento():
    if request.method == 'POST':
        nombre = request.form['nombre_evento']
        descripcion = request.form['descripcion']
        fecha_str = request.form['fecha_evento']
        lugar = request.form['lugar']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO evento (nombre, descripcion, fecha, lugar) VALUES (?, ?, ?, ?)",
                (nombre, descripcion, fecha, lugar)
            )
            conn.commit()
            flash('Evento creado exitosamente.', 'success')
        except Exception as e:
            flash(f'Ocurrió un error al crear el evento: {e}', 'error')
        finally:
            conn.close()

    return redirect(url_for('dashboard.mostrar_dashboard'))



from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.conexion_db import get_db_connection
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def mostrar_dashboard():
    # ... (código para verificar el rol del usuario) ...
    
    conn = get_db_connection()
    
    # Obtener TODAS las bicicletas, sin importar el estado
    bicicletas = conn.execute("SELECT * FROM bicicleta").fetchall()
    
    # Obtener todos los préstamos para la sección de bicicletas prestadas
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
    
    # Procesar los datos para el frontend (como el tiempo transcurrido)
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



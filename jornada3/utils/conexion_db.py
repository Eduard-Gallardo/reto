import sqlite3
from time import time
from werkzeug.security import generate_password_hash

def get_db_connection():
    conn = sqlite3.connect('model/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL,
            nombre TEXT NOT NULL,
            email NOT NULL UNIQUE,
            password TEXT NOT NULL,
            estrato INTEGER NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bicicleta(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            color TEXT NOT NULL,
            estado TEXT NOT NULL,
            tarifa_inicial REAL NOT NULL,
            tarifa_adicional REAL NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alquiler(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            bicicleta_id INTEGER NOT NULL,
            fecha_prestamo timestamp DEFAULT CURRENT_TIMESTAMP,
            fecha_devolucion timestamp NULL,
            costo_total REAL,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id),
            FOREIGN KEY (bicicleta_id) REFERENCES bicicleta(id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha timestamp DEFAULT CURRENT_TIMESTAMP,
            lugar TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones_evento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            evento_id INTEGER NOT NULL,
            fecha_inscripcion timestamp DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id),
            FOREIGN KEY (evento_id) REFERENCES evento(id),
            UNIQUE (usuario_id, evento_id)
        );
    ''')
    conn.commit()
    conn.close()

def create_admin_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash('12345')

    cursor.execute("SELECT id FROM usuario WHERE email = ?", ('admin@gmail.com',))
    admin_exists = cursor.fetchone()
    
    if not admin_exists:
        conn.execute(
            "INSERT INTO usuario (nombre, email, password, rol, estrato) VALUES (?, ?, ?, ?, ?)",
            ('admin', 'admin@gmail.com', hashed_password, 'Administrador', 1)
        )
        conn.commit()
        print("Usuario administrador creado.")
    else:
        print("El usuario administrador ya existe.")
        
    conn.close()
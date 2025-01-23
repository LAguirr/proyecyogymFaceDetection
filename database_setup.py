import sqlite3

def create_database():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("powerhousegym.db")
    cursor = conn.cursor()

    # Crear tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_ingreso TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            id_membresia INTEGER,
            foto BLOB,
            FOREIGN KEY(id_membresia) REFERENCES membresia(id_membresia)
        )
    ''')

    # Crear tabla de membresía si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS membresia (
            id_membresia INTEGER PRIMARY KEY AUTOINCREMENT,
            membresia TEXT NOT NULL
        )
    ''')

    # Create the new logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            hora_acceso TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            vencido BOOL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
    ''')

    # Poblar la tabla de membresía con datos de ejemplo
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (1, 'Dia')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (2, 'Semana')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (3, 'Quincena')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (4, 'Mes Estudiante')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (5, 'Mes')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (6, 'Trimestre')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (7, 'Semestre')")
    cursor.execute("INSERT OR IGNORE INTO membresia (id_membresia, membresia) VALUES (8, 'Anualidad')")

    # Insert sample data into 'usuarios'
    cursor.executemany("""
    INSERT INTO usuarios (nombre, id_membresia, fecha_ingreso, fecha_vencimiento) 
    VALUES (?, ?, ?, ?);
    """, [
        ("Alice", 1, "2024-01-01", "2024-12-31"),
        ("Bob", 2, "2024-02-01", "2025-01-31"),
        ("Charlie", 3, "2024-03-01", "2025-02-28"),
    ])


    # Confirmar cambios y cerrar la conexión
    conn.commit()
    conn.close()

# Llamar a esta función para crear la base de datos al ejecutar el archivo
if __name__ == "__main__":
    create_database()
    print("Base de datos y tablas creadas exitosamente.")

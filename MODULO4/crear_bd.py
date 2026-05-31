import sqlite3

conexion = sqlite3.connect("estudiantes.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    nombre TEXT PRIMARY KEY,
    id_estudiante INTEGER,
    edad INTEGER,
    carrera TEXT,
    semestre INTEGER
)
""")

datos = [
    ("Jorge", 21170363, 22, "Ing en sistemas", 10),
    ("Diego", 2217, 21, "Ing en sistemas", 8),
    ("Karim", 23171159, 24, "Ing en sistemas", 6),
    ("Miguel", 19170561, 24, "Ing en sistemas", 14),
    ("Valeria", 19170631, 24, "Ing en sistemas", 14),
    ("German", 18170521, 25, "Lic en derecho", 18)
]

cursor.executemany("""
INSERT OR REPLACE INTO estudiantes
VALUES (?, ?, ?, ?, ?)
""", datos)

conexion.commit()
conexion.close()

print("Base de datos creada correctamente.")
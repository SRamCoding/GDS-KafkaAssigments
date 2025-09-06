import os
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Leer queries del archivo
with open("querys.sql", "r") as f:
    sql_script = f.read()

# Conexión a MySQL (sin seleccionar base de datos, porque la creamos en el script)
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", "rootpass")
)

cursor = conn.cursor()

# Ejecutar múltiples sentencias
for result in cursor.execute(sql_script, multi=True):
    pass  # simplemente avanza ejecutando cada sentencia

cursor.close()
conn.close()

print("✅ Base de datos y tabla inicializadas con querys.sql")
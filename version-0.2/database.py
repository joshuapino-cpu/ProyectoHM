import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    # <-- Pon tu contraseña si tienes
        database="petro"
    )

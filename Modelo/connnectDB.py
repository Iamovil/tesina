import sqlite3
import mysql.connector
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

config = {
    'host': 'sql9.freemysqlhosting.net',
    'user': 'sql9629978',
    'password': '23r5jmB7LK',
    'database': 'sql9629978'
}

conn = mysql.connector.connect(**config)

def obtenerConexionBD():
    c = conn.cursor()
    return c

def confirmarAccionBD():
    conn.commit()

def cerrarConector():
    conn.close()




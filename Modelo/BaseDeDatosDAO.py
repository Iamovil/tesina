import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import sqlite3 
import shutil
import pymysql
import mysql
nombre = "BDNEW.db"

def respaldoBD():
    # ///////////////////////////////////////////
    # RESPALDO DE LA BASE DE DATOS DE FORMA LOCAL
    # ///////////////////////////////////////////
    # # Ruta de la base de datos original
    # ruta_base_datos = 'BDNEW.db'

    # # # Ruta donde se va a copiar el respaldo
    # ruta_respaldo = 'respaldoDB' + '.db'

    # #Copia la base de datos a la nueva ubicación
    # shutil.copyfile(ruta_base_datos, ruta_respaldo)
    # ///////////////////////////////////////////
    
    c = connexBD.obtenerConexionBD()
    # Obtener la estructura de la base de datos
    c.execute("SHOW CREATE DATABASE sql9629978")
    create_database = c.fetchone()[1]

    # Obtener la estructura de las tablas
    c.execute("SHOW TABLES")
    tables = c.fetchall()

    # Generar el archivo de respaldo
    with open('respaldo.sql', 'w') as backup_file:
        backup_file.write(create_database + "\n\n")

        for table in tables:
            table_name = table[0]
            c.execute(f"SHOW CREATE TABLE {table_name}")
            create_table = c.fetchone()[1]
            backup_file.write(create_table + ";\n\n")

            c.execute(f"SELECT * FROM {table_name}")
            rows = c.fetchall()
            for row in rows:
                values = ', '.join([repr(value) for value in row])
                backup_file.write(f"INSERT INTO {table_name} VALUES ({values});\n")

    # Cerrar el cursor y la conexión
    c.close()
    connexBD.cerrarConector()
    return True

def restauracionBD():
    # ///////////////////////////////////////////
    # RESTAURACIÓN DE LA BASE DE DATOS DE FORMA LOCAL
    # ///////////////////////////////////////////
    # c = connexBD.getConnection()
    # c.close()
    # c.connection.close()
    # # Ruta de la base de datos original
    # ruta_base_datos = 'BDNEW.db'

    # # Ruta donde se encuentra el archivo de respaldo
    # ruta_respaldo = 'respaldoDB' + '.db'

    # # Copia el archivo de respaldo a la ubicación de la base de datos original
    # os.remove('BDNEW.db')
    # shutil.copyfile(ruta_respaldo, ruta_base_datos)

    # shutil.move(ruta_respaldo,ruta_base_datos)
    # ///////////////////////////////////////////
    c = connexBD.obtenerConexionBD()
    # Leer el contenido del archivo de respaldo
    with open('respaldo.sql', 'r') as backup_file:
        sql_statements = backup_file.read()

    # Ejecutar las instrucciones SQL para restaurar la base de datos
    for statement in sql_statements.split(';'):
        try:
            c.execute(statement)
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la instrucción SQL: {e}")

    # Confirmar los cambios
    connexBD.confirmarAccionBD()

    # Cerrar el cursor y la conexión
    c.close()
    connexBD.cerrarConector()
    return True
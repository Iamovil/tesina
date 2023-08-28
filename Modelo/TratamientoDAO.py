import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Cache.CacheDeTratamiento as cacheDeTratamiento
import Cache.CacheDeUsuario as cacheUsuario
import sqlite3 
import datetime

def obtenerSiguienteIdTratamiento():
    c = connexBD.obtenerConexionBD()
    c.execute('select max(idTratamiento) + 1 from Tratamiento')
    p = c
    if c.arraysize>0:
        for i in c:
            print("Siguiente ID tratamiento:",i[0])
            return i
    else:
        return 0

# Entradas:
# idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen, idUsuario
# Salidas:
# El sistema confirma que se ha realizado la inserción correctamente con True
# Función para insertar un nuevo tratamiento
def insertarNuevoTratamiento(idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen, idUsuario):
    c = connexBD.obtenerConexionBD() #Conexión a la base de datos
    c.execute('insert into Tratamiento (idTratamiento, enfermedad,fungicida,marca,descripcion,precaucion,imagen,fecha,idUsuario) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
              [idTratamiento, str(enfermedad), str(fungicida),str(marca),str(descripcion),str(precaucion), imagen,datetime.datetime.now(), int(idUsuario)])
    connexBD.confirmarAccionBD() #Confirmar la inserción de la base de datos
    print("insertar tratamiento")
    c.close()
    return True

def obtenerTotalTratamientos():
    c = connexBD.obtenerConexionBD()
    c.execute("select count(*) from Tratamiento")
    p = c
    if c.arraysize > 0:
        for i in c:
            print("Total de tratamientos registrados:", i[0])
            return i
    else:
        return "0";

def obtenerIdsTratamientos():
    c = connexBD.obtenerConexionBD()
    c.execute('select idTratamiento from Tratamiento')
    p = c
    for i in c:
        cacheDeTratamiento.idsTratamientos.append(i[0])
    c.close()

def obtenerTotalTratamientosReconocimiento(enfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute("select count(*) from Tratamiento where enfermedad = %s",(enfermedad,))
    p = c
    if c.arraysize > 0:
        for i in c:
            print("Total de tratamientos registrados:", i[0])
            return i
    else:
        return "0";

def obtenerIdsTratamientosReconocimiento(enfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select idTratamiento from Tratamiento where enfermedad = %s',(enfermedad,))
    p = c
    for i in c:
        cacheDeTratamiento.idsTratamientos.append(i[0])
    c.close()

# Etradas:
# idTratamiento
# Salidas:
# Información del tratamiento
#Función de consulta del tratamiento
def obtenerTratamiento(idTratamiento):
    c = connexBD.obtenerConexionBD() #Conexión a la base de datos
    c.execute('select idTratamiento,enfermedad,fungicida,imagen,idUsuario from Tratamiento where idTratamiento = %s',(idTratamiento,))
    p = c
    for i in c:
        print("idTratamiento", i[0])
        print("Enfermedad", i[1])
        print("Fungicida", i[2])
        print("imagen", i[3])
        print("idUsuario", i[4])
        return i #Se envia la información del registro del tratamiento
    c.close

def obtenerTratamientoCompleto(idTratamiento):
    c = connexBD.obtenerConexionBD()
    c.execute('select idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen, fecha,idUsuario from Tratamiento where idTratamiento = %s',(idTratamiento,))
    p = c
    for i in c:
        print("idTratamiento", i[0])
        print("Enfermedad", i[1])
        print("Fungicida", i[2])
        print("Marca", i[3])
        print("Descripción", i[4])
        print("Precaución:",i[5])
        print("imagen",i[6])
        print("fecha",i[7])
        print("idUsuario",i[8])
        return i
    c.close

# Entradas:
# idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen,idUsuario
# Salidas:
# Confirmación de modificación exitosa con True
#Función de modificación del tratamiento
def modificarTratamientoSeleccionada(idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen,idUsuario):
    c = connexBD.obtenerConexionBD() #Conexión a la base de datos
    c.execute('update Tratamiento set enfermedad = %s, fungicida = %s, marca = %s, descripcion = %s, precaucion = %s, imagen = %s, fecha = %s, idUsuario = %s where idTratamiento = %s',(enfermedad,fungicida,marca,descripcion,precaucion,imagen,datetime.datetime.now(),idUsuario,idTratamiento)) #Envio de información
    connexBD.confirmarAccionBD() #Confirmación
    print("Modificación de tratamiento realizada en Data Access Object")
    c.close()
    return True #La actualización se hace con exito

# Entradas:
# idTratamiento
#Salidas:
# Confirmación de la eliminación
#Función de eliminación de información
def eliminarTratamientoSeleccionado(idTratamiento):
    c = connexBD.obtenerConexionBD() #Conexión a la base de datos
    c.execute('delete from tratamiento where idTratamiento = ?',(idTratamiento,)) #Uso de la función delete de sqllite para eliminar tratamiento
    connexBD.confirmarAccionBD() #Confirmar eliminación
    c.close()
    return True #Envio de mensaje de exito con True
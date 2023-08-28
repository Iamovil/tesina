import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Cache.CacheDeUsuario as cacheUsuario
import Cache.CacheDePregunta as cachePregunta
import sqlite3 
from PIL import Image

def obtenerPregunta(idPregunta):
    c = connexBD.obtenerConexionBD()
    c.execute('select idPregunta,descripcion,pregunta,imagen,idUsuario from Pregunta where idPregunta = %s',(idPregunta,))
    p = c
    for i in c:
        print("idPregunta", i[0])
        print("descripción", i[1])
        print("pregunta", i[2])
        print("imagen", i[3])
        print("idUsuario", i[4])
        return i
    c.close

def obtenerPreguntaUsuarioPersonal(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select idPregunta,descripcion,pregunta,imagen,idUsuario from Pregunta where idPregunta = %s',(idUsuario,))
    p = c
    for i in c:
        return i
    c.close

def obtenerTotalPreguntas():
    c = connexBD.obtenerConexionBD()
    c.execute("select count(*) from Pregunta")
    p = c
    if c.arraysize > 0:
        for i in c:
            print("Total de preguntas registradas:", i[0])
            return i
    else:
        return "0";

def obtenerTotalPreguntasPersonal(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute("select count(*) from Pregunta where idUsuario = %s",(idUsuario,))
    p = c
    if c.arraysize > 0: #Verifica el arreglo no este vacio, si no está vacio realiza las funciones:
        for i in c:
            return i #Devuelve la información de las preguntas
    else:
        return "0"; #No devuelve nada

def obtenerSiguienteIdPregunta():
    c = connexBD.obtenerConexionBD()
    c.execute('select max(idPregunta) + 1 from Pregunta')
    p = c
    if c.arraysize>0:
        for i in c:
            print("Siguiente ID pregunta:",i[0])
            return i
    else:
        return 0

def insertarNuevaPregunta(idPregunta, descripcion, pregunta, imagen, idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('insert into Pregunta (idPregunta, descripcion, pregunta, imagen, idUsuario) values (%s, %s, %s, %s, %s)',
              (idPregunta, descripcion, pregunta, imagen, idUsuario))
    connexBD.confirmarAccionBD()
    print("insertar pregunta")
    c.close()
    return True

def modificarPreguntaSeleccionada(idPregunta, descripcion, pregunta, imagen):
    c = connexBD.obtenerConexionBD()
    c.execute('update Pregunta set descripcion = %s, pregunta = %s, imagen = %s where idPregunta = %s',(descripcion,pregunta,imagen,idPregunta))
    connexBD.confirmarAccionBD()
    print("Modificación de pregunta realizada en Data Access Object")
    c.close()
    return True

def obtenerIdsPreguntas():
    c = connexBD.obtenerConexionBD()
    c.execute('select idPregunta from Pregunta')
    p = c
    for i in c:
        cachePregunta.idsPreguntas.append(i[0])
    c.close()

def obtenerIdsPreguntasPersonales(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select idPregunta from Pregunta where idUsuario = %s',(idUsuario,))
    p = c
    for i in c:
        cachePregunta.idsPreguntas.append(i[0])
    c.close()

def eliminarPreguntaSeleccionada(idPregunta):
    c = connexBD.obtenerConexionBD()
    c.execute('delete from Pregunta where idPregunta = %s',(idPregunta,))
    connexBD.confirmarAccionBD()
    c.close()
    return True

def obtenerTotalIDPreguntasContestadas(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select COUNT(DISTINCT Pregunta.idPregunta) from Pregunta inner join Respuesta on Respuesta.idPregunta = Pregunta.idPregunta inner join Usuario on Usuario.idUsuario = Respuesta.idUsuario where Respuesta.idUsuario = %s',(idUsuario,))
    p = c
    if c.arraysize > 0:
        for i in c:
            return i
    else:
        return "0";

def obtenerIdsPreguntasContestadasPersonales(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select DISTINCT Pregunta.idPregunta from Pregunta inner join Respuesta on Respuesta.idPregunta = Pregunta.idPregunta inner join Usuario on Usuario.idUsuario = Respuesta.idUsuario where Respuesta.idUsuario = %s',(idUsuario,))
    p = c
    for i in c:
        cachePregunta.idsPreguntas.append(i[0])
    c.close()


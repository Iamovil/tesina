import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Cache.CacheDeRespuesta as cacheDeRespuesta
import sqlite3 


def obtenerRespuesta(idRespuesta,idPregunta):
    c = connexBD.obtenerConexionBD()
    c.execute('select idRespuesta,descripcion,idUsuario,idPregunta from Respuesta where idPregunta = %s and idRespuesta = %s',(idPregunta,idRespuesta))
    p = c
    for i in c:
        print("idRespuesta", i[0])
        print("descripción", i[1])
        print("idUsuario", i[2])
        print("idPregunta", i[3])
        return i
    c.close

def obtenerIdsRespuestas(idPregunta):
    c = connexBD.obtenerConexionBD()
    c.execute('select idRespuesta from Respuesta where idPregunta = %s',(idPregunta,))
    p = c
    for i in c:
        cacheDeRespuesta.idsRespuestas.append(i[0])
    
def obtenerIdsRespuestasPersonales(idPregunta,idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select idRespuesta from Respuesta where idPregunta = %s and idUsuario = %s',(idPregunta,idUsuario))
    p = c
    for i in c:
        cacheDeRespuesta.idsRespuestas.append(i[0])

def obtenerTotalRespuestasIdPregunta(idPregunta):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Respuesta where idPregunta = %s',(idPregunta,))
    for i in c:
        cacheDeRespuesta.totalRespuestasId = i[0]

def obtenerTotalRespuestasIdPreguntaPersonales(idPregunta,idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Respuesta where idPregunta = %s and idUsuario = %s',(idPregunta,idUsuario))
    for i in c:
        cacheDeRespuesta.totalRespuestasId = i[0]

def obtenerSiguienteIdRespuesta():
    c = connexBD.obtenerConexionBD()
    c.execute('select max(idRespuesta) + 1 from Respuesta')
    p = c
    if c.arraysize>0:
        for i in c:
            print("Siguiente ID respuesta:",i[0])
            cacheDeRespuesta.idRespuestaNueva = i[0]
    else:
        cacheDeRespuesta.idRespuestaNueva = "0"

def insertarNuevaRespuesta(idRespuesta, descripcion, idUsuario, idPregunta):
    c = connexBD.obtenerConexionBD()
    c.execute('insert into Respuesta (idRespuesta, descripcion, idUsuario, idPregunta) values (%s, %s, %s, %s)',
              [idRespuesta, str(descripcion), idUsuario, idPregunta])
    connexBD.confirmarAccionBD()
    print("insertar respuesta")
    c.close()
    return True

def modificarRespuestaSeleccionada(descripcion, idRespuesta):
    c = connexBD.obtenerConexionBD()
    c.execute('update Respuesta set descripcion = %s where idrespuesta = %s',(descripcion,idRespuesta))
    connexBD.confirmarAccionBD()
    print("Modificación de respuesta realizada en Data Access Object")
    c.close()
    return True

def eliminarRespuestaSeleccionada(idRespuesta):
    c = connexBD.obtenerConexionBD()
    c.execute('delete from Respuesta where idRespuesta = %s',(idRespuesta,))
    connexBD.confirmarAccionBD()
    c.close()
    return True
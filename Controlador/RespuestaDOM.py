import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.RespuestaDAO as respuestaDAO

def obtenerRespuesta(idRespuesta,idPregunta):
    respuestaContenido = respuestaDAO.obtenerRespuesta(idRespuesta,idPregunta)
    return respuestaContenido

def obtenerIdsRespuestas(idPregunta):
    respuestaDAO.obtenerIdsRespuestas(idPregunta)

def obtenerTotalRespuestasIdPregunta(idPregunta):
    respuestaDAO.obtenerTotalRespuestasIdPregunta(idPregunta)

def escanearImagen(direccionImagen):
    respuestaDAO.escanearImagen(direccionImagen)

def obtenerSiguienteIdRespuesta():
    respuestaDAO.obtenerSiguienteIdRespuesta()

def insertarNuevaRespuesta(idRespuesta, descripcion, idUsuario, idPregunta):
    mensaje = respuestaDAO.insertarNuevaRespuesta(idRespuesta, descripcion, idUsuario, idPregunta)
    return mensaje

def obtenerIdsRespuestasPersonales(idPregunta,idUsuario):
    respuestaDAO.obtenerIdsRespuestasPersonales(idPregunta,idUsuario)

def obtenerTotalRespuestasIdPreguntaPersonales(idPregunta,idUsuario):
    respuestaDAO.obtenerTotalRespuestasIdPreguntaPersonales(idPregunta,idUsuario)

def modificarRespuestaSeleccionada(descripcion, idRespuesta):
    mensaje = respuestaDAO.modificarRespuestaSeleccionada(descripcion, idRespuesta)
    return mensaje

def eliminarRespuestaSeleccionada(idRespuesta):
    mensaje = respuestaDAO.eliminarRespuestaSeleccionada(idRespuesta)
    return mensaje
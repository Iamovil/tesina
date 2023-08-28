import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.PreguntaDAO as preguntaDAO

def obtenerPregunta(idPregunta):
    pregunta = preguntaDAO.obtenerPregunta(idPregunta)
    return pregunta

def obtenerTotalPreguntas():
    total = preguntaDAO.obtenerTotalPreguntas()
    return total

def obtenerSiguienteIdPregunta():
    siguienteID = preguntaDAO.obtenerSiguienteIdPregunta()
    return siguienteID

def obtenerIdsPreguntas():
    preguntaDAO.obtenerIdsPreguntas()

def insertarNuevaPregunta(idPregunta,descripcion,pregunta,imagen,idUsuario):
    mensaje = preguntaDAO.insertarNuevaPregunta(idPregunta,descripcion,pregunta,imagen,idUsuario)
    return mensaje

def obtenerPreguntaUsuarioPersonal(idUsuario):
    preguntaPersonal = preguntaDAO.obtenerPreguntaUsuarioPersonal(idUsuario)
    return preguntaPersonal

def obtenerTotalPreguntasPersonal(idUsuario):
    totalPreguntasPersonal = preguntaDAO.obtenerTotalPreguntasPersonal(idUsuario)
    return totalPreguntasPersonal

def obtenerIdsPreguntasPersonales(idUsuario):
    preguntaDAO.obtenerIdsPreguntasPersonales(idUsuario)

def modificarPreguntaSeleccionada(idPregunta, descripcion, pregunta, imagen):
    mensaje = preguntaDAO.modificarPreguntaSeleccionada(idPregunta, descripcion, pregunta, imagen)
    return mensaje

def eliminarPreguntaSeleccionada(idPregunta):
    mensaje = preguntaDAO.eliminarPreguntaSeleccionada(idPregunta)
    return mensaje

def obtenerTotalIDPreguntasContestadas(idUsuario):
    mensaje = preguntaDAO.obtenerTotalIDPreguntasContestadas(idUsuario)
    return mensaje

def obtenerIdsPreguntasContestadasPersonales(idUsuario):
    preguntaDAO.obtenerIdsPreguntasContestadasPersonales(idUsuario)
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.TratamientoHistorialDAO as tratamientoHistorialDAO

def obtenerSiguienteIdHistorial():
    siguienteID = tratamientoHistorialDAO.obtenerSiguienteIdHistorial()
    return siguienteID

def insertarNuevoHistorial(idHistorialTratamiento, idUsuario, idTratamiento):
    resultado = tratamientoHistorialDAO.insertarNuevoHistorial(idHistorialTratamiento, idUsuario, idTratamiento)
    return resultado

#OBTENER RECOMENDACIONES POR MES

def obtenerRecomendacionesEnero():
    tratamientoHistorialDAO.obtenerRecomendacionesEnero()

def obtenerRecomendacionesFebrero():
    tratamientoHistorialDAO.obtenerRecomendacionesFebrero()

def obtenerRecomendacionesMarzo():
    tratamientoHistorialDAO.obtenerRecomendacionesMarzo()

def obtenerRecomendacionesAbril():
    tratamientoHistorialDAO.obtenerRecomendacionesAbril()

def obtenerRecomendacionesMayo():
    tratamientoHistorialDAO.obtenerRecomendacionesMayo()

def obtenerRecomendacionesJunio():
    tratamientoHistorialDAO.obtenerRecomendacionesJunio()

def obtenerRecomendacionesJulio():
    tratamientoHistorialDAO.obtenerRecomendacionesJulio()

def obtenerRecomendacionesAgosto():
    tratamientoHistorialDAO.obtenerRecomendacionesAgosto()

def obtenerRecomendacionesSeptiembre():
    tratamientoHistorialDAO.obtenerRecomendacionesSeptiembre()

def obtenerRecomendacionesOctubre():
    tratamientoHistorialDAO.obtenerRecomendacionesOctubre()

def obtenerRecomendacionesNoviembre():
    tratamientoHistorialDAO.obtenerRecomendacionesNoviembre()

def obtenerRecomendacionesDiciembre():
    tratamientoHistorialDAO.obtenerRecomendacionesDiciembre()

#Obtener recomendaciones de experto por mes

def obtenerRecomendacionExpertoEnero(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoEnero(NombreUsuario)

def obtenerRecomendacionExpertoFebrero(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoFebrero(NombreUsuario)

def obtenerRecomendacionExpertoMarzo(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoMarzo(NombreUsuario)

def obtenerRecomendacionExpertoAbril(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoAbril(NombreUsuario)

def obtenerRecomendacionExpertoMayo(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoMayo(NombreUsuario)

def obtenerRecomendacionExpertoJunio(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoJunio(NombreUsuario)

def obtenerRecomendacionExpertoJulio(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoJulio(NombreUsuario)

def obtenerRecomendacionExpertoAgosto(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoAgosto(NombreUsuario)

def obtenerRecomendacionExpertoSeptiembre(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoSeptiembre(NombreUsuario)

def obtenerRecomendacionExpertoOctubre(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoOctubre(NombreUsuario)

def obtenerRecomendacionExpertoNoviembre(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoNoviembre(NombreUsuario)

def obtenerRecomendacionExpertoDiciembre(NombreUsuario):
    tratamientoHistorialDAO.obtenerRecomendacionExpertoDiciembre(NombreUsuario)

def comprobacionExistenciaUsuarioExperto(NombreUsuario):
    informacion = tratamientoHistorialDAO.comprobacionExistenciaUsuarioExperto(NombreUsuario)
    return informacion
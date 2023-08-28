import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.TratamientoDAO as tratamientoDAO

def obtenerSiguienteIdTratamiento():
    siguienteIDtratamiento = tratamientoDAO.obtenerSiguienteIdTratamiento()
    return siguienteIDtratamiento

def insertarNuevoTratamiento(idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen, idUsuario):
    mensaje = tratamientoDAO.insertarNuevoTratamiento(idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen, idUsuario)
    return mensaje

def obtenerTotalTratamientos():
    totalTratamientos = tratamientoDAO.obtenerTotalTratamientos()
    return totalTratamientos

def obtenerIdsTratamientos():
    tratamientoDAO.obtenerIdsTratamientos()

def obtenerTratamiento(idTratamiento):
    infoTratamiento = tratamientoDAO.obtenerTratamiento(idTratamiento)
    return infoTratamiento

def obtenerTratamientoCompleto(idTratamiento):
    infoCompletaTratamiento = tratamientoDAO.obtenerTratamientoCompleto(idTratamiento)
    return infoCompletaTratamiento

def modificarTratamientoSeleccionada(idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen,idUsuario):
    mensaje = tratamientoDAO.modificarTratamientoSeleccionada(idTratamiento, enfermedad, fungicida, marca, descripcion, precaucion, imagen,idUsuario)
    return mensaje

def eliminarTratamientoSeleccionado(idTratamiento):
    mensaje = tratamientoDAO.eliminarTratamientoSeleccionado(idTratamiento)
    return mensaje 

def obtenerIdsTratamientosReconocimiento(enfermedad):
    tratamientoDAO.obtenerIdsTratamientosReconocimiento(enfermedad)

def obtenerTotalTratamientosReconocimiento(enfermedad):
    total = tratamientoDAO.obtenerTotalTratamientosReconocimiento(enfermedad)
    return total
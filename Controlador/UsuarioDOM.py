import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.UsuarioDAO as usuarioDAO

    
def obtenerTodosUsuarios():
    usuarios = usuarioDAO.mostrarTodosUsuarios()
    return usuarios

def existeUsuario(correo,contra):
    mensaje = usuarioDAO.existeUsuario(str(correo),(contra))
    return mensaje

def insertarNuevoUsuario(idUsuario,nombre,apellido,correo,usuario,contra,tipoUsuario,grado,telefono):
    mensaje = usuarioDAO.insertarNuevoUsuario(idUsuario,nombre,apellido,correo,usuario,contra,tipoUsuario,grado,telefono)
    return mensaje

def obtenerNuevaIdUsuario():
    usuarioDAO.obtenerNuevaIdUsuario()

def obtenerNombreUsuario(idUsuario):
    nombreDeUsuario = usuarioDAO.obtenerNombreUsuario(idUsuario)
    return nombreDeUsuario

def obtenerTotalDeUsuarios():
    usuarioDAO.obtenerTotalDeUsuarios()

def obtenerIdsUsuarios():
    usuarioDAO.obtenerIdsUsuarios()

def obtenerInformacionUsuario(idUsuario):
    infoUsuario = usuarioDAO.obtenerInformacionUsuario(idUsuario)
    return infoUsuario

def modificarUsuarioSeleccionado(idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono):
    mensaje = usuarioDAO.modificarUsuarioSeleccionado(idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono)
    return mensaje

def eliminarUsuarioSeleccionado(idUsuario):
    mensaje = usuarioDAO.eliminarUsuarioSeleccionado(idUsuario)
    return mensaje

def enviarCorreoUsuariosComunes(usuario,preguntaUsC,descripcionUsC):
    usuarioDAO.enviarCorreoUsuariosComunes(usuario,preguntaUsC,descripcionUsC)

def verificacionExistenciaCorreo(correoIngresado):
    correo = usuarioDAO.verificacionExistenciaCorreo(correoIngresado)
    return correo

def enviarCorreoUsuarioRecuperacion(correo):
    usuarioDAO.enviarCorreoUsuarioRecuperacion(correo)

class userDAO:
    def __init__(self) -> None:
        pass
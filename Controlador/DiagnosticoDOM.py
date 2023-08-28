import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.DiagnosticoDAO as diagnosticoDAO

def obtenerSiguienteIdDiagnostico():
    idSiguienteDiagnostico = diagnosticoDAO.obtenerSiguienteIdDiagnostico()
    return idSiguienteDiagnostico

def insertarNuevoDiagnostico(idDiagnostico, imagen, diagnostico, idUsuario):
    resultado = diagnosticoDAO.insertarNuevoDiagnostico(idDiagnostico, imagen, diagnostico, idUsuario)
    return resultado


#OBTENER HISTORIAL DE DIAGNOSTICOS POR MES

def obtenerDiagnosticosEneroEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosEneroEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosFebreroEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosFebreroEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosMarzoEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosMarzoEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosAbrilEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosAbrilEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosMayoEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosMayoEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosJunioEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosJunioEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosJulioEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosJulioEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosAgostoEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosAgostoEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosSeptiembreEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosSeptiembreEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosOctubreEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosOctubreEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosNoviembreEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosNoviembreEnfermedad(NombreEnfermedad)

def obtenerDiagnosticosDiciembreEnfermedad(NombreEnfermedad):
    diagnosticoDAO.obtenerDiagnosticosDiciembreEnfermedad(NombreEnfermedad)
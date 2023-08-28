import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.BaseDeDatosDAO as baseDeDatosDAO


def respaldoBD():
    confirmacion = baseDeDatosDAO.respaldoBD()
    return confirmacion

def restauracionBD():
    confirmacion = baseDeDatosDAO.restauracionBD()
    return confirmacion
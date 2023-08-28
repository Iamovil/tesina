import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Modelo.Entrenamiento.escaneoDAO as escaneoDAO


def RealizarEscaneo(imagen):
    resultado = escaneoDAO.RealizarEscaneo(imagen)
    return resultado

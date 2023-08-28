import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Cache.CacheDeUsuario as cacheUsuario
import Cache.CacheDePregunta as cachePregunta
import Cache.CacheDeDiagnostico as cacheDiagnostico
import sqlite3 
import datetime
from PIL import Image

def obtenerSiguienteIdDiagnostico():
    c = connexBD.obtenerConexionBD()
    c.execute('select max(idDiagnostico) + 1 from Diagnostico')
    p = c
    if c.arraysize>0:
        for i in c:
            print("Siguiente ID diagnostico:",i[0])
            return i
    else:
        return 0
    
def insertarNuevoDiagnostico(idDiagnostico, imagen, diagnostico, idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('insert into Diagnostico (idDiagnostico, fecha, img, diagnostico, idUsuario) values (%s, %s, %s, %s, %s)',
              [idDiagnostico, datetime.datetime.now(),imagen,str(diagnostico), int(idUsuario)])
    connexBD.confirmarAccionBD()
    print("insertar diagnostico")
    c.close()
    return True

#OBTENER HISTORIAL DE DIAGNOSTICOS POR MES
def obtenerDiagnosticosEneroEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "01" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosEnero = i[0]
    c.close()

def obtenerDiagnosticosFebreroEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "02" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosFebrero = i[0]
    c.close()

def obtenerDiagnosticosMarzoEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "03" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosMarzo = i[0]
    c.close()

def obtenerDiagnosticosAbrilEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "04" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosAbril = i[0]
    c.close()

def obtenerDiagnosticosMayoEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "05" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosMayo = i[0]
    c.close()

def obtenerDiagnosticosJunioEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "06" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosJunio = i[0]
    c.close()

def obtenerDiagnosticosJulioEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "07" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosJulio = i[0]
    c.close()

def obtenerDiagnosticosAgostoEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "08" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosAgosto = i[0]
    c.close()

def obtenerDiagnosticosSeptiembreEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "09" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosSeptiembre = i[0]
    c.close()

def obtenerDiagnosticosOctubreEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "10" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosOctubre = i[0]
    c.close()

def obtenerDiagnosticosNoviembreEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "11" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosNoviembre = i[0]
    c.close()

def obtenerDiagnosticosDiciembreEnfermedad(NombreEnfermedad):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Diagnostico where MONTH(fecha) = "12" and YEAR(now()) = YEAR(fecha) and Diagnostico.diagnostico  == %s',(NombreEnfermedad,))
    for i in c:
       cacheDiagnostico.cantidadDiagnosticosDiciembre = i[0]
    c.close()
    
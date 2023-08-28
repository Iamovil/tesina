import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Cache.CacheDeTratamiento as cacheDeTratamiento
import Cache.CacheDeReporte as cacheReporte
import sqlite3 
import datetime

def obtenerSiguienteIdHistorial():
    c = connexBD.obtenerConexionBD()
    c.execute('select max(idHistorialTratamiento) + 1 from TratamientoHistorial')
    p = c
    if c.arraysize>0:
        for i in c:
            print("Siguiente ID TratamientoHistorial:",i[0])
            return i
    else:
        return 0
    
def insertarNuevoHistorial(idHistorialTratamiento, idUsuario, idTratamiento):
    c = connexBD.obtenerConexionBD() #Conexión a la base de datos
    c.execute('insert into TratamientoHistorial (idHistorialTratamiento, fecha, idUsuario, idTratamiento) values (%s, %s, %s, %s)',
              [idHistorialTratamiento,datetime.datetime.now(), idUsuario,idTratamiento])
    connexBD.confirmarAccionBD() #Confirmar la inserción de la base de datos
    print("insertar historial nuevo")
    c.close()
    return True

#OBTENER RECOMENDACIONES

def obtenerRecomendacionesEnero():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial MONTH(fecha) = "01" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesEnero = i[0]
    c.close()

def obtenerRecomendacionesFebrero():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "02" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesFebrero = i[0]
    c.close()

def obtenerRecomendacionesMarzo():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "03" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesMarzo = i[0]
    c.close()

def obtenerRecomendacionesAbril():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "04" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesAbril = i[0]
    c.close()

def obtenerRecomendacionesMayo():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "05" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesMayo = i[0]
    c.close()

def obtenerRecomendacionesJunio():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "06" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesJunio = i[0]
    c.close()

def obtenerRecomendacionesJulio():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "07" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesJulio = i[0]
    c.close()

def obtenerRecomendacionesAgosto():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "08" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesAgosto = i[0]
    c.close()

def obtenerRecomendacionesSeptiembre():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "09" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesSeptiembre = i[0]
    c.close()

def obtenerRecomendacionesOctubre():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "10" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesOctubre = i[0]
    c.close()

def obtenerRecomendacionesNoviembre():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "11" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesNoviembre = i[0]
    c.close()

def obtenerRecomendacionesDiciembre():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial where MONTH(fecha) = "12" and YEAR(now()) = YEAR(fecha)')
    for i in c:
       cacheReporte.recomendacionesDiciembre = i[0]
    c.close()

## Obtener recomendaciones de expertos de acuerdo al mes

def obtenerRecomendacionExpertoEnero(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "01" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoEnero = i[0]
    c.close()

def obtenerRecomendacionExpertoFebrero(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "02" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoFebrero = i[0]
    c.close()

def obtenerRecomendacionExpertoMarzo(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "03" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoMarzo = i[0]
    c.close()

def obtenerRecomendacionExpertoAbril(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "04" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoAbril = i[0]
    c.close()

def obtenerRecomendacionExpertoMayo(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "05" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoMayo = i[0]
    c.close()

def obtenerRecomendacionExpertoJunio(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "06" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoJunio = i[0]
    c.close()

def obtenerRecomendacionExpertoJulio(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "07" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoJulio = i[0]
    c.close()

def obtenerRecomendacionExpertoAgosto(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "08" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoAgosto = i[0]
    c.close()

def obtenerRecomendacionExpertoSeptiembre(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "09" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoSeptiembre = i[0]
    c.close()

def obtenerRecomendacionExpertoOctubre(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "10" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoOctubre = i[0]
    c.close()

def obtenerRecomendacionExpertoNoviembre(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "11" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoNoviembre = i[0]
    c.close()

def obtenerRecomendacionExpertoDiciembre(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from TratamientoHistorial inner join Tratamiento on Tratamiento.idTratamiento = TratamientoHistorial.idTratamiento inner join Usuario on Tratamiento.idUsuario = Usuario.idUsuario where MONTH(TratamientoHistorial.fecha) = "12" and YEAR(now()) = YEAR(TratamientoHistorial.fecha) and Usuario.usuario = %s',(NombreUsuario,))
    for i in c:
        cacheReporte.recomendacionesExpertoDiciembre = i[0]
    c.close()

def comprobacionExistenciaUsuarioExperto(NombreUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select * from Usuario where usuario = %s and tipoUsuario = "2"', (NombreUsuario,))
    if c.arraysize > 0:
        for i in c: 
            return i
    c.close()
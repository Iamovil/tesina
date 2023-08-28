import Modelo.connnectDB as connexBD
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import Cache.CacheDeUsuario as cacheUsuario
import sqlite3
import smtplib 
from email.message import EmailMessage

def mostrarTodosUsuarios():
    c = connexBD.obtenerConexionBD()
    c.execute('select * from Usuario')
    p = c
    for i in c:
        print("idUsuario", i[0])
        print("nombre", i[1])
        print("apellido", i[2])
        print("correo", i[3])
        print("usuario", i[4])
        print("contraseña", i[5])
        print("tipousuario", i[6])
        print("gradp", i[7])
        print("telefono", i[8])
    c.close
    return p

def obtenerTotalDeUsuarios():
    c = connexBD.obtenerConexionBD()
    c.execute('select count(*) from Usuario ')
    for i in c:
        cacheUsuario.totalUsuarios = i[0]

def obtenerIdsUsuarios():
    c = connexBD.obtenerConexionBD()
    c.execute('select idUsuario from Usuario')
    p = c
    for i in c:
        cacheUsuario.idsUsuario.append(i[0])

def obtenerInformacionUsuario(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono from Usuario where idUsuario = %s',(idUsuario,))
    p = c
    for i in c:
        return i
    c.close

def obtenerNuevaIdUsuario():
    c = connexBD.obtenerConexionBD()
    c.execute('select (count(*) + 2) as newUser from Usuario')
    if c.arraysize > 0:
        for i in c:
            cacheUsuario.idNuevoUsuario = i[0]

def insertarNuevoUsuario(idUsuario,nombre,apellido,correo,usuario,contra,tipoUsuario,grado,telefono):
    c = connexBD.obtenerConexionBD()
    c.execute('insert into Usuario (idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(idUsuario+1,nombre,apellido,correo,usuario,contra,tipoUsuario,grado,telefono))
    connexBD.confirmarAccionBD()
    c.fetchall()
    c.close
    return True

#Entradas:
# La función recibe el correo y contraseña del usuario
# Salidas:
# El sistema informa si el usuario existe con True y si no existe con False
# Función de comprobación de inicio de sesión del usuario (existencia del usuario)
def existeUsuario(correo,contra):
    c = connexBD.obtenerConexionBD() #Conexión a la base de datos
    # Ejecuta la consulta de inserción en la base de datos
    query = ("SELECT * FROM Usuario WHERE CORREO = %s AND contraseña = %s") #Comprobación de datos
    values = (correo, contra,)
    c.execute(query, values) #Ejecución de la consulta
    p = c
    if c.arraysize > 0:
        for i in c: #Se almacena la información del usuario conectado al sistema de forma temporal
            cacheUsuario.idUsuario = i[0]
            cacheUsuario.nombre = i[1]
            cacheUsuario.apellido = i[2]
            cacheUsuario.correo = i[3]
            cacheUsuario.usuario = i[4]
            cacheUsuario.contra = i[5]
            cacheUsuario.tipoUsuario = i[6]
            cacheUsuario.grado = i[7]
            cacheUsuario.telefono = i[8]
            if(i[3] == correo and i[5] == contra):
                return True #El usuario existe
        c.close
        return False #No existe el usuario
    else:
        c.close
        return False

def obtenerNombreUsuario(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('select Usuario from Usuario where idUsuario = %s', (idUsuario,))
    p = c
    for i in c:
        nombreUsuario = i[0]
        return nombreUsuario


def modificarUsuarioSeleccionado(idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono):
    c = connexBD.obtenerConexionBD()
    c.execute('update Usuario set nombre = %s,apellido = %s,correo = %s,usuario = %s,contraseña = %s,tipoUsuario = %s, grado = %s, telefono = %s  where idUsuario = %s',(nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono,idUsuario))
    connexBD.confirmarAccionBD()
    print("Modificación de usuario realizada en Data Access Object")
    c.close()
    return True
    
def eliminarUsuarioSeleccionado(idUsuario):
    c = connexBD.obtenerConexionBD()
    c.execute('delete from Usuario where idUsuario = %s',(str(idUsuario),))
    connexBD.confirmarAccionBD()
    c.close()
    return True

def enviarCorreoUsuariosComunes(usuario,preguntaUsC,descripcionUsC):
    print("Envio de correoDAO")
    c = connexBD.obtenerConexionBD()
    c.execute('select * from Usuario')
    p = c
    for i in c:
        if(i[6] == "2" or i[6] == 2):
            email_subject = "Nuevo posteo de pregunta en la comunidad! - DPE" 
            sender_email_address = "DPE_OFFICIAL@outlook.com" 
            receiver_email_address = str(i[3])
            email_smtp = "smtp.office365.com"
            email_password = "DPEOFFICIAL*1"

            # Create an email message object 
            message = EmailMessage() 

            # Configure email headers 
            message['Subject'] = email_subject 
            message['From'] = sender_email_address 
            message['To'] = receiver_email_address 
            mensaje = f"""
                ¡Hola!

                Te informamos que el usuario {usuario} acaba de publicar una nueva pregunta en la comunidad:

                Título de la pregunta: {preguntaUsC}
                Descripción de la pregunta: {descripcionUsC}

                ¡Ayuda a la comunidad y contribuye con tu conocimiento! ¿Te animas a responder la pregunta?

                Saludos cordiales,
                El equipo de la comunidad de DPE
                """
            # Set email body text 
            message.set_content(mensaje) 

            # Set smtp server and port 
            server = smtplib.SMTP(email_smtp, '587') 

            # Identify this client to the SMTP server 
            server.ehlo() 

            # Secure the SMTP connection 
            server.starttls() 

            # Login to email account 
            server.login(sender_email_address, email_password) 

            # Send email 
            server.send_message(message) 

            # Close connection to server 
            server.quit()
    c.close

def verificacionExistenciaCorreo(correoIngresado):
    c = connexBD.obtenerConexionBD() 
    c.execute('select correo from Usuario where correo = %s',(str(correoIngresado),))
    p = c
    for i in c:
        correoUsuario = i[0]
        return correoUsuario
    c.close()

def enviarCorreoUsuarioRecuperacion(correo):
    print("Envio de correoDAO")
    c = connexBD.obtenerConexionBD()
    c.execute('select * from Usuario where correo = %s',(str(correo),))
    p = c
    for i in c:
        email_subject = "La recuperación de tu contraseña ya está aquí! - DPE" 
        sender_email_address = "DPE_OFFICIAL@outlook.com" 
        receiver_email_address = str(correo)
        email_smtp = "smtp.office365.com"
        email_password = "DPEOFFICIAL*1"

        # Create an email message object 
        message = EmailMessage() 

        # Configure email headers 
        message['Subject'] = email_subject 
        message['From'] = sender_email_address 
        message['To'] = receiver_email_address 
        mensaje = f"""
            ¡Hola {i[1]}!

            Aquí tienes la contraseña de tu cuenta que pediste:

            correo: {correo}
            Contraseña: {i[5]}

            Te recomendamos cambiar tu contraseña constantemente

            ¡La seguridad es primero!

            Saludos cordiales,
            El equipo de la comunidad de DPE
            """
        # Set email body text 
        message.set_content(mensaje) 

        # Set smtp server and port 
        server = smtplib.SMTP(email_smtp, '587') 

        # Identify this client to the SMTP server 
        server.ehlo() 

        # Secure the SMTP connection 
        server.starttls() 

        # Login to email account 
        server.login(sender_email_address, email_password) 

        # Send email 
        server.send_message(message) 

        # Close connection to server 
        server.quit()
    c.close
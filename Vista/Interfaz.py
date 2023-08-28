from kivy import utils
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.utils import get_color_from_hex, rgba
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.hero import MDHeroFrom
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDIconButton, MDRectangleFlatIconButton, MDFillRoundFlatButton,MDFillRoundFlatIconButton
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel
from kivy.uix.slider import Slider
from kivymd.uix.list import TwoLineListItem,ThreeLineListItem, TwoLineAvatarListItem, ImageLeftWidget, IconLeftWidget,ThreeLineIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.utils import asynckivy
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Controlador import UsuarioDOM as usuarioDOM
from Controlador import PreguntaDOM as preguntaDOM
from Controlador import RespuestaDOM as respuestaDOM
from Controlador import BaseDeDatosDOM as baseDeDatosDOM
from Controlador import TratamientoDOM as tratamientoDOM
from Controlador import escaneoDOM as EscaneoDOM
from Controlador import DiagnosticoDOM as diagnosticoDOM
from Controlador import TratamientoHistorialDOM as tratamientoHistorialDOM
from Cache import CacheDeUsuario as cacheUsuario
from Cache import CacheDePregunta as cachePregunta
from Cache import CacheDeRespuesta as cacheRespuesta
from Cache import CacheDeTratamiento as cacheTratamiento
from Cache import CacheReconocimiento as cacheReconocimiento
from Cache import CacheDeReporte as cacheReporte
from Cache import CacheDeDiagnostico as cacheDiagnostico
from kivy.graphics.texture import Texture
from io import BytesIO
from PIL import Image as PIL_Image
import tkinter as tk
from tkinter import filedialog
from functools import partial
from kivy.metrics import dp
import tempfile
import os
import uuid
import time
import threading
import datetime
from kivy.graphics import Color
import cv2
import PySimpleGUI as sg

# REPORTES
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


Window.size=(300,450)
binario = 1
class Test(MDApp):
    dialog = None #
    white_color = get_color_from_hex('#FFFFFF')
    binario = 1
    file_path = ""
    def build(self):
        
        return Builder.load_file("Interfaz.kv")

    def menu_preguntas(self):
        print("menu de preguntas")
        cachePregunta.confirmacionBorrado = False
        total = preguntaDOM.obtenerTotalPreguntasPersonal(cacheUsuario.idUsuario)
        box_layout = self.root.ids.gridPregPersonales
        box_layout.clear_widgets()
        print("Total de preguntas registradas al momento: ", total[0])
        if(total[0] == 0 or total[0] == "" or total[0] == None):
            print("No preguntas")
        else:
            preguntaDOM.obtenerIdsPreguntasPersonales(cacheUsuario.idUsuario)
            print(cachePregunta.idsPreguntas[0], "")
            for i in cachePregunta.idsPreguntas:
                pregunta = preguntaDOM.obtenerPregunta(i)
                # Generar un nombre de archivo único para la imagen
                image_file = str(uuid.uuid4()) + ".jpg"

                cachePregunta.archivosDePregunta.append(image_file)
                # Guardar la imagen en disco con el nombre de archivo único
                with open(image_file, "wb") as f:
                    f.write(pregunta[3])
                nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[4])
                tile = MDSmartTile(source=image_file, radius=20, box_radius=[0, 0, 24, 24], lines=2, size=("120dp", "120dp"))
                def open_modificar(obj,pregunta = pregunta[2],descripcion = pregunta[1],imagen = pregunta[3],IDPregunta = i):
                        self.abrirFormularioDePreguntaModificar(pregunta,descripcion,imagen,IDPregunta,obj)
                tile.bind(on_release=open_modificar)
                descr = ThreeLineListItem(text=pregunta[2], secondary_text=pregunta[1], tertiary_text=nombreUsuario, font_style= "H6", theme_text_color= "Custom", text_color = "#FFFFFF", secondary_theme_text_color = "Custom" , secondary_text_color = "#FFFFFF",tertiary_theme_text_color = "Custom",tertiary_text_color = "#FFFFFF")
                # if(cacheUsuario.idUsuario == pregunta[4]):
                #     iconoModificacion = IconLeftWidget(icon="account-circle")
                #     descr.add_widget(iconoModificacion)
                tile.add_widget(descr)
                box_layout.add_widget(tile)
            self.dialog = MDDialog(
                title = 'Aviso',
                text = f"Bienvenid@ a tus preguntas!",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.eliminarArchivosPreguntaConfirmado
                    ),
                ],
            )
            self.dialog.open()
            cachePregunta.idsPreguntas.clear()
        inter = self.root.ids.navItemComm
        ButtonAddPregunta = MDFloatingActionButton(icon = "plus",
                            md_bg_color = "#383EF1")
        ButtonAddPregunta.bind(on_release = self.abrirFormularioDePreguntas)
        inter.add_widget(ButtonAddPregunta)

    
    def abrirPreguntasRespondidasPersonales(self):
        print("menu de preguntas respondidas")
        cachePregunta.confirmacionBorrado = False
        total = preguntaDOM.obtenerTotalIDPreguntasContestadas(cacheUsuario.idUsuario)
        box_layout = self.root.ids.gridPregPersonales_Resp_Per
        box_layout.clear_widgets()
        print("Total de preguntas registradas al momento: ", total[0])
        if(total[0] == 0 or total[0] == "" or total[0] == None):
            print("No preguntas")
        else:   
            preguntaDOM.obtenerIdsPreguntasContestadasPersonales(cacheUsuario.idUsuario)
            print(cachePregunta.idsPreguntas[0], "")
            for i in cachePregunta.idsPreguntas:
                pregunta = preguntaDOM.obtenerPregunta(i)
                # Generar un nombre de archivo único para la imagen
                image_file = str(uuid.uuid4()) + ".jpg"
                cachePregunta.archivosDePregunta.append(image_file)
                # Guardar la imagen en disco con el nombre de archivo único
                with open(image_file, "wb") as f:
                    f.write(pregunta[3])
                nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[4])
                tile = MDSmartTile(source=image_file, radius=20, box_radius=[0, 0, 24, 24], lines=2, size=("120dp", "120dp"))
                def open_responses(obj, pregunta_2=pregunta[2], pregunta_1=pregunta[1], pregunta_0=i,usuario = cacheUsuario.idUsuario):
                    self.abrirRespuestasComunidadPersonales(pregunta_2, pregunta_1, pregunta_0,usuario, obj)
                tile.bind(on_release=open_responses)
                descr = ThreeLineListItem(text=pregunta[2], secondary_text=pregunta[1], tertiary_text=nombreUsuario, font_style= "H6", theme_text_color= "Custom", text_color = "#FFFFFF", secondary_theme_text_color = "Custom" , secondary_text_color = "#FFFFFF",tertiary_theme_text_color = "Custom",tertiary_text_color = "#FFFFFF")
                # if(cacheUsuario.idUsuario == pregunta[4]):
                #     iconoModificacion = IconLeftWidget(icon="account-circle")
                #     descr.add_widget(iconoModificacion)
                tile.add_widget(descr)
                box_layout.add_widget(tile)
            cachePregunta.idsPreguntas.clear()
        inter = self.root.ids.navItemComm
        ButtonAddPregunta = MDFloatingActionButton(icon = "plus",
                            md_bg_color = self.theme_cls.primary_color)
        ButtonAddPregunta.bind(on_release = self.abrirFormularioDePreguntas)
        inter.add_widget(ButtonAddPregunta)

    def obtener(self):
        usuarioDOM.obtenerTodosUsuarios()

    def accederAlRegistroUsuario(self):
        self.root.current_heroes = ["hero"]
        self.root.current = "screen R"

    def enviarCorreoDeRecuperacionCorreo(self):
        correoValidado = False
        if (('.com' in self.root.ids.textcorreoRecuperacion.text) or ('.mx' in self.root.ids.textcorreoRecuperacion.text) or ('.edu.mx' in self.root.ids.textcorreoRecuperacion.text)) and (('@outlook' in self.root.ids.textcorreoRecuperacion.text) or ('@gmail' in self.root.ids.textcorreoRecuperacion.text) or ('@upemor' in self.root.ids.textcorreoRecuperacion.text) or ('@hotmail' in self.root.ids.textcorreoRecuperacion.text)):
            correoValidado = True
        
        if(correoValidado == True):
            correo = usuarioDOM.verificacionExistenciaCorreo(self.root.ids.textcorreoRecuperacion.text)
            if (correo == "" or correo == " " or correo == None):
                self.dialog = MDDialog(
                    title = 'Error al enviar',
                    text = f"El correo que ingreso no existe o no está bien escrito",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;
            else:
                usuarioDOM.enviarCorreoUsuarioRecuperacion(correo)
                self.dialog = MDDialog(
                    title = 'Recuperación de contraseña',
                    text = f"Hemos enviado un correo con tu contraseña, verifica tu buzón!",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;
        else:
            self.dialog = MDDialog(
                title = 'Error al enviar',
                text = f"El correo que ingreso no existe o no está bien escrito",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            return;



    # Función de registro de un nuevoUsuario
    def registrarNuevoUsuario(self):
        correoValidado = False
        if(self.root.ids.checkGdAcademico.active == True):
            experto = 2
        else:
            experto = 1
        usuarioDOM.obtenerNuevaIdUsuario()
        print(cacheUsuario.idNuevoUsuario)
        if (('.com' in self.root.ids.correo_reg.text) or ('.mx' in self.root.ids.correo_reg.text) or ('.edu.mx' in self.root.ids.correo_reg.text)) and (('@outlook' in self.root.ids.correo_reg.text) or ('@gmail' in self.root.ids.correo_reg.text) or ('@upemor' in self.root.ids.correo_reg.text) or ('@hotmail' in self.root.ids.correo_reg.text)):
            correoValidado = True
        try:
            if(self.root.ids.nombre_reg.text == "" or  self.root.ids.apellido_reg.text == "" or self.root.ids.correo_reg.text == "" or self.root.ids.nombreUsuario_reg.text == "" or self.root.ids.password_reg.text == "" or correoValidado == False):
                self.dialog = MDDialog(
                    title = 'Aviso',
                    text = f"Registre su información correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;
            
            valor = usuarioDOM.existeUsuario(self.root.ids.correo_reg.text,self.root.ids.password_reg.text)
            if valor == True:
                self.dialog = MDDialog(
                    title = 'Error de registro',
                    text = f"El usuario que ha intentado registrar ya se encuentra en uso",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;

            mensaje = usuarioDOM.insertarNuevoUsuario(cacheUsuario.idNuevoUsuario,self.root.ids.nombre_reg.text,self.root.ids.apellido_reg.text,self.root.ids.correo_reg.text,self.root.ids.nombreUsuario_reg.text,self.root.ids.password_reg.text,experto,self.root.ids.grado_reg.text,self.root.ids.telefono_reg.text)
            if mensaje == True:
                self.dialog = MDDialog(
                title = 'Registro exitoso',
                text = f"Se ha registrado correctamente",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            cacheUsuario.idNuevoUsuario = ""
            self.root.ids.nombre_reg.text = ""
            self.root.ids.apellido_reg.text = ""
            self.root.ids.correo_reg.text = ""
            self.root.ids.nombreUsuario_reg.text = ""
            self.root.ids.password_reg.text = ""
            self.root.ids.grado_reg.text = ""
            self.root.ids.telefono_reg.text = ""
            self.root.ids.checkGdAcademico.active = False
            
        except:
            self.dialog = MDDialog(
                title = 'Error al registrar',
                text = f"Ha ocurrido un error al intentar registrarse",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()

    #Entradas:
    # La función no recibe ninguna entrada
    # Salidas:
    # El usuario entra a la interfaz del menú si accede de forma correcta
    # Función de inicio de sesión
    def inicioSesion(self):
        valor = usuarioDOM.existeUsuario(self.root.ids.user.text,self.root.ids.password.text) #Comprobación de que el usuario existe
        if valor == True: #Si existe se transporta al usuario a la interfaz del menú
            self.root.current_heroes = ["hero"]
            self.root.current = "screen B"
            print(cacheUsuario.nombre)
            self.root.ids.user.text = ""
            self.root.ids.password.text = ""
        else: #Si no se colocan las credenciales de forma correcta, se ejecuta un aviso de advertencia al usuario sobre el error
            self.dialog = MDDialog(
                title = 'Login',
                text = f"Nombre de usuario o contraseña incorrectos",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
    
    def buscarImagenPregunta(self):
        # Crea una ventana raíz de tkinter (no se mostrará en la pantalla)
        root = tk.Tk()
        root.withdraw()

        # Muestra el cuadro de diálogo para seleccionar un archivo y filtra por archivos de imagen JPEG o JPG
        file_path = filedialog.askopenfilename(filetypes=[("JPEG", "*.jpg"), ("JPEG", "*.jpeg")])

        # Imprime la ruta del archivo seleccionado
        print("La imagen seleccionada es:", file_path)

        cachePregunta.file_path = file_path
        
    
    def registrarPregunta(self):
        siguienteIDPreg = preguntaDOM.obtenerSiguienteIdPregunta()
        if self.root.ids.descripcion_preg.text != "" and self.root.ids.pregunta_preg.text != "" and cachePregunta.file_path != "":
            with open(cachePregunta.file_path, "rb") as f:
                imagen_bytes = f.read()
            mensaje = preguntaDOM.insertarNuevaPregunta(int(siguienteIDPreg[0]),self.root.ids.descripcion_preg.text,self.root.ids.pregunta_preg.text,imagen_bytes,cacheUsuario.idUsuario)
            if mensaje == True:
                print("regreso")
                self.dialog = MDDialog(
                    title = 'Registro exitoso',
                    text = f"Se ha registrado correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                if(cacheUsuario.tipoUsuario == "1" or cacheUsuario.tipoUsuario == 1):
                    usuarioDOM.enviarCorreoUsuariosComunes(cacheUsuario.usuario,self.root.ids.pregunta_preg.text,self.root.ids.descripcion_preg.text)

    def modificarPreguntaSeleccionada(self):
        if self.root.ids.descripcion_preg_mod.text != "" and self.root.ids.pregunta_preg_mod.text != "" and cachePregunta.file_path != "":
            print("Segunda fase",cacheUsuario.idUsuario)
            with open(cachePregunta.file_path, "rb") as f:
                imagen_bytes = f.read()
            mensaje = preguntaDOM.modificarPreguntaSeleccionada(cachePregunta.idModificacionPregunta,self.root.ids.descripcion_preg_mod.text,self.root.ids.pregunta_preg_mod.text,imagen_bytes)
            if mensaje == True:
                print("Modificación realizada")
                self.dialog = MDDialog(
                    title = 'Aviso de acción',
                    text = f"Se ha realizado la modificación correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
            os.remove(cachePregunta.file_path)
    
    def eliminarPreguntaSeleccionada(self):
        print("Eliminar Pregunta seleccionada")
        self.dialog = MDDialog(
            title = 'Advertencia',
            text = f"Desea eliminar la pregunta?",
            buttons = [
                MDFlatButton(
                    text = "Eliminar", text_color = self.theme_cls.accent_color,
                    on_release = self.eliminarPreguntaConfirmado
                ),
                MDFlatButton(
                    text = "Cancelar", text_color = self.theme_cls.accent_color,
                    on_release = self.close_dialog
                ),
            ],
        )
        self.dialog.open()
    
    def eliminarPreguntaConfirmado(self,obj):
        self.dialog.dismiss()
        mensaje = preguntaDOM.eliminarPreguntaSeleccionada(cachePregunta.idModificacionPregunta)
        if mensaje == True:
            self.dialog = MDDialog(
                    title = 'Aviso de acción',
                    text = f"Se ha realizado la eliminación correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        os.remove(cachePregunta.file_path)
        self.root.current_heroes = ["hero"]
        self.root.current = "screen B"

    def regresarVentanaModificar(self):
        os.remove(cachePregunta.file_path)
        self.root.current_heroes = ["hero"]
        self.root.current = "screen B"



    # Función de busqueda de preguntas
    def interfazPreguntas(self):
        cachePregunta.confirmacionBorrado = False
        total = preguntaDOM.obtenerTotalPreguntas()
        box_layout = self.root.ids.gridPreg
        box_layout.clear_widgets()
        print("Total de preguntas registradas al momento: ", total[0])
        if(total[0] == 0 or total[0] == "" or total == "0" or total[0] == None):
            print("No preguntas")
        else:   
            preguntaDOM.obtenerIdsPreguntas()
            print(cachePregunta.idsPreguntas[0], "")
            for i in cachePregunta.idsPreguntas:
                pregunta = preguntaDOM.obtenerPregunta(i)
                # Generar un nombre de archivo único para la imagen
                image_file = str(uuid.uuid4()) + ".jpg"
                cachePregunta.archivosDePregunta.append(image_file)
                # Guardar la imagen en disco con el nombre de archivo único
                with open(image_file, "wb") as f:
                    f.write(pregunta[3])
                nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[4])
                tile = MDSmartTile(source=image_file, radius=20, box_radius=[0, 0, 24, 24], lines=2, size=("120dp", "120dp"))
                def open_responses(obj, pregunta_2=pregunta[2], pregunta_1=pregunta[1], pregunta_0=i,usuario = pregunta[4]):
                    self.abrirRespuestasComunidad(pregunta_2, pregunta_1, pregunta_0,usuario, obj)
                tile.bind(on_release=open_responses)
                descr = ThreeLineListItem(text=pregunta[2], secondary_text=pregunta[1], tertiary_text=nombreUsuario, font_style= "H6", theme_text_color= "Custom", text_color = "#FFFFFF", secondary_theme_text_color = "Custom" , secondary_text_color = "#FFFFFF",tertiary_theme_text_color = "Custom",tertiary_text_color = "#FFFFFF")
                tile.add_widget(descr)
                box_layout.add_widget(tile)
            cachePregunta.idsPreguntas.clear()
            self.dialog = MDDialog(
                title = 'Aviso',
                text = f"Bienvenidos a la comunidad!",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.eliminarArchivosPreguntaConfirmado
                    ),
                ],
            )
            self.dialog.open()
        inter = self.root.ids.navItemComm
        ButtonAddPregunta = MDFloatingActionButton(icon = "plus",
                            md_bg_color = "#383EF1")
        ButtonAddPregunta.bind(on_release = self.abrirFormularioDePreguntas)
        inter.add_widget(ButtonAddPregunta)
        
    def eliminarArchivosPreguntaConfirmado(self,obj):
        self.dialog.dismiss()
        self.eliminarArchivos()

    def abrirFormularioDePreguntas(self,obj):
        self.root.current_heroes = ["hero"]
        self.root.current = "screen Pr"

    def abrirFormularioDePreguntaModificar(self,pregunta,descripcion,imagen,IDPregunta,obj):
        self.eliminarArchivos()
        self.root.ids.pregunta_preg_mod.text = pregunta
        self.root.ids.descripcion_preg_mod.text = descripcion
        self.root.current_heroes = ["hero"]
        self.root.current = "screen PrMd"
        image_file = str(uuid.uuid4()) + ".jpg"
        with open(image_file, "wb") as f:
            f.write(imagen)
        cachePregunta.file_path = image_file
        cachePregunta.idModificacionPregunta = IDPregunta
        

    def eliminarArchivos(self):
        if(cachePregunta.archivosDePregunta.count != 0):
            for i in cachePregunta.archivosDePregunta:
                os.remove(i)
            cachePregunta.confirmacionBorrado = True
            cachePregunta.archivosDePregunta.clear()
    
    def eliminarArchivosTratamiento(self):
        if(cacheTratamiento.archivosDeTratamiento.count != 0):
            for i in cacheTratamiento.archivosDeTratamiento:
                os.remove(i)
            cacheTratamiento.confirmacionBorrado = True
            cacheTratamiento.archivosDeTratamiento.clear()

    def abrirRespuestasComunidad(self, pregunta, descripcion,pregunta_0,usuario, obj):
        self.eliminarArchivos()
        self.root.current_heroes = ["hero"]
        self.root.current = "screen Respuesta"      
        cacheRespuesta.idPreguntaRespuestaNueva = pregunta_0
        cacheRespuesta.idUsuarioRespuestaNueva = cacheUsuario.idUsuario
        boxInfoPregunta = self.root.ids.gridinfoRespuesta_Comunidad
        boxInfoPregunta.clear_widgets()
        boxInfoPregunta.size_hint_x = 1
        boxInfoPregunta.size_hint_y = 1
        label = MDLabel()
        label.text = pregunta
        label.halign = "center"
        label.valign = "top"
        label.size_hint_y = None
        label.height = label.texture_size[1] + dp(20)
        label.bold = True
        # label.padding = ("15dp", "15dp", "15dp", "15dp")
        label.text_color = self.theme_cls.text_color
        boxInfoPregunta.add_widget(label)

        #Space
        spaceDesc = MDAnchorLayout(size_hint_y = None, height = "5dp")
        boxInfoPregunta.add_widget(spaceDesc)

        label2 = MDLabel()
        label2.text = descripcion
        label2.halign = "justify"
        label2.valign = "top"
        label2.size_hint_y = None
        label2.height = label2.texture_size[1] + dp(20)
        # label.padding = ("15dp", "15dp", "15dp", "15dp")
        label2.text_color = self.theme_cls.text_color
        boxInfoPregunta.add_widget(label2)
        boxInfoPregunta.padding = [dp(1), dp(1), dp(1), 0]

        lista_respuestas = self.root.ids.lista_respuestas
        lista_respuestas.clear_widgets()
        respuestaDOM.obtenerIdsRespuestas(pregunta_0)
        respuestaDOM.obtenerTotalRespuestasIdPregunta(pregunta_0)
        if cacheRespuesta.totalRespuestasId == 0 or cacheRespuesta.totalRespuestasId == "" or cacheRespuesta.totalRespuestasId == None:
            print("Sin respuestas")
        else:
            for i in cacheRespuesta.idsRespuestas:
                pregunta = respuestaDOM.obtenerRespuesta(i,pregunta_0)
                # Generar un nombre de archivo único para la imagen
                image_file = str(uuid.uuid4()) + ".jpg"
                cacheRespuesta.archivosDeRespuesta.append(image_file)
                # Guardar la imagen en disco con el nombre de archivo único
                # with open(image_file, "wb") as f:
                #     f.write(pregunta[2])
                nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[2])
                
                item = TwoLineListItem(text=nombreUsuario, secondary_text=pregunta[1], secondary_font_style = "Caption")

                # item.height = item.texture_size[1] + dp(20)
                lista_respuestas.add_widget(item)
        cacheRespuesta.idsRespuestas.clear()
        
        # ################################################
        # RESPUESTAS PERSONALES EN LA PREGUNTA SELECCIONADA
    def abrirRespuestasComunidadPersonales(self,pregunta, descripcion,pregunta_0,usuario, obj):
        self.eliminarArchivos()
        self.root.current_heroes = ["hero"]
        self.root.current = "screen RespuestaMod"      
        cacheRespuesta.idPreguntaRespuestaNueva = pregunta_0
        cacheRespuesta.idUsuarioRespuestaNueva = cacheUsuario.idUsuario
        boxInfoPregunta = self.root.ids.gridinfo_Mod_Resp
        boxInfoPregunta.clear_widgets()
        boxInfoPregunta.size_hint_x = 1
        boxInfoPregunta.size_hint_y = 1
        label = MDLabel()
        label.text = pregunta
        label.halign = "center"
        label.valign = "top"
        label.size_hint_y = None
        label.height = label.texture_size[1] + dp(20)
        label.bold = True
        # label.padding = ("15dp", "15dp", "15dp", "15dp")
        label.text_color = self.theme_cls.text_color
        boxInfoPregunta.add_widget(label)

        label2 = MDLabel()
        label2.text = descripcion
        label2.halign = "justify"
        label2.valign = "top"
        label2.size_hint_y = None
        label2.height = label2.texture_size[1] + dp(20)
        # label.padding = ("15dp", "15dp", "15dp", "15dp")
        label2.text_color = self.theme_cls.text_color
        boxInfoPregunta.add_widget(label2)
        boxInfoPregunta.padding = [dp(1), dp(1), dp(1), 0]

        lista_respuestas = self.root.ids.lista_respuestas_Modf
        lista_respuestas.clear_widgets()
        respuestaDOM.obtenerIdsRespuestasPersonales(pregunta_0,cacheUsuario.idUsuario)
        respuestaDOM.obtenerTotalRespuestasIdPreguntaPersonales(pregunta_0,cacheUsuario.idUsuario)
        if cacheRespuesta.totalRespuestasId == 0 or cacheRespuesta.totalRespuestasId == "" or cacheRespuesta.totalRespuestasId == None:
            print("Sin respuestas")
        else:
            print(cacheRespuesta.idsRespuestas[0], "")
            for i in cacheRespuesta.idsRespuestas:
                pregunta = respuestaDOM.obtenerRespuesta(i,pregunta_0)
                # Generar un nombre de archivo único para la imagen
                image_file = str(uuid.uuid4()) + ".jpg"
                cacheRespuesta.archivosDeRespuesta.append(image_file)
                # Guardar la imagen en disco con el nombre de archivo único
                # with open(image_file, "wb") as f:
                #     f.write(pregunta[2])
                nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[2])
                
                item = TwoLineListItem(text=nombreUsuario, secondary_text=pregunta[1])

                def open_responses(idPreg = pregunta_0,usuarioid = usuario,contenido = pregunta[1],idRespuesta = i):
                    self.moverInformacionModificaciónRespuesta(idPreg,usuarioid,contenido,idRespuesta,obj)
                item.bind(on_release=open_responses)

                lista_respuestas.add_widget(item)
        cacheRespuesta.idsRespuestas.clear()
        
    def moverInformacionModificaciónRespuesta(self,idPreg,usuarioid,contenido,idRespuesta,obj):
        self.root.ids.text_field_resp_Mod.text = str(contenido)
        print("Llega a aqui")
        cacheRespuesta.idRespuestaModificar = idRespuesta
        cacheRespuesta.idPreguntaModificarResp = idPreg
        self.dialog = MDDialog(
            title = 'Acciones',
                text = f"Elija que actividad desea realizar",
                buttons = [
                MDFlatButton(
                    text = "Modificar", text_color = self.theme_cls.accent_color,
                    on_release = self.close_dialog
                ),
                MDFlatButton(
                    text = "Eliminar", text_color = self.theme_cls.accent_color,
                    on_release = self.seleccionEliminacionRespuesta
                ),
                MDFlatButton(
                    text = "Cancelar", text_color = self.theme_cls.accent_color,
                    on_release = self.close_dialog
                ),
            ],
        )
        self.dialog.open()
        # self.abrirRespuestasComunidadPersonales()
    
    def seleccionEliminacionRespuesta(self,obj):
        self.dialog.dismiss()
        mensaje = respuestaDOM.eliminarRespuestaSeleccionada(cacheRespuesta.idRespuestaModificar)
        if mensaje == True:
            self.root.ids.text_field_resp_Mod.text = ""
            self.dialog = MDDialog(
                title = 'Modificación exitosa',
                text = f"Se ha eliminado el registro de su respuesta correctamente",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
        self.root.current_heroes = ["hero"]
        self.root.current = "screen B"

    def modificarRespuesta(self):
        if self.root.ids.text_field_resp_Mod.text != "":
            print("Modificacion")
            mensaje = respuestaDOM.modificarRespuestaSeleccionada(self.root.ids.text_field_resp_Mod.text,cacheRespuesta.idRespuestaModificar)
            if mensaje == True:
                self.root.ids.text_field_resp_Mod.text = ""
                self.dialog = MDDialog(
                    title = 'Modificación exitosa',
                    text = f"Se ha modificado el registro de su respuesta correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                self.root.current_heroes = ["hero"]
                self.root.current = "screen B"
            else:
                self.dialog = MDDialog(
                    title = 'Error',
                    text = f"Se ha producido un error al modificar su respuesta, intente nuevamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()

    def registrarRespuesta(self):
        print("respuesta")
        if self.root.ids.text_field_resp.text != "":
            respuestaDOM.obtenerSiguienteIdRespuesta()
            mensaje = respuestaDOM.insertarNuevaRespuesta(cacheRespuesta.idRespuestaNueva,self.root.ids.text_field_resp.text,cacheRespuesta.idUsuarioRespuestaNueva,cacheRespuesta.idPreguntaRespuestaNueva)
            if mensaje == True:
                self.root.ids.text_field_resp.text = ""
                self.dialog = MDDialog(
                    title = 'Registro exitoso',
                    text = f"Se ha registrado correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
            else:
                self.dialog = MDDialog(
                    title = 'Error',
                    text = f"Se ha producido un error al registrar su respuesta, intente nuevamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()    
        
    def agregarBotonGestionUsuarios(self):
        interfazAccionesUsuario = self.root.ids.interfazUsuarioAcciones
        interfazAccionesUsuario.clear_widgets()
        labelTitleInfo = MDLabel(text = "Mi espacio", halign = "center", font_style = "H5",theme_text_color= "Custom",
                    text_color= "#110d4e", pos_hint = {"center_x": .5, "center_y": .9})
        interfazAccionesUsuario.add_widget(labelTitleInfo)
        print(cacheUsuario.tipoUsuario)
        if cacheUsuario.tipoUsuario == "3":

            #BOTON DE PREGUNTAS ----------------------
            botonPreguntasMenuPrincipal = MDFillRoundFlatIconButton(text = "Preguntas", icon = "frequently-asked-questions",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .75})
            # FUNCIÓN QUE CORRRESPONDE A PREGUNTAS
            def open_PreguntasPersonalesFunc(obj):
                self.abrirPreguntasPersonalesMenuPrincipal(obj)
            #Añadir al botón
            botonPreguntasMenuPrincipal.bind(on_release = open_PreguntasPersonalesFunc)
            interfazAccionesUsuario.add_widget(botonPreguntasMenuPrincipal)
                
            #BOTON DE RESPUESTAS ---------------------
            botonRespuestasMenuPrincipal = MDFillRoundFlatIconButton(text = "Respuestas",icon = "forum",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .60} )
            # FUNCIÓN QUE CORRESPONDE A RESPUESTAS
            def open_RespuestasPersonalesFunc(obj):
                self.abrirRespuestasPersonalesMenuPrincipal(obj)
            #Añadir al botón
            botonRespuestasMenuPrincipal.bind(on_release = open_RespuestasPersonalesFunc)
            interfazAccionesUsuario.add_widget(botonRespuestasMenuPrincipal)

            #BOTON DE USUARIOS -----------
            botonIngresarGestionUsuarios = MDFillRoundFlatIconButton(text = "Usuarios", icon = "account-group-outline",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .45} )
            def open_responses(obj):
                self.abrirInterfazGestionUsuarios(obj)
            botonIngresarGestionUsuarios.bind(on_release=open_responses)
            interfazAccionesUsuario.add_widget(botonIngresarGestionUsuarios)

            #BOTON DE BASE DE DATOS ------------
            botonRespaldoRestauracion = MDFillRoundFlatIconButton(text = "Base de datos", icon = "database-cog",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .30} )
            def open_respRestBD(obj):
                self.abrirInterfazBaseDeDatosRR(obj)
            botonRespaldoRestauracion.bind(on_release=open_respRestBD)
            interfazAccionesUsuario.add_widget(botonRespaldoRestauracion)

            #BOTON DE REPORTES ------------------
            botonReportesPDF = MDFillRoundFlatIconButton(text = "Reportes", icon = "file-pdf-box",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .15} )
            def open_respRestBD(obj):
                self.abrirInterfazReportesBotones(obj)
            botonReportesPDF.bind(on_release=open_respRestBD)
            interfazAccionesUsuario.add_widget(botonReportesPDF)

        else:
            if cacheUsuario.tipoUsuario == "2":
                #BOTON DE PREGUNTAS ----------------------
                botonPreguntasMenuPrincipal = MDFillRoundFlatIconButton(text = "Preguntas", icon = "frequently-asked-questions",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .75})
                # FUNCIÓN QUE CORRRESPONDE A PREGUNTAS
                def open_PreguntasPersonalesFunc(obj):
                    self.abrirPreguntasPersonalesMenuPrincipal(obj)
                #Añadir al botón
                botonPreguntasMenuPrincipal.bind(on_release = open_PreguntasPersonalesFunc)
                interfazAccionesUsuario.add_widget(botonPreguntasMenuPrincipal)
                
                #BOTON DE RESPUESTAS ---------------------
                botonRespuestasMenuPrincipal = MDFillRoundFlatIconButton(text = "Respuestas",icon = "forum",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .60} )
                # FUNCIÓN QUE CORRESPONDE A RESPUESTAS
                def open_RespuestasPersonalesFunc(obj):
                    self.abrirRespuestasPersonalesMenuPrincipal(obj)
                #Añadir al botón
                botonRespuestasMenuPrincipal.bind(on_release = open_RespuestasPersonalesFunc)
                interfazAccionesUsuario.add_widget(botonRespuestasMenuPrincipal)

                #BOTON DE TRATAMIENTOS ----------------------
                botonIngresarGestionTratamiento = MDFillRoundFlatIconButton(text = "Tratamientos", icon = "needle",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .45} )
                # FUNCION QUE CORRESPONDE A TRATAMIENTOS
                def open_Tratamientos(obj):
                    self.abrirInterfazTratamientosCon(obj)
                # AÑADIR FUNCION AL BOTON
                botonIngresarGestionTratamiento.bind(on_release = open_Tratamientos)
                interfazAccionesUsuario.add_widget(botonIngresarGestionTratamiento)

            else:
                if cacheUsuario.tipoUsuario == "1":

                    #BOTON DE PREGUNTAS ----------------------
                    botonPreguntasMenuPrincipal = MDFillRoundFlatIconButton(text = "Preguntas", icon = "frequently-asked-questions",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .75})
                    # FUNCIÓN QUE CORRRESPONDE A PREGUNTAS
                    def open_PreguntasPersonalesFunc(obj):
                        self.abrirPreguntasPersonalesMenuPrincipal(obj)
                    #Añadir al botón
                    botonPreguntasMenuPrincipal.bind(on_release = open_PreguntasPersonalesFunc)
                    interfazAccionesUsuario.add_widget(botonPreguntasMenuPrincipal)
                    
                    #BOTON DE RESPUESTAS ---------------------
                    botonRespuestasMenuPrincipal = MDFillRoundFlatIconButton(text = "Respuestas",icon = "forum",md_bg_color = "#383EF1", pos_hint={"center_x": .5, "center_y": .60} )
                    # FUNCIÓN QUE CORRESPONDE A RESPUESTAS
                    def open_RespuestasPersonalesFunc(obj):
                        self.abrirRespuestasPersonalesMenuPrincipal(obj)
                    #Añadir al botón
                    botonRespuestasMenuPrincipal.bind(on_release = open_RespuestasPersonalesFunc)
                    interfazAccionesUsuario.add_widget(botonRespuestasMenuPrincipal)


    # Funciones de interfaz de menu principal de acciones
    def abrirPreguntasPersonalesMenuPrincipal(self,obj):
        print("Interfaz de preguntas personales")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen PrP"
        self.menu_preguntas()

    def abrirRespuestasPersonalesMenuPrincipal(self,obj):
        print("Interfaz de respuestas personales")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen PrPRes11"
        self.abrirPreguntasRespondidasPersonales()

    def abrirInterfazGestionUsuarios(self,obj):
        print("Interfaz de gestión de usuarios")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen UsuarioConsulta"
        self.mostrarUsuariosInterfazGestion()

    def abrirInterfazBaseDeDatosRR(self,obj):
        print("Ingreso a recuperación y restauración de base de datos")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen RR DB"
    
    def abrirInterfazTratamientosCon(self,obj):
        print("Interfaz de tratamientos")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen TratamientosConsulta"
        self.interfazTratamientosUsuarios()

    def abrirInterfazReportesBotones(self,obj):
        print("Reportes")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen ReportesBotones"


    def abrirInterfazModificacionUsuarios(self,esc,idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono):
        print("Interfaz de gestión de usuarios (Modificaciones y eliminaciones)")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen UDAdminUsers"
        print("IdUsuario= ",idUsuario)
        cacheUsuario.idUsuarioModificar = idUsuario
        self.root.ids.nombreUsuario_reg_Admin_UD.text = str(usuario)
        self.root.ids.password_reg_Admin_UD.text = str(contraseña)
        self.root.ids.correo_reg_Admin_UD.text = str(correo)
        self.root.ids.nombre_reg_Admin_UD.text = str(nombre)
        self.root.ids.apellido_reg_Admin_UD.text = str(apellido)
        if tipoUsuario == "2":
            self.root.ids.checkGdAcademico_Admin_UD.active = True
            print(grado)
            self.root.ids.grado_reg_Admin_UD.text = str(grado)
            self.root.ids.telefono_reg_Admin_UD.text = str(telefono)
        else:
            if tipoUsuario == "1":
                self.root.ids.checkGdAcademico_Admin_UD.active = False


    def mostrarUsuariosInterfazGestion(self):
        print("Mostrar Usuarios")
        listaUsuarios = self.root.ids.lista_Usuarios_Consulta
        listaUsuarios.clear_widgets()
        usuarioDOM.obtenerTotalDeUsuarios()
        usuarioDOM.obtenerIdsUsuarios()
        if cacheUsuario.totalUsuarios == "0" or cacheUsuario.totalUsuarios == "" or cacheUsuario.totalUsuarios == 0 or cacheUsuario.totalUsuarios == None:
            print("Sin existencia de usuarios")
        else:
            for i in cacheUsuario.idsUsuario:
                usuario = usuarioDOM.obtenerInformacionUsuario(i)
                nuevoElementoListaUsuario = ThreeLineIconListItem(text = ("ID: "+ str(usuario[0])),secondary_text = usuario[4],tertiary_text = usuario[3])
                iconoLista = IconLeftWidget(icon = "account")
                nuevoElementoListaUsuario.add_widget(iconoLista)
                cacheUsuario.idUsuarioModificar = i
                def open_responses(esc ="esc",idUsuario = cacheUsuario.idUsuarioModificar,nombre = usuario[1],apellido = usuario[2],correo = usuario[3],usuario = usuario[4],contraseña = usuario[5],tipoUsuario = usuario[6],grado = usuario[7],telefono = usuario[8]):
                    self.abrirInterfazModificacionUsuarios(esc,idUsuario,nombre,apellido,correo,usuario,contraseña,tipoUsuario,grado,telefono)
                nuevoElementoListaUsuario.bind(on_release=open_responses)
                listaUsuarios.add_widget(nuevoElementoListaUsuario)
            cacheUsuario.idsUsuario.clear()

    def limpiarUsuarios(self):
        listaUsuarios = self.root.ids.lista_Usuarios_Consulta
        listaUsuarios.clear_widgets()
        cacheUsuario.idsUsuario.clear()
    
    # Registro de usuarios desde la interfaz del administrador
    def registrarUsuarioNuevoDesdeAdministrador(self):
        #Comprueba si el check box está activo (Si está activo es experto o de otra de manera es común)
        if(self.root.ids.checkGdAcademico_Admin.active == True):
            experto = 2 #Experto
        else:
            experto = 1 #Común
        usuarioDOM.obtenerNuevaIdUsuario()
        print(cacheUsuario.idNuevoUsuario)
        try:
            if(self.root.ids.nombre_reg_Admin.text == "" or  self.root.ids.apellido_reg_Admin.text == "" or self.root.ids.correo_reg_Admin.text == "" or self.root.ids.nombreUsuario_reg_Admin.text == "" or self.root.ids.password_reg_Admin.text == ""):
                self.dialog = MDDialog(
                    title = 'Aviso',
                    text = f"Registre su información correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;
            
            valor = usuarioDOM.existeUsuario(self.root.ids.correo_reg_Admin.text,self.root.ids.password_reg_Admin.text)
            if valor == True:
                self.dialog = MDDialog(
                    title = 'Error de registro',
                    text = f"El usuario que ha intentado registrar ya se encuentra en uso",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;

            mensaje = usuarioDOM.insertarNuevoUsuario(cacheUsuario.idNuevoUsuario,self.root.ids.nombre_reg_Admin.text,self.root.ids.apellido_reg_Admin.text,self.root.ids.correo_reg_Admin.text,self.root.ids.nombreUsuario_reg_Admin.text,self.root.ids.password_reg_Admin.text,experto,self.root.ids.grado_reg_Admin.text,self.root.ids.telefono_reg_Admin.text)
            if mensaje == True:
                self.dialog = MDDialog(
                title = 'Registro exitoso',
                text = f"Se ha registrado correctamente",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            cacheUsuario.idNuevoUsuario = ""
        except:
            self.dialog = MDDialog(
                title = 'Error al registrar',
                text = f"Ha ocurrido un error al intentar registrarse",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
    
    def eliminarUsuarioDesdeAdministrador(self):
        mensaje = usuarioDOM.eliminarUsuarioSeleccionado(cacheUsuario.idUsuarioModificar)
        if mensaje == True:
            self.dialog = MDDialog(
                title = 'Eliminación exitosa',
                text = f"El usuario se ha eliminado correctamente",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            self.root.current_heroes = ["hero"]
            self.root.current = "screen B"
        else:
            self.dialog = MDDialog(
                title = 'Error al intentar eliminar',
                text = f"No se ha podido eliminar el usuario",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()

    def modificacionUsuarioDesdeAdministrador(self):
        if(self.root.ids.checkGdAcademico_Admin_UD.active == True):
            experto = 2
        else:
            experto = 1
        try:
            
            if(self.root.ids.nombre_reg_Admin_UD.text == "" or  self.root.ids.apellido_reg_Admin_UD.text == "" or self.root.ids.correo_reg_Admin_UD.text == "" or self.root.ids.nombreUsuario_reg_Admin_UD.text == "" or self.root.ids.password_reg_Admin_UD.text == ""):
                self.dialog = MDDialog(
                    title = 'Aviso',
                    text = f"Llene la información del usuario correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;

            mensaje = usuarioDOM.modificarUsuarioSeleccionado(cacheUsuario.idUsuarioModificar,self.root.ids.nombre_reg_Admin_UD.text,self.root.ids.apellido_reg_Admin_UD.text,self.root.ids.correo_reg_Admin_UD.text,self.root.ids.nombreUsuario_reg_Admin_UD.text,self.root.ids.password_reg_Admin_UD.text,experto,self.root.ids.grado_reg_Admin_UD.text,self.root.ids.telefono_reg_Admin_UD.text)
            if mensaje == True:
                self.dialog = MDDialog(
                title = 'Modifcación exitosa',
                text = f"Se ha modificado correctamente",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            cacheUsuario.idNuevoUsuario = ""
            self.root.current_heroes = ["hero"]
            self.root.current = "screen B"
        except:
            self.dialog = MDDialog(
                title = 'Error al modificar',
                text = f"Ha ocurrido un error al intentar modificar registro",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()

    # RESTAURACION
    def restaurarBaseDeDatos(self):
        print("Restauración de base de datos")
        try:
            confirmacion = baseDeDatosDOM.restauracionBD()
            if confirmacion == True:
                self.dialog = MDDialog(
                    title = 'Restauración de base de datos exitosa',
                    text = f"La base de datos se ha restaurado a su nueva versión de forma exitosa, el sistema se va a reiniciar",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_System_Rest
                        ),
                    ],
                )
                self.dialog.open()
        except OSError as e:
            self.dialog = MDDialog(
                title = 'Error al realizar respaldo de base de datos',
                text = f"Error del sistema al intentar restaurar la base de datos",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
            print("Error:",e.strerror)
        
    # RESPALDO
    def respaldoBaseDeDatos(self):
        print("Respaldo de base de datos")
        # try:
        confirmacion = baseDeDatosDOM.respaldoBD()
        if confirmacion == True:
            self.dialog = MDDialog(
                title = 'Respaldo de base de datos exitoso',
                text = f"Se ha respaldado la base de datos de forma correcta",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()
        # except:
        #     self.dialog = MDDialog(
        #         title = 'Error al realizar respaldo de base de datos',
        #         text = f"Error del sistema al intentar respaldar la base de datos",
        #         buttons = [
        #             MDFlatButton(
        #                 text = "OK", text_color = self.theme_cls.accent_color,
        #                 on_release = self.close_dialog
        #             ),
        #         ],
        #     )
        #     self.dialog.open()
        
    def buscarImagenTratamiento(self):
        # Crea una ventana raíz de tkinter (no se mostrará en la pantalla)
        root = tk.Tk()
        root.withdraw()

        # Muestra el cuadro de diálogo para seleccionar un archivo y filtra por archivos de imagen JPEG o JPG
        file_path = filedialog.askopenfilename(filetypes=[("JPEG", "*.jpg"), ("JPEG", "*.jpeg")])

        # Imprime la ruta del archivo seleccionado
        print("La imagen seleccionada es:", file_path)

        cacheTratamiento.filepathImagenRegistro = file_path
    
    #Función de registro de tratamiento en interfaz 
    def registrarNuevoTratamiento(self):
        print("Nuevo tratamiento en registro")
        siguienteIDPreg = tratamientoDOM.obtenerSiguienteIdTratamiento() #Obtención de id disponible en la tabla de base de datos de Tratamiento
        if (siguienteIDPreg[0] == "null" or siguienteIDPreg[0] == None or siguienteIDPreg[0] == "" or siguienteIDPreg[0] == "0" or siguienteIDPreg == None): 
            siguienteIDRegTrat = 1 #La id obtenida es 1
        else:
            siguienteIDRegTrat = siguienteIDPreg[0] #La id obtenida es diferente de 1 y 0
        print("My file",cacheTratamiento.filepathImagenRegistro)
        if self.root.ids.enfermedad_tratamiento_text.text != "" and self.root.ids.fungicida_tratamiento_text.text != "" and cacheTratamiento.filepathImagenRegistro != "":
            print("Primera base",cacheUsuario.idUsuario)
            with open(cacheTratamiento.filepathImagenRegistro, "rb") as f: #Se carga la imagen del tratamiento especificada
                imagen_bytes = f.read()
            mensaje = tratamientoDOM.insertarNuevoTratamiento(int(siguienteIDRegTrat),self.root.ids.enfermedad_tratamiento_text.text,self.root.ids.fungicida_tratamiento_text.text,self.root.ids.marca_tratamiento_text.text,self.root.ids.instrucciones_tratamiento_text.text,self.root.ids.precauciones_tratamiento_text.text,imagen_bytes,cacheUsuario.idUsuario)
            if mensaje == True: #La inserción se realizo correctamente
                print("regreso")
                self.dialog = MDDialog(
                    title = 'Registro exitoso',
                    text = f"Se ha registrado correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                self.root.ids.enfermedad_tratamiento_text.text = ""
                self.root.ids.fungicida_tratamiento_text.text = ""
                self.root.ids.marca_tratamiento_text.text = ""
                self.root.ids.instrucciones_tratamiento_text.text = ""
                self.root.ids.precauciones_tratamiento_text.text = ""
    
    #Función de consulta de la información de tratamientos
    def interfazTratamientosUsuarios(self):
        cachePregunta.confirmacionBorrado = False
        total = tratamientoDOM.obtenerTotalTratamientos() #Se obtiene el numero total de tratamientos existentes
        box_layout = self.root.ids.gridTratamientosConsulta
        box_layout.clear_widgets()
        print("Total de tratamientos registrados al momento: ", total[0])
        if(total[0] == 0 or total[0] == "" or total == "0" or total[0] == None):
            print("No tratamientos")
        else:   
            tratamientoDOM.obtenerIdsTratamientos() #Se obtienen las ids de tratamientos de la información
            print(cacheTratamiento.idsTratamientos[0], "")
            for i in cacheTratamiento.idsTratamientos:
                pregunta = tratamientoDOM.obtenerTratamiento(i) #Se obtiene la información del tratamiento
                # Generar un nombre de archivo único para la imagen
                image_file = str(uuid.uuid4()) + ".jpg"
                cacheTratamiento.archivosDeTratamiento.append(image_file)
                # Guardar la imagen en disco con el nombre de archivo único
                with open(image_file, "wb") as f:
                    f.write(pregunta[3])
                nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[4])
                tile = MDSmartTile(source=image_file, radius=20, box_radius=[0, 0, 24, 24], lines=2, size=("120dp", "120dp")) #Se muestra la imagen del tratamiento
                def open_responses(obj, pregunta_0=i,usuario = pregunta[4]):
                    self.abrirInterfazTratamientosModificacionEliminacion(pregunta_0,usuario, obj)
                tile.bind(on_release=open_responses)
                descr = ThreeLineListItem(text=pregunta[1], secondary_text=pregunta[2], tertiary_text=nombreUsuario, font_style= "H6", theme_text_color= "Custom", text_color = "#FFFFFF", secondary_theme_text_color = "Custom" , secondary_text_color = "#FFFFFF",tertiary_theme_text_color = "Custom",tertiary_text_color = "#FFFFFF") #Se muestra la información en texto del tratamiento
                tile.add_widget(descr) #Añadir elementos a la interfaz
                box_layout.add_widget(tile)
            self.dialog = MDDialog(
                title = 'Aviso',
                text = f"Bienvenidos a la sección de tratamientos!",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.eliminarArchivosTratamientoConfirmado
                    ),
                ],
            )
            self.dialog.open()
            cacheTratamiento.idsTratamientos.clear()

    def eliminarArchivosTratamientoConfirmado(self,obj):
        self.dialog.dismiss()
        self.eliminarArchivosTratamiento()
        
    
    def abrirInterfazTratamientosModificacionEliminacion(self,pregunta_0,usuario,obj):
        print("Interfaz de tratamientos en modificación y eliminación")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen RegTratamiento_mod"
        self.interfazTratamientosUsuariosModificacionEliminacion(pregunta_0,usuario)
    
    def interfazTratamientosUsuariosModificacionEliminacion(self,pregunta_0,usuario):
        print("Interfaz modificacion  y eliminación")
        infoTratamientoMod = tratamientoDOM.obtenerTratamientoCompleto(pregunta_0)
        cacheTratamiento.idTratamientoModificar = pregunta_0
        self.root.ids.enfermedad_tratamiento_text_modf.text = str(infoTratamientoMod[1])
        self.root.ids.fungicida_tratamiento_text_modf.text = str(infoTratamientoMod[2])
        self.root.ids.marca_tratamiento_text_modf.text = str(infoTratamientoMod[3])
        self.root.ids.instrucciones_tratamiento_text_modf.text = str(infoTratamientoMod[4])
        self.root.ids.precauciones_tratamiento_text_modf.text = str(infoTratamientoMod[5])
        image_file = str(uuid.uuid4()) + ".jpg"
        with open(image_file, "wb") as f:
            f.write(infoTratamientoMod[6])
        cacheTratamiento.filepathImagenRegistro = image_file
    
    #Función de modificación de la información de un tratamiento
    def modificarTratamientoSeleccionado(self):
        if self.root.ids.enfermedad_tratamiento_text_modf.text != "" and self.root.ids.fungicida_tratamiento_text_modf.text != "" and self.root.ids.marca_tratamiento_text_modf.text != "" and self.root.ids.instrucciones_tratamiento_text_modf.text != "" and self.root.ids.precauciones_tratamiento_text_modf.text != "" and cacheTratamiento.filepathImagenRegistro != "":
            print("Segunda fase",cacheUsuario.idUsuario)
            with open(cacheTratamiento.filepathImagenRegistro, "rb") as f:
                imagen_bytes = f.read() #Creación de imagen temporal
            mensaje = tratamientoDOM.modificarTratamientoSeleccionada(cacheTratamiento.idTratamientoModificar,self.root.ids.enfermedad_tratamiento_text_modf.text,self.root.ids.fungicida_tratamiento_text_modf.text,self.root.ids.marca_tratamiento_text_modf.text, self.root.ids.instrucciones_tratamiento_text_modf.text, self.root.ids.precauciones_tratamiento_text_modf.text,imagen_bytes,cacheUsuario.idUsuario)
            if mensaje == True:
                print("Modificación realizada")
                self.dialog = MDDialog(
                    title = 'Aviso de acción',
                    text = f"Se ha realizado la modificación correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
            os.remove(cacheTratamiento.filepathImagenRegistro)

    def eliminarTratamientoSeleccionado(self):
        print("Eliminar Tratamiento seleccionada")
        self.dialog = MDDialog(
            title = 'Advertencia',
            text = f"Desea eliminar el tratamiento?",
            buttons = [
                MDFlatButton(
                    text = "Eliminar", text_color = self.theme_cls.accent_color,
                    on_release = self.eliminarTratamientoConfirmado
                ),
                MDFlatButton(
                    text = "Cancelar", text_color = self.theme_cls.accent_color,
                    on_release = self.close_dialog
                ),
            ],
        )
        self.dialog.open()

    #Función de eliminación de tratamiento
    def eliminarTratamientoConfirmado(self,obj):
        self.dialog.dismiss()
        mensaje = tratamientoDOM.eliminarTratamientoSeleccionado(cacheTratamiento.idTratamientoModificar) #Se envia el id del tratamiento seleccionado al eliminar
        if mensaje == True: #Al realizar la eliminación de forma correcta se envia un mensaje
            self.dialog = MDDialog(
                    title = 'Aviso de acción',
                    text = f"Se ha realizado la eliminación correctamente",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        os.remove(cacheTratamiento.filepathImagenRegistro)
        self.root.current_heroes = ["hero"]
        self.root.current = "screen B" #Se envia al usuario al menú
    
    #Rellena la información del usuario que está utilizando el sistema en el perfil de forma automatica
    def rellenarInformacionPerfil(self):
        print("Información de perfil")
        self.root.ids.nombreUsuario_perfil.text = str(cacheUsuario.usuario)
        self.root.ids.correoUsuario_perfil.text = str(cacheUsuario.correo)
        self.root.ids.contraUsuario_perfil.text = str(cacheUsuario.contra)
        self.root.ids.nombrePersonalUsuario_perfil.text = str(cacheUsuario.nombre)
        self.root.ids.apellidoUsuario_perfil.text = str(cacheUsuario.apellido)
        self.root.ids.gradoActPerfil.text = str(cacheUsuario.grado)
        self.root.ids.telefonoPerfil.text = str(cacheUsuario.telefono)
        if(cacheUsuario.tipoUsuario == "2"):
            self.root.ids.checkGdAcademicoPerfil.active = True

    def actualizarInformacionPerfilUsuario(self):
        if(self.root.ids.checkGdAcademicoPerfil.active == True):
            experto = 2
        else:
            experto = 1
        try:
            if(self.root.ids.nombrePersonalUsuario_perfil.text == "" or  self.root.ids.apellidoUsuario_perfil.text == "" or self.root.ids.correoUsuario_perfil.text == "" or self.root.ids.nombreUsuario_perfil.text == "" or self.root.ids.contraUsuario_perfil.text == ""):
                self.dialog = MDDialog(
                    title = 'Aviso',
                    text = f"Llena la información de tu perfil de forma correcta",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                return;

            mensaje = usuarioDOM.modificarUsuarioSeleccionado(cacheUsuario.idUsuario,self.root.ids.nombrePersonalUsuario_perfil.text,self.root.ids.apellidoUsuario_perfil.text,self.root.ids.correoUsuario_perfil.text,self.root.ids.nombreUsuario_perfil.text,self.root.ids.contraUsuario_perfil.text,experto,self.root.ids.gradoActPerfil.text,self.root.ids.telefonoPerfil.text)
            if mensaje == True:
                self.dialog = MDDialog(
                    title = 'Actualización exitosa',
                    text = f"Se ha modificado tu información correctamente!",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
                cacheUsuario.usuario = self.root.ids.nombreUsuario_perfil.text
                cacheUsuario.nombre = self.root.ids.nombrePersonalUsuario_perfil.text
                cacheUsuario.apellido = self.root.ids.apellidoUsuario_perfil.text
                cacheUsuario.correo = self.root.ids.correoUsuario_perfil.text
                cacheUsuario.contra = self.root.ids.contraUsuario_perfil.text
                cacheUsuario.grado = self.root.ids.gradoActPerfil.text
                cacheUsuario.telefono = self.root.ids.telefonoPerfil.text
        except:
            self.dialog = MDDialog(
                title = 'Error',
                text = f"Ha ocurrido un error al intentar actualizar tu información :(",
                buttons = [
                    MDFlatButton(
                        text = "OK", text_color = self.theme_cls.accent_color,
                        on_release = self.close_dialog
                    ),
                ],
            )
            self.dialog.open()

    def capturarImagenReconocimientoNueva(self):
        camera = self.root.ids.camera
        camera.export_to_png('captured_image.png')
        cacheReconocimiento.imagenReconocimientoReg = "captured_image.png"
        self.root.current_heroes = ["hero"]
        self.root.current = "screen B"
    
    def on_start(self):
        self.root.ids.camera.play = True

    def on_stop(self):
        self.root.ids.camera.play = False


    def buscarImagenReconocimiento(self):
        # Crea una ventana raíz de tkinter (no se mostrará en la pantalla)
        root = tk.Tk()
        root.withdraw()

        # Muestra el cuadro de diálogo para seleccionar un archivo y filtra por archivos de imagen JPEG o JPG
        file_path = filedialog.askopenfilename(filetypes=[("JPEG", "*.jpg"), ("JPEG", "*.jpeg")])

        # Imprime la ruta del archivo seleccionado
        print("La imagen seleccionada es:", file_path)

        cacheReconocimiento.imagenReconocimientoReg = file_path

    def rellenarInformacionReconocimientoResultados(self):
        print("Información de reconocimiento")
        if(cacheReconocimiento.imagenReconocimientoReg == ""):
            print("Validaciones")
        else:

            idDiagnostico = ""
            idDiagnostico = diagnosticoDOM.obtenerSiguienteIdDiagnostico()
            if idDiagnostico[0] == "" or idDiagnostico[0] == "null" or idDiagnostico[0] == "0" or idDiagnostico[0] == 0 or idDiagnostico[0] == None:
                finalId = 1
            else:
                finalId = idDiagnostico[0]
            with open(cacheReconocimiento.imagenReconocimientoReg, "rb") as f:
                imagen_bytes = f.read()

            self.root.ids.imagenSeleccionadaReconocimiento.source = str(cacheReconocimiento.imagenReconocimientoReg)
            resultado = EscaneoDOM.RealizarEscaneo(cacheReconocimiento.imagenReconocimientoReg)

            mensajebdConfirmacion = diagnosticoDOM.insertarNuevoDiagnostico(finalId,imagen_bytes,resultado,cacheUsuario.idUsuario)

            self.root.ids.resultadoTextoImagenReconocimiento.text = "[color=#ffffff][b]" + resultado + "[/b][/color]"
            # TRATAMIENTOS RECOMENDADOS
            # cachePregunta.confirmacionBorrado = False
            total = tratamientoDOM.obtenerTotalTratamientosReconocimiento(resultado)
            box_layout = self.root.ids.gridTratamientosConsultaRecomendados
            box_layout.clear_widgets()
            print("Total de tratamientos registrados al momento: ", total[0])
            if(total[0] == 0 or total[0] == "" or total == "0" or total[0] == None):
                print("No tratamientos")
            else:   
                tratamientoDOM.obtenerIdsTratamientosReconocimiento(resultado)
                print(cacheTratamiento.idsTratamientos[0], "")
                for i in cacheTratamiento.idsTratamientos:
                    pregunta = tratamientoDOM.obtenerTratamiento(i)
                    # Generar un nombre de archivo único para la imagen
                    image_file = str(uuid.uuid4()) + ".jpg"
                    cacheTratamiento.archivosDeTratamiento.append(image_file)
                    # Guardar la imagen en disco con el nombre de archivo único
                    with open(image_file, "wb") as f:
                        f.write(pregunta[3])
                    nombreUsuario = usuarioDOM.obtenerNombreUsuario(pregunta[4])
                    tile = MDSmartTile(source=image_file, radius=20, box_radius=[0, 0, 24, 24], lines=2, size=("120dp", "120dp"))
                    def open_responses(obj, pregunta_0=i,usuario = pregunta[4]):
                        self.abrirInterfazTratamientoSeleccionadoReconocimiento(pregunta_0,usuario, obj)
                    tile.bind(on_release=open_responses)
                    descr = ThreeLineListItem(text=pregunta[1], secondary_text=pregunta[2], tertiary_text=nombreUsuario, font_style= "H6", theme_text_color= "Custom", text_color = "#FFFFFF", secondary_theme_text_color = "Custom" , secondary_text_color = "#FFFFFF",tertiary_theme_text_color = "Custom",tertiary_text_color = "#FFFFFF")
                    tile.add_widget(descr)
                    box_layout.add_widget(tile)
                self.dialog = MDDialog(
                    title = 'Aviso',
                    text = f"Análisis finalizado!",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.eliminarArchivosTratamientoConfirmado
                        ),
                    ],
                )
                self.dialog.open()
                cacheTratamiento.idsTratamientos.clear()

    def abrirInterfazTratamientoSeleccionadoReconocimiento(self,pregunta_0,usuario,obj):
        print("Interfaz de reconocimiento para tratamiento seleccionado")
        self.root.current_heroes = ["hero"]
        self.root.current = "screen ReconocimientoTratamientoSeleccionado"
        informacionTratamiento = tratamientoDOM.obtenerTratamientoCompleto(pregunta_0)
        self.root.ids.labelTratamiento_TitleSeleccionado.text = str(informacionTratamiento[1])
        image_file = str(uuid.uuid4()) + ".jpg"
        cacheTratamiento.archivosDeTratamiento.append(image_file)
        # Guardar la imagen en disco con el nombre de archivo único
        with open(image_file, "wb") as f:
            f.write(informacionTratamiento[6])
        self.root.ids.imagenSeleccionadaReconocimiento_Tratamiento.source = str(image_file)
        self.root.ids.labelMarca_TratamientoReconocimiento.text = informacionTratamiento[3] 
        self.root.ids.labelDescripcion_TratamientoReconocimiento.text = informacionTratamiento[4] 
        self.root.ids.labelPrecaucion_TratamientoReconocimiento.text = informacionTratamiento[5]
        siguienteIDHistorial = tratamientoHistorialDOM.obtenerSiguienteIdHistorial()
        resultadoInsercion = tratamientoHistorialDOM.insertarNuevoHistorial(siguienteIDHistorial[0],cacheUsuario.idUsuario,pregunta_0)

    def opcionDidymellaReporte(self):
        self.root.ids.btnEleccionDidymellaReporteEnfermedad.md_bg_color = "#6C1902"
        self.root.ids.btnEleccionRojaReporteEnfermedad.md_bg_color = "#19076b"
        self.root.ids.btnEleccionSanaReporteEnfermedad.md_bg_color = "#19076b"
        cacheReporte.eleccionReporteTratamiento = "Didymella"

    def opcionRojaReporte(self):
        self.root.ids.btnEleccionDidymellaReporteEnfermedad.md_bg_color = "#19076b"
        self.root.ids.btnEleccionRojaReporteEnfermedad.md_bg_color = "#6C1902"
        self.root.ids.btnEleccionSanaReporteEnfermedad.md_bg_color = "#19076b"
        cacheReporte.eleccionReporteTratamiento = "Araña Roja"

    def opcionSanaReporte(self):
        self.root.ids.btnEleccionDidymellaReporteEnfermedad.md_bg_color = "#19076b"
        self.root.ids.btnEleccionRojaReporteEnfermedad.md_bg_color = "#19076b"
        self.root.ids.btnEleccionSanaReporteEnfermedad.md_bg_color = "#6C1902"
        cacheReporte.eleccionReporteTratamiento = "Planta sana"

    def generarReportePDFTratamientos(self):
       # Datos para el gráfico
        nombreDocumento = self.root.ids.textfielNombre_ReporteTratamiento.text
        self.obtenerTotalTratamientosRecomendadosPorMes()
        datos = [cacheReporte.recomendacionesEnero, cacheReporte.recomendacionesFebrero, cacheReporte.recomendacionesMarzo, cacheReporte.recomendacionesAbril, cacheReporte.recomendacionesMayo, cacheReporte.recomendacionesJunio, cacheReporte.recomendacionesJulio, cacheReporte.recomendacionesAgosto, cacheReporte.recomendacionesSeptiembre, cacheReporte.recomendacionesOctubre, cacheReporte.recomendacionesNoviembre, cacheReporte.recomendacionesDiciembre]
        nombres = ['1', '2', '3', '4', '5','6','7','8','9','10','11','12']
        nombres2 = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        # Crear el gráfico
        
        plt.bar(nombres, datos)

        # Establecer el título y las etiquetas de los ejes
        plt.title('Cantidad de Recomendaciones de tratamientos del año '+ str(datetime.datetime.now().year))
        plt.xlabel('Meses')
        plt.ylabel('Cantidad')

        # Guardar el gráfico en un archivo temporal
        plt.savefig('temp.png')

        # Crear un archivo PDF y agregar el gráfico y un título
        canvas = Canvas(nombreDocumento + ".pdf", pagesize=letter)
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawCentredString(300, 750, "Tratamientos")
        canvas.drawImage(ImageReader('temp.png'), 100, 500, width=400, height=200)
        canvas.setFont("Helvetica", 12)
        # Crear el mensaje
        mensaje = "Reporte por mes sobre tratamientos recomendados"

        # Establecer el estilo del texto
        estilo_texto = canvas.beginText()
        estilo_texto.setFont("Helvetica-Bold", 14)
        estilo_texto.setFillColorRGB(0.2, 0.2, 0.2)

        # Agregar el mensaje al lienzo PDF
        estilo_texto.setTextOrigin(145, 700)
        estilo_texto.textLine(mensaje)
        canvas.drawText(estilo_texto)

        # Crear el mensaje
        mensaje2 = "Tabla de información por mes"

        # Establecer el estilo del texto
        estilo_texto2 = canvas.beginText()
        estilo_texto2.setFont("Helvetica-Bold", 14)
        estilo_texto2.setFillColorRGB(0.2, 0.2, 0.2)

        # Agregar el mensaje al lienzo PDF
        estilo_texto2.setTextOrigin(200, 450)
        estilo_texto2.textLine(mensaje2)
        canvas.drawText(estilo_texto2)

        # Agregar la tabla
        datos_tabla = [('Mes','Cantidad'),('Enero', cacheReporte.recomendacionesEnero), ('Febrero', cacheReporte.recomendacionesFebrero), ('Marzo', cacheReporte.recomendacionesMarzo), ('Abril', cacheReporte.recomendacionesAbril), ('Mayo', cacheReporte.recomendacionesMayo), ('Junio', cacheReporte.recomendacionesJunio), ('Julio', cacheReporte.recomendacionesJulio), ('Agosto', cacheReporte.recomendacionesAgosto), ('Septiembre', cacheReporte.recomendacionesSeptiembre), ('Octubre', cacheReporte.recomendacionesOctubre), ('Noviembre', cacheReporte.recomendacionesNoviembre), ('Diciembre', cacheReporte.recomendacionesDiciembre)]
        ancho_columnas = [300, 200]
        tabla = Table(datos_tabla, ancho_columnas)

        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ])
        
        tabla.setStyle(estilo_tabla)
        # Agregar la tabla al documento
        # canvas.drawCentredString(150, 100, "Tabla de meses y cantidades")
        tabla.wrapOn(canvas, 0, 0)
        tabla.drawOn(canvas, 50, 100)


        # Agregar un espacio en blanco
        canvas.drawString(100, 600, "")
        canvas.showPage()
        
        # Guardar el archivo PDF y limpiar la memoria
        canvas.save()
        plt.clf()

    def obtenerTotalTratamientosRecomendadosPorMes(self):
        tratamientoHistorialDOM.obtenerRecomendacionesEnero()
        tratamientoHistorialDOM.obtenerRecomendacionesFebrero()
        tratamientoHistorialDOM.obtenerRecomendacionesMarzo()
        tratamientoHistorialDOM.obtenerRecomendacionesAbril()
        tratamientoHistorialDOM.obtenerRecomendacionesMayo()
        tratamientoHistorialDOM.obtenerRecomendacionesJunio()
        tratamientoHistorialDOM.obtenerRecomendacionesJulio()
        tratamientoHistorialDOM.obtenerRecomendacionesAgosto()
        tratamientoHistorialDOM.obtenerRecomendacionesSeptiembre()
        tratamientoHistorialDOM.obtenerRecomendacionesOctubre()
        tratamientoHistorialDOM.obtenerRecomendacionesNoviembre()
        tratamientoHistorialDOM.obtenerRecomendacionesDiciembre()
        if cacheReporte.recomendacionesEnero == "" or cacheReporte.recomendacionesEnero == "null" or cacheReporte.recomendacionesEnero == None:
            cacheReporte.recomendacionesEnero = "0"
        if cacheReporte.recomendacionesFebrero == "" or cacheReporte.recomendacionesFebrero == "null" or cacheReporte.recomendacionesFebrero == None:
            cacheReporte.recomendacionesFebrero = "0"
        if cacheReporte.recomendacionesMarzo == "" or cacheReporte.recomendacionesMarzo == "null" or cacheReporte.recomendacionesMarzo == None:
            cacheReporte.recomendacionesMarzo = "0"
        if cacheReporte.recomendacionesAbril == "" or cacheReporte.recomendacionesAbril == "null" or cacheReporte.recomendacionesAbril == None:
            cacheReporte.recomendacionesAbril = "0"
        if cacheReporte.recomendacionesMayo == "" or cacheReporte.recomendacionesMayo == "null" or cacheReporte.recomendacionesMayo == None:
            cacheReporte.recomendacionesMayo = "0"
        if cacheReporte.recomendacionesJunio == "" or cacheReporte.recomendacionesJunio == "null" or cacheReporte.recomendacionesJunio == None:
            cacheReporte.recomendacionesJunio = "0"
        if cacheReporte.recomendacionesJulio == "" or cacheReporte.recomendacionesJulio == "null" or cacheReporte.recomendacionesJulio == None:
            cacheReporte.recomendacionesJulio = "0"
        if cacheReporte.recomendacionesAgosto == "" or cacheReporte.recomendacionesAgosto == "null" or cacheReporte.recomendacionesAgosto == None:
            cacheReporte.recomendacionesAgosto = "0"
        if cacheReporte.recomendacionesSeptiembre == "" or cacheReporte.recomendacionesSeptiembre == "null" or cacheReporte.recomendacionesSeptiembre == None:
            cacheReporte.recomendacionesSeptiembre = "0"
        if cacheReporte.recomendacionesOctubre == "" or cacheReporte.recomendacionesOctubre == "null" or cacheReporte.recomendacionesOctubre == None:
            cacheReporte.recomendacionesOctubre = "0"
        if cacheReporte.recomendacionesNoviembre == "" or cacheReporte.recomendacionesNoviembre == "null" or cacheReporte.recomendacionesNoviembre == None:
            cacheReporte.recomendacionesNoviembre = "0"
        if cacheReporte.recomendacionesDiciembre == "" or cacheReporte.recomendacionesDiciembre == "null" or cacheReporte.recomendacionesDiciembre == None:
            cacheReporte.recomendacionesDiciembre = "0"

    def obtenerTotalDiagnosticosPorMes(self,nombreEnfermedad):
        diagnosticoDOM.obtenerDiagnosticosEneroEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosFebreroEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosMarzoEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosAbrilEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosMayoEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosJunioEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosJulioEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosAgostoEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosSeptiembreEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosOctubreEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosNoviembreEnfermedad(nombreEnfermedad)
        diagnosticoDOM.obtenerDiagnosticosDiciembreEnfermedad(nombreEnfermedad)
        if cacheDiagnostico.cantidadDiagnosticosEnero == "" or cacheDiagnostico.cantidadDiagnosticosEnero == "null" or cacheDiagnostico.cantidadDiagnosticosEnero == None:
            cacheDiagnostico.cantidadDiagnosticosEnero = "0"
        if cacheDiagnostico.cantidadDiagnosticosFebrero == "" or cacheDiagnostico.cantidadDiagnosticosFebrero == "null" or cacheDiagnostico.cantidadDiagnosticosFebrero == None:
            cacheDiagnostico.cantidadDiagnosticosFebrero = "0"
        if cacheDiagnostico.cantidadDiagnosticosMarzo == "" or cacheDiagnostico.cantidadDiagnosticosMarzo == "null" or cacheDiagnostico.cantidadDiagnosticosMarzo == None:
            cacheDiagnostico.cantidadDiagnosticosMarzo = "0"
        if cacheDiagnostico.cantidadDiagnosticosAbril == "" or cacheDiagnostico.cantidadDiagnosticosAbril == "null" or cacheDiagnostico.cantidadDiagnosticosAbril == None:
            cacheDiagnostico.cantidadDiagnosticosAbril = "0"
        if cacheDiagnostico.cantidadDiagnosticosMayo == "" or cacheDiagnostico.cantidadDiagnosticosMayo == "null" or cacheDiagnostico.cantidadDiagnosticosMayo == None:
            cacheDiagnostico.cantidadDiagnosticosMayo = "0"
        if cacheDiagnostico.cantidadDiagnosticosJunio == "" or cacheDiagnostico.cantidadDiagnosticosJunio == "null" or cacheDiagnostico.cantidadDiagnosticosJunio == None:
            cacheDiagnostico.cantidadDiagnosticosJunio = "0"
        if cacheDiagnostico.cantidadDiagnosticosJulio == "" or cacheDiagnostico.cantidadDiagnosticosJulio == "null" or cacheDiagnostico.cantidadDiagnosticosJulio == None:
            cacheDiagnostico.cantidadDiagnosticosJulio = "0"
        if cacheDiagnostico.cantidadDiagnosticosAgosto == "" or cacheDiagnostico.cantidadDiagnosticosAgosto == "null" or cacheDiagnostico.cantidadDiagnosticosAgosto == None:
            cacheDiagnostico.cantidadDiagnosticosAgosto = "0"
        if cacheDiagnostico.cantidadDiagnosticosSeptiembre == "" or cacheDiagnostico.cantidadDiagnosticosSeptiembre == "null" or cacheDiagnostico.cantidadDiagnosticosSeptiembre == None:
            cacheDiagnostico.cantidadDiagnosticosSeptiembre = "0"
        if cacheDiagnostico.cantidadDiagnosticosOctubre == "" or cacheDiagnostico.cantidadDiagnosticosOctubre == "null" or cacheDiagnostico.cantidadDiagnosticosOctubre == None:
            cacheDiagnostico.cantidadDiagnosticosOctubre = "0"
        if cacheDiagnostico.cantidadDiagnosticosNoviembre == "" or cacheDiagnostico.cantidadDiagnosticosNoviembre == "null" or cacheDiagnostico.cantidadDiagnosticosNoviembre == None:
            cacheDiagnostico.cantidadDiagnosticosNoviembre = "0"
        if cacheDiagnostico.cantidadDiagnosticosDiciembre == "" or cacheDiagnostico.cantidadDiagnosticosDiciembre == "null" or cacheDiagnostico.cantidadDiagnosticosDiciembre == None:
            cacheDiagnostico.cantidadDiagnosticosDiciembre = "0"

    def generarReportePDFEnfermedades(self):
       # Datos para el gráfico
       if cacheReporte.eleccionReporteTratamiento == "":
           print("sin realizar la elección de reporte")
       else:
            nombreDocumento = self.root.ids.textfielNombre_ReporteEnfermedad.text
            self.obtenerTotalDiagnosticosPorMes(cacheReporte.eleccionReporteTratamiento)
            datos = [cacheDiagnostico.cantidadDiagnosticosEnero, cacheDiagnostico.cantidadDiagnosticosFebrero, cacheDiagnostico.cantidadDiagnosticosMarzo, cacheDiagnostico.cantidadDiagnosticosAbril, cacheDiagnostico.cantidadDiagnosticosMayo, cacheDiagnostico.cantidadDiagnosticosJunio, cacheDiagnostico.cantidadDiagnosticosJulio, cacheDiagnostico.cantidadDiagnosticosAgosto, cacheDiagnostico.cantidadDiagnosticosSeptiembre, cacheDiagnostico.cantidadDiagnosticosOctubre, cacheDiagnostico.cantidadDiagnosticosNoviembre, cacheDiagnostico.cantidadDiagnosticosDiciembre]
            nombres = ['1', '2', '3', '4', '5','6','7','8','9','10','11','12']
            nombres2 = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
            # Crear el gráfico
            plt.bar(nombres, datos)

            # Establecer el título y las etiquetas de los ejes
            plt.title('Cantidad de diagnosticos de '+ cacheReporte.eleccionReporteTratamiento +' del año '+ str(datetime.datetime.now().year))
            plt.xlabel('Meses')
            plt.ylabel('Cantidad')

            # Guardar el gráfico en un archivo temporal
            plt.savefig('temp.png')

            # Crear un archivo PDF y agregar el gráfico y un título
            canvas = Canvas(nombreDocumento + ".pdf", pagesize=letter)
            canvas.setFont("Helvetica-Bold", 18)
            canvas.drawCentredString(300, 750, "Enfermedad/Plaga")
            canvas.drawImage(ImageReader('temp.png'), 100, 500, width=400, height=200)
            canvas.setFont("Helvetica", 12)
            # Crear el mensaje
            mensaje = "Reporte por mes sobre diagnosticos realizados"

            # Establecer el estilo del texto
            estilo_texto = canvas.beginText()
            estilo_texto.setFont("Helvetica-Bold", 14)
            estilo_texto.setFillColorRGB(0.2, 0.2, 0.2)

            # Agregar el mensaje al lienzo PDF
            estilo_texto.setTextOrigin(145, 700)
            estilo_texto.textLine(mensaje)
            canvas.drawText(estilo_texto)

            # Crear el mensaje
            mensaje2 = "Tabla de información por mes"

            # Establecer el estilo del texto
            estilo_texto2 = canvas.beginText()
            estilo_texto2.setFont("Helvetica-Bold", 14)
            estilo_texto2.setFillColorRGB(0.2, 0.2, 0.2)

            # Agregar el mensaje al lienzo PDF
            estilo_texto2.setTextOrigin(200, 450)
            estilo_texto2.textLine(mensaje2)
            canvas.drawText(estilo_texto2)

            # Agregar la tabla
            datos_tabla = [('Mes','Cantidad'),('Enero', cacheDiagnostico.cantidadDiagnosticosEnero), ('Febrero', cacheDiagnostico.cantidadDiagnosticosFebrero), ('Marzo', cacheDiagnostico.cantidadDiagnosticosMarzo), ('Abril', cacheDiagnostico.cantidadDiagnosticosAbril), ('Mayo', cacheDiagnostico.cantidadDiagnosticosMayo), ('Junio', cacheDiagnostico.cantidadDiagnosticosJunio), ('Julio', cacheDiagnostico.cantidadDiagnosticosJulio), ('Agosto', cacheDiagnostico.cantidadDiagnosticosAgosto), ('Septiembre', cacheDiagnostico.cantidadDiagnosticosSeptiembre), ('Octubre', cacheDiagnostico.cantidadDiagnosticosOctubre), ('Noviembre', cacheDiagnostico.cantidadDiagnosticosNoviembre), ('Diciembre', cacheDiagnostico.cantidadDiagnosticosDiciembre)]
            ancho_columnas = [300, 200]
            tabla = Table(datos_tabla, ancho_columnas)

            estilo_tabla = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
                ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), 'white'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, 'black')
            ])
            
            tabla.setStyle(estilo_tabla)
            # Agregar la tabla al documento
            # canvas.drawCentredString(150, 100, "Tabla de meses y cantidades")
            tabla.wrapOn(canvas, 0, 0)
            tabla.drawOn(canvas, 50, 100)


            # Agregar un espacio en blanco
            canvas.drawString(100, 600, "")
            canvas.showPage()
            
            # Guardar el archivo PDF y limpiar la memoria
            canvas.save()
            plt.clf()
    
    def obtenerTotalRecomendacionesExperto(self,nombreUsuarioExperto):
        tratamientoHistorialDOM.obtenerRecomendacionExpertoEnero(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoFebrero(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoMarzo(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoAbril(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoMayo(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoJunio(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoJulio(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoAgosto(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoSeptiembre(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoOctubre(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoNoviembre(nombreUsuarioExperto)
        tratamientoHistorialDOM.obtenerRecomendacionExpertoDiciembre(nombreUsuarioExperto)
        if cacheReporte.recomendacionesExpertoEnero == "" or cacheReporte.recomendacionesExpertoEnero == "null" or cacheReporte.recomendacionesExpertoEnero == None:
            cacheReporte.recomendacionesExpertoEnero = "0"
        if cacheReporte.recomendacionesExpertoFebrero == "" or cacheReporte.recomendacionesExpertoFebrero == "null" or cacheReporte.recomendacionesExpertoFebrero == None:
            cacheReporte.recomendacionesExpertoFebrero = "0"
        if cacheReporte.recomendacionesExpertoMarzo == "" or cacheReporte.recomendacionesExpertoMarzo == "null" or cacheReporte.recomendacionesExpertoMarzo == None:
            cacheReporte.recomendacionesExpertoMarzo = "0"
        if cacheReporte.recomendacionesExpertoAbril == "" or cacheReporte.recomendacionesExpertoAbril == "null" or cacheReporte.recomendacionesExpertoAbril == None:
            cacheReporte.recomendacionesExpertoAbril = "0"
        if cacheReporte.recomendacionesExpertoMayo == "" or cacheReporte.recomendacionesExpertoMayo == "null" or cacheReporte.recomendacionesExpertoMayo == None:
            cacheReporte.recomendacionesExpertoMayo = "0"
        if cacheReporte.recomendacionesExpertoJunio == "" or cacheReporte.recomendacionesExpertoJunio == "null" or cacheReporte.recomendacionesExpertoJunio == None:
            cacheReporte.recomendacionesExpertoJunio = "0"
        if cacheReporte.recomendacionesExpertoJulio == "" or cacheReporte.recomendacionesExpertoJulio == "null" or cacheReporte.recomendacionesExpertoJulio == None:
            cacheReporte.recomendacionesExpertoJulio = "0"
        if cacheReporte.recomendacionesExpertoAgosto == "" or cacheReporte.recomendacionesExpertoAgosto == "null" or cacheReporte.recomendacionesExpertoAgosto == None:
            cacheReporte.recomendacionesExpertoAgosto = "0"
        if cacheReporte.recomendacionesExpertoSeptiembre == "" or cacheReporte.recomendacionesExpertoSeptiembre == "null" or cacheReporte.recomendacionesExpertoSeptiembre == None:
            cacheReporte.recomendacionesExpertoSeptiembre = "0"
        if cacheReporte.recomendacionesExpertoOctubre == "" or cacheReporte.recomendacionesExpertoOctubre == "null" or cacheReporte.recomendacionesExpertoOctubre == None:
            cacheReporte.recomendacionesExpertoOctubre = "0"
        if cacheReporte.recomendacionesExpertoNoviembre == "" or cacheReporte.recomendacionesExpertoNoviembre == "null" or cacheReporte.recomendacionesExpertoNoviembre == None:
            cacheReporte.recomendacionesExpertoNoviembre = "0"
        if cacheReporte.recomendacionesExpertoDiciembre == "" or cacheReporte.recomendacionesExpertoDiciembre == "null" or cacheReporte.recomendacionesExpertoDiciembre == None:
            cacheReporte.recomendacionesExpertoDiciembre = "0"

    def generarReportePDFExpertos(self):
       # Datos para el gráfico
       nombreUsuario = self.root.ids.textFieldExpertoNombreUsuarioReporte.text
       informacion = tratamientoHistorialDOM.comprobacionExistenciaUsuarioExperto(nombreUsuario)
       if informacion == None:
           return

       if informacion[0] == "" or informacion[0] == "0" or informacion[0] == "" or informacion[0] == "null" or informacion[0] == " ":
           print("Sin existencia del usuario")
       else:
            nombreDocumento = self.root.ids.textFieldNombreReporteExperto.text
            self.obtenerTotalRecomendacionesExperto(nombreUsuario)
            datos = [cacheReporte.recomendacionesExpertoEnero, cacheReporte.recomendacionesExpertoFebrero, cacheReporte.recomendacionesExpertoMarzo, cacheReporte.recomendacionesExpertoAbril, cacheReporte.recomendacionesExpertoMayo, cacheReporte.recomendacionesExpertoJunio, cacheReporte.recomendacionesExpertoJulio, cacheReporte.recomendacionesExpertoAgosto, cacheReporte.recomendacionesExpertoSeptiembre, cacheReporte.recomendacionesExpertoOctubre, cacheReporte.recomendacionesExpertoNoviembre, cacheReporte.recomendacionesExpertoDiciembre]
            nombres = ['1', '2', '3', '4', '5','6','7','8','9','10','11','12']
            nombres2 = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
            # Crear el gráfico
            plt.bar(nombres, datos)

            # Establecer el título y las etiquetas de los ejes
            plt.title('Cantidad de recomendaciones de '+ nombreUsuario+' del año '+ str(datetime.datetime.now().year))
            plt.xlabel('Meses')
            plt.ylabel('Cantidad')

            # Guardar el gráfico en un archivo temporal
            plt.savefig('temp.png')

            # Crear un archivo PDF y agregar el gráfico y un título
            canvas = Canvas(nombreDocumento + ".pdf", pagesize=letter)
            canvas.setFont("Helvetica-Bold", 18)
            canvas.drawCentredString(300, 750, "Recomendación de tratamientos")
            canvas.drawImage(ImageReader('temp.png'), 100, 500, width=400, height=200)
            canvas.setFont("Helvetica", 12)
            # Crear el mensaje
            mensaje = "Reporte por mes sobre recomendaciones de tratamientos por el experto"

            # Establecer el estilo del texto
            estilo_texto = canvas.beginText()
            estilo_texto.setFont("Helvetica-Bold", 14)
            estilo_texto.setFillColorRGB(0.2, 0.2, 0.2)

            # Agregar el mensaje al lienzo PDF
            estilo_texto.setTextOrigin(80, 700)
            estilo_texto.textLine(mensaje)
            canvas.drawText(estilo_texto)

            # Crear el mensaje
            mensaje2 = "Tabla de información por mes"

            # Establecer el estilo del texto
            estilo_texto2 = canvas.beginText()
            estilo_texto2.setFont("Helvetica-Bold", 14)
            estilo_texto2.setFillColorRGB(0.2, 0.2, 0.2)

            # Agregar el mensaje al lienzo PDF
            estilo_texto2.setTextOrigin(200, 450)
            estilo_texto2.textLine(mensaje2)
            canvas.drawText(estilo_texto2)

            # Agregar la tabla
            datos_tabla = [('Mes','Cantidad'),('Enero', cacheReporte.recomendacionesExpertoEnero), ('Febrero', cacheReporte.recomendacionesExpertoFebrero), ('Marzo', cacheReporte.recomendacionesExpertoMarzo), ('Abril', cacheReporte.recomendacionesExpertoAbril), ('Mayo', cacheReporte.recomendacionesExpertoMayo), ('Junio', cacheReporte.recomendacionesExpertoJunio), ('Julio', cacheReporte.recomendacionesExpertoJulio), ('Agosto', cacheReporte.recomendacionesExpertoAgosto), ('Septiembre', cacheReporte.recomendacionesExpertoSeptiembre), ('Octubre', cacheReporte.recomendacionesExpertoOctubre), ('Noviembre', cacheReporte.recomendacionesExpertoNoviembre), ('Diciembre', cacheReporte.recomendacionesExpertoDiciembre)]
            ancho_columnas = [300, 200]
            tabla = Table(datos_tabla, ancho_columnas)

            estilo_tabla = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), 'gray'),
                ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), 'white'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, 'black')
            ])
            
            tabla.setStyle(estilo_tabla)
            # Agregar la tabla al documento
            # canvas.drawCentredString(150, 100, "Tabla de meses y cantidades")
            tabla.wrapOn(canvas, 0, 0)
            tabla.drawOn(canvas, 50, 100)


            # Agregar un espacio en blanco
            canvas.drawString(100, 600, "")
            canvas.showPage()
            
            # Guardar el archivo PDF y limpiar la memoria
            canvas.save()
            plt.clf()
    # CIERRE DE INTERFAZ

    def close_System_Rest(self, obj):
        self.dialog.dismiss()
        sys.exit()

    def close_dialog(self,obj):
		# Close alert box
	    self.dialog.dismiss()
    
    




class MyHero(MDHeroFrom):
    def on_transform_out(
        self, instance_hero_widget: MDRelativeLayout, duration: float
    ):
        '''Called when the hero back from screen **B** to screen **A**.'''




Test().run()
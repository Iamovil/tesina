# from tensorflow.keras.optimizers import Adam
from keras.utils import load_img,img_to_array
import numpy as np
from keras.models import load_model
import os.path
import gc
import keras.backend as K

def RealizarEscaneo(imagena):
  imagen = imagena

  model = 'modelo_checkpoint.h5'  
  pesos = 'pesos_checkpoint.h5'


  # Cargar el modelo y los pesos de la CNN entrenada
  cnn = load_model(model)
  cnn.load_weights(pesos)
  
  # Cargar y redimensionar la imagen
  imagen_clasificar = load_img(imagen, target_size=(416, 416))
  imagen_clasificar = img_to_array(imagen_clasificar)
  imagen_clasificar = np.expand_dims(imagen_clasificar, axis=0)

  # Evaluar la clase de pertenencia
  clase = cnn.predict(imagen_clasificar)

  print(clase[0])

  arg_max = np.argmax(clase[0])
  print(arg_max)

  if arg_max == 0:
    del cnn
    del imagen_clasificar
    K.clear_session()  # Liberar memoria de TensorFlow
    gc.collect()
    return "Didymella"
  
  if arg_max == 1:
    del cnn
    del imagen_clasificar
    K.clear_session()  # Liberar memoria de TensorFlow
    gc.collect()
    return "Araña Roja"
  
  if arg_max == 2:
    del cnn
    del imagen_clasificar
    K.clear_session()  # Liberar memoria de TensorFlow
    gc.collect()
    return "Planta sana"
  
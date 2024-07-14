from tkinter import messagebox

import cv2
import os
import face_recognition as fr
import pickle

def train_model():
    # crear base de datos
    ruta = 'dataset'
    mis_imagenes = []
    numeros_ci = []
    lista_ci = os.listdir(ruta)

    for nombre in lista_ci:
        imagen_actual = cv2.imread(f'{ruta}\{nombre}')
        mis_imagenes.append((imagen_actual))
        numeros_ci.append(os.path.splitext(nombre)[0])
    print(numeros_ci)
    lista_ci_codificada = codificar(mis_imagenes)

    # Guardar la lista codificada en un archivo
    with open('lista_ci_codificada.pkl', 'wb') as f:
        pickle.dump(lista_ci_codificada, f)

    # Guardar la lista numeros_ci en un archivo
    with open('numeros_ci.pkl', 'wb') as f:
        pickle.dump(numeros_ci, f)

    messagebox.showinfo("Aviso", "Modelo entrenado correctamente")  #codifica las imagenes de la carpeta dataset


#coficar imagenes
def codificar(imagenes):
    #crear una lista nueva
    lista_codificada = []

    #pasar todas las imagenes rgb
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        #codificar
        codificado = fr.face_encodings(imagen)[0]

        #agregar a la lista
        lista_codificada.append(codificado)
    #devolver lista codificada
    return lista_codificada

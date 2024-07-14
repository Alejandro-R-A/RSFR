import cv2
import os
import datetime
import tkinter as tk
from tkinter import messagebox, Tk, simpledialog
from Data_base.db_connection import insert_to_db_in, insert_to_db_out
import pickle
import face_recognition as fr
import numpy
import pyautogui

from notes_delivery_return import reemplazar_texto_return, reemplazar_texto_delivery, create_note_return, create_note_delivery


def center_window(root):
    # Actualiza la ventana para asegurarte de que tiene las dimensiones correctas
    root.update()

    # Obtiene el ancho y la altura de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Obtiene el ancho y la altura de la ventana
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calcula la posición de la ventana para que esté centrada
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Posiciona la ventana
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")


def in_evaluate_model():
    root = Tk()
    root.withdraw()
    # tomar una imagen de camara web
    #captura = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true")
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # leer imagen de la camara
        exito, imagen = captura.read()
        if not exito:
            print("no se ha podido tomar la captura")
        else:
            # Muestra la imagen de la cámara en una ventana
            cv2.imshow('Imagen web', imagen)

            # Obtiene el tamaño de la pantalla
            screen_width, screen_height = pyautogui.size()

            # Calcula la posición de la ventana para que esté centrada
            position_right = int(screen_width / 2 - imagen.shape[1] / 2)
            position_top = int(screen_height / 2 - imagen.shape[0] / 2)

            # Mueve la ventana de la cámara al centro
            cv2.moveWindow('Imagen web', position_right, position_top)

            # Espera a que se presione la tecla Q para tomar la foto o Esc para cerrar la cámara
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                # Cargar la lista codificada desde el archivo
                with open('lista_ci_codificada.pkl', 'rb') as f:
                    lista_ci_codificada = pickle.load(f)

                # Cargar la lista numeros_ci desde el archivo
                with open('numeros_ci.pkl', 'rb') as f:
                    numeros_ci = pickle.load(f)

                # reconocer cara en captura
                cara_captura = fr.face_locations(imagen)
                # codificar cara capturada
                cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

                # buscar coincidencias
                for caracodif, caraubic in zip(cara_captura_codificada, cara_captura):
                    coincidencias = fr.compare_faces(lista_ci_codificada, caracodif)
                    distancias = fr.face_distance(lista_ci_codificada, caracodif)

                    print(distancias)

                    indice_coincidencia = numpy.argmin(distancias)

                    # mostrar coincidencias si las hay
                    if distancias[indice_coincidencia] > 0.6:
                        print("no coincide con nuestros empleados")
                        messagebox.showerror("Error", "El rostro no coincide con ninguna persona")
                    else:
                        print("bienvenido")
                        # buscar el nombre del empleado encontrado
                        nombre = numeros_ci[indice_coincidencia]

                        confirm = messagebox.askyesno("Confirmación",
                                                      "Persona reconocida con número de carnet: {}. ¿Es correcto?".format(
                                                          nombre), parent=root)
                        if confirm:
                            captura.release()
                            cv2.destroyAllWindows()
                            take_photo(nombre)
                            reemplazar_texto_delivery('format_register/format_note_delivery.docx', create_note_delivery(), nombre)
                break
            elif key & 0xFF == 27:  # 27 es el código ASCII para la tecla 'Esc'
                print("Cámara cerrada")
                break

    # Cuando se termina el bucle, se libera la cámara y se cierran todas las ventanas
    captura.release()
    cv2.destroyAllWindows()



def take_photo(carnet):
    #cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()

        # Muestra la imagen de la cámara en una ventana
        cv2.imshow('Presiona q para tomar la foto', frame)

        # Obtiene el tamaño de la pantalla
        screen_width, screen_height = pyautogui.size()

        # Calcula la posición de la ventana para que esté centrada
        position_right = int(screen_width / 2 - frame.shape[1] / 2)
        position_top = int(screen_height / 2 - frame.shape[0] / 2)

        # Mueve la ventana de la cámara al centro
        cv2.moveWindow('Presiona q para tomar la foto', position_right, position_top)

        # Espera hasta que se presione la tecla 'Q' para tomar la foto o 'Esc' para cerrar la cámara
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            folder_name = 'Documents/' + datetime.datetime.now().strftime("%d-%m-%Y") + '/fotos'
            os.makedirs(folder_name, exist_ok=True)
            cv2.imwrite(folder_name + '/' + carnet + '.jpg', frame)
            print("Foto guardada exitosamente")
            messagebox.showinfo("Registro", "Foto guardada exitosamente")
            root = tk.Tk()
            root.withdraw()
            center_window(root)
            motivo = simpledialog.askstring("Input", "¿Cuál es el motivo?", parent=root)
            print("Motivo: ", motivo)
            root = tk.Tk()
            root.withdraw()
            center_window(root)
            observacion = simpledialog.askstring("Input", "¿Cuál es la observacion?", parent=root)
            print("Observacion: ", observacion)
            insert_to_db_in(carnet, motivo, observacion)
            break
        elif key & 0xFF == 27:  # 27 es el código ASCII para la tecla 'Esc'
            print("Cámara cerrada")
            break

    cap.release()
    cv2.destroyAllWindows()


def out_evaluate_model():
    root = Tk()
    root.withdraw()
    # tomar una imagen de camara web
    #captura = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true")
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # leer imagen de la camara
        exito, imagen = captura.read()
        if not exito:
            print("no se ha podido tomar la captura")
        else:
            # Muestra la imagen de la cámara en una ventana
            cv2.imshow('Imagen web', imagen)

            # Obtiene el tamaño de la pantalla
            screen_width, screen_height = pyautogui.size()

            # Calcula la posición de la ventana para que esté centrada
            position_right = int(screen_width / 2 - imagen.shape[1] / 2)
            position_top = int(screen_height / 2 - imagen.shape[0] / 2)

            # Mueve la ventana de la cámara al centro
            cv2.moveWindow('Imagen web', position_right, position_top)

            # Espera a que se presione la tecla Q para tomar la foto o Esc para cerrar la cámara
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                # Cargar la lista codificada desde el archivo
                with open('lista_ci_codificada.pkl', 'rb') as f:
                    lista_ci_codificada = pickle.load(f)

                # Cargar la lista numeros_ci desde el archivo
                with open('numeros_ci.pkl', 'rb') as f:
                    numeros_ci = pickle.load(f)

                # reconocer cara en captura
                cara_captura = fr.face_locations(imagen)
                # codificar cara capturada
                cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

                # buscar coincidencias
                for caracodif, caraubic in zip(cara_captura_codificada, cara_captura):
                    coincidencias = fr.compare_faces(lista_ci_codificada, caracodif)
                    distancias = fr.face_distance(lista_ci_codificada, caracodif)

                    print(distancias)

                    indice_coincidencia = numpy.argmin(distancias)

                    # mostrar coincidencias si las hay
                    if distancias[indice_coincidencia] > 0.6:
                        print("no coincide con nuestros empleados")
                        messagebox.showerror("Error", "No coincide con ninguna persona")
                    else:
                        print("bienvenido")
                        # buscar el nombre del empleado encontrado
                        nombre = numeros_ci[indice_coincidencia]

                        confirm = messagebox.askyesno("Confirmación",
                                                      "Persona reconocida con número de carnet: {}. ¿Es correcto?".format(
                                                          nombre), parent=root)
                        if confirm:
                            captura.release()
                            cv2.destroyAllWindows()

                            # Crea una ventana de Tkinter para el input del motivo
                            root = tk.Tk()
                            root.withdraw()  # Oculta la ventana principal de Tkinter
                            center_window(root)  # Centra la ventana
                            motivo = simpledialog.askstring("Input", "¿Cuál es el motivo?", parent=root)
                            print("Motivo: ", motivo)  # Imprime el motivo ingresado

                            root = tk.Tk()
                            root.withdraw()  # Oculta la ventana principal de Tkinter
                            center_window(root)  # Centra la ventana
                            observacion = simpledialog.askstring("Input", "¿Cuál es la observación?", parent=root)
                            print("obs: ", observacion)  # Imprime el motivo ingresado

                            insert_to_db_out(nombre, observacion, motivo)
                            reemplazar_texto_return('format_register/format_note_return.docx', create_note_return(), nombre)
                break
            elif key & 0xFF == 27:  # 27 es el código ASCII para la tecla 'Esc'
                print("Cámara cerrada")
                break

    captura.release()
    cv2.destroyAllWindows()





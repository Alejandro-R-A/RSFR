import cv2
import os
from tkinter import simpledialog, messagebox
from tkinter import Tk
import face_recognition as fr
import pyautogui

def center_window(root, width=300, height=200):
    # Obtiene las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula la posición x e y para centrar la ventana
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def collect_data():
    # Crea una ventana de Tkinter y ocúltala
    root = Tk()
    root.withdraw()

    # Centra la ventana
    center_window(root)

    # Muestra un cuadro de diálogo para ingresar el número de carnet
    root.update()  # Actualiza la ventana antes de mostrar el cuadro de diálogo
    ci_name = simpledialog.askstring("Input", "Ingresa el número de carnet:", parent=root)

    print ("open camera")
    #cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # Captura un frame de la cámara
        ret, frame = cap.read()

        # Muestra el frame en una ventana
        cv2.imshow('Presiona Q para tomar la foto', frame)

        # Obtiene el tamaño de la pantalla
        screen_width, screen_height = pyautogui.size()

        # Calcula la posición de la ventana para que esté centrada
        position_right = int(screen_width / 2 - frame.shape[1] / 2)
        position_top = int(screen_height / 2 - frame.shape[0] / 2)

        # Mueve la ventana de la cámara al centro
        cv2.moveWindow('Presiona Q para tomar la foto', position_right, position_top)

        # Espera hasta que se presione la tecla 'Q' o 'Esc'
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            # Guarda la foto con el número de CI directamente en la carpeta 'dataset'
            cv2.imwrite('dataset/{}.jpg'.format(ci_name), frame)
            break
        elif key & 0xFF == 27:  # 27 es el código ASCII para la tecla 'Esc'
            print("Cámara cerrada")
            break

    cap.release()
    cv2.destroyAllWindows()

    messagebox.showinfo("Aviso", "Foto guardada con exito")





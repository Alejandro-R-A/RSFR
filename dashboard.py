from tkinter import Tk, Button, Frame
from tkinter import font as tkFont
from face_recognition_local import in_recognize_face, out_recognize_face
from data_collection import collect_data
from massive_register import massive_register
from period_reports import period_reports_out, period_reports_in
from train_model import train_model

def show_dashboard(root):
    # Crear una nueva ventana
    dashboard = Tk()
    dashboard.title("Dashboard")

    # Configura el tamaño de la ventana
    dashboard.geometry("400x400")

    # Obtiene las dimensiones de la ventana
    window_width = dashboard.winfo_reqwidth()
    window_height = dashboard.winfo_reqheight()

    # Obtiene la posición de la mitad de la pantalla
    position_right = int(dashboard.winfo_screenwidth()/2 - window_width/2)
    position_down = int(dashboard.winfo_screenheight()/2 - window_height/2)

    # Posiciona la ventana en el centro de la pantalla
    dashboard.geometry("+{}+{}".format(position_right, position_down))

    # Configura el estilo de la fuente
    fontStyle = tkFont.Font(family="Lucida Grande", size=12)

    # Crea un marco para los botones
    frame = Frame(dashboard)
    frame.pack(pady=20)

    # Crea botones para cada función
    Button(frame, text="Registro entrada", command=registro_entrada, font=fontStyle).pack(fill='x', pady=5)
    Button(frame, text="Registro salida", command=registro_salida, font=fontStyle).pack(fill='x', pady=5)
    Button(frame, text="Nuevo registro en el sistema", command=nuevo_registro, font=fontStyle).pack(fill='x', pady=5)
    Button(frame, text="Nuevo registro biometrico", command=nuevo_registro_biometrico, font=fontStyle).pack(fill='x', pady=5)
    Button(frame, text="Actualizar IA", command=actualizar_ia, font=fontStyle).pack(fill='x', pady=5)
    Button(frame, text="Reportes de Entrada", command=reportes_entrada, font=fontStyle).pack(fill='x', pady=5)
    Button(frame, text="Reportes de Salida", command=reportes_salida, font=fontStyle).pack(fill='x', pady=5)

    # Configurar el evento de cierre de la ventana para mostrar la ventana de inicio de sesión
    dashboard.protocol("WM_DELETE_WINDOW", lambda: on_close(dashboard, root))

    dashboard.mainloop()  # Iniciar el mainloop para la nueva ventana

def registro_entrada():
    # Inicia el reconocimiento facial
    out_recognize_face()

def registro_salida():
    # Implementa la funcionalidad de registro de salida aquí
    in_recognize_face()

def nuevo_registro():
    # Implementa la funcionalidad de nuevo registro en el sistema aquí
    massive_register()

def nuevo_registro_biometrico():
    # Implementa la funcionalidad de nuevo registro en el sistema aquí
    collect_data()

def actualizar_ia():
    # Implementa la funcionalidad de nuevo registro en el sistema aquí
    train_model()

def reportes_entrada():
    # Implementa la funcionalidad de reportes aquí
    period_reports_in()

def reportes_salida():
    # Implementa la funcionalidad de reportes aquí
    period_reports_out()


def on_close(dashboard, root):
    # Cuando se cierre el dashboard, mostrar la ventana de inicio de sesión
    dashboard.destroy()
    root.deiconify()

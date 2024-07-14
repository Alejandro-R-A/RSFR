from tkinter import Tk, Label, Entry, Button, StringVar
from tkinter import font as tkFont
from login import login
from dashboard import show_dashboard

root = Tk()
root.title("Iniciar sesión")  # Agrega un título a la ventana

# Configura el tamaño de la ventana
root.geometry("400x300")

# Obtiene las dimensiones de la ventana
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()

# Obtiene la posición de la mitad de la pantalla
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)

# Posiciona la ventana en el centro de la pantalla
root.geometry("+{}+{}".format(position_right, position_down))

# Configura el estilo de la fuente
fontStyle = tkFont.Font(family="Lucida Grande", size=12)

nombre_usuario = StringVar()
contraseña = StringVar()

# Configura los widgets con un estilo mejorado
Label(root, text="Usuario", font=fontStyle).pack(pady=(20,10))
Entry(root, textvariable=nombre_usuario, font=fontStyle).pack()
Label(root, text="Contraseña", font=fontStyle).pack(pady=10)
Entry(root, textvariable=contraseña, show='*', font=fontStyle).pack()

Button(root, text="Iniciar sesión", command=lambda: login(root, nombre_usuario, contraseña, show_dashboard), font=fontStyle).pack(pady=20)

root.mainloop()

# login.py
from Data_base.db_connection import connect
from tkinter import messagebox, StringVar

def login(root, nombre_usuario: StringVar, contraseña: StringVar, show_dashboard):
    # Verificar las credenciales del usuario
    conexion = connect()
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM usuario WHERE nombre_usuario = %s AND contraseña = %s''', (nombre_usuario.get(), contraseña.get()))
    if cursor.fetchone() is not None:
        messagebox.showinfo("Login", "¡Inicio de sesión exitoso!")
        root.withdraw()  # Oculta la ventana de inicio de sesión
        show_dashboard(root)  # Muestra el dashboard
    else:
        messagebox.showerror("Login", "Usuario o contraseña incorrectos")
    cursor.close()
    conexion.close()

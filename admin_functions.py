import tkinter as tk
from tkinter import ttk
from Data_base.db_connection import connect
import pandas as pd

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Funciones de Administrador")
        self.geometry("1000x400")

        # Obtiene las dimensiones de la ventana
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Obtiene la posición de la mitad de la pantalla
        position_right = int(self.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.winfo_screenheight()/2 - window_height/2)

        # Posiciona la ventana en el centro de la pantalla
        self.geometry("+{}+{}".format(position_right, position_down))

        # Configura el estilo de la fuente
        self.option_add("*Font", "Lucida 12")

        # Crea un marco para los botones
        self.frame = ttk.Frame(self)
        self.frame.pack(pady=20)

        # Crea botones para cada función
        ttk.Button(self.frame, text="Mostrar lista de cursantes registrados", command=self.mostrar_lista).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Mostrar registro de entrada del día", command=self.mostrar_entrada).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Mostrar registro de salida del día", command=self.mostrar_salida).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Eliminar cursante por CI", command=self.eliminar_cursante).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Cambiar nombre de usuario", command=self.cambiar_usuario).pack(fill='x', pady=5)

        self.mainloop()

    def mostrar_lista(self):
        self.clear_frame()

        conn = connect()
        # Crea una consulta SQL para obtener los detalles del instructor
        query = """
                SELECT 
                    persona.grado, persona.ap_paterno, persona.ap_materno, persona.nombres, persona.ci, persona.exp
                FROM instructor
                INNER JOIN persona ON instructor.id_persona = persona.id_persona;
                """

        # Ejecuta la consulta y obtén los resultados
        df = pd.read_sql_query(query, conn)

        # Cierra la conexión
        conn.close()

        # Crea un marco para la tabla y las barras de desplazamiento
        table_frame = ttk.Frame(self.frame)
        table_frame.pack()

        # Crea un marco para la tabla
        table_container = ttk.Frame(table_frame)
        table_container.grid(row=0, column=0, sticky="nsew")

        # Crea una tabla en tkinter para mostrar los resultados
        table = ttk.Treeview(table_container)
        table["columns"] = list(df.columns)
        table["show"] = "headings"

        for column in df.columns:
            table.heading(column, text=column)

        for index, row in df.iterrows():
            table.insert("", "end", values=list(row))

        # Crea barras de desplazamiento para la tabla
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        # Coloca la tabla y las barras de desplazamiento en el marco
        table.grid(row=0, column=0, sticky="nsew")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        # Configura el marco para expandirse con la ventana
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        ttk.Button(self.frame, text="Volver al menú", command=self.show_menu).pack()

    def mostrar_entrada(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Aquí se mostrará el registro de entrada del día").pack()
        ttk.Button(self.frame, text="Volver al menú", command=self.show_menu).pack()

    def mostrar_salida(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Aquí se mostrará el registro de salida del día").pack()
        ttk.Button(self.frame, text="Volver al menú", command=self.show_menu).pack()

    def eliminar_cursante(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Aquí se eliminará un cursante por CI").pack()
        ttk.Button(self.frame, text="Volver al menú", command=self.show_menu).pack()

    def cambiar_usuario(self):
        self.clear_frame()
        ttk.Label(self.frame, text="Aquí se cambiará el nombre de usuario").pack()
        ttk.Button(self.frame, text="Volver al menú", command=self.show_menu).pack()

    def clear_frame(self):
        # Destruye los widgets actuales en el marco
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_frame()
        # Muestra el menú principal
        ttk.Button(self.frame, text="Mostrar lista de cursantes registrados", command=self.mostrar_lista).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Mostrar registro de entrada del día", command=self.mostrar_entrada).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Mostrar registro de salida del día", command=self.mostrar_salida).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Eliminar cursante por CI", command=self.eliminar_cursante).pack(fill='x', pady=5)
        ttk.Button(self.frame, text="Cambiar nombre de usuario", command=self.cambiar_usuario).pack(fill='x', pady=5)

app = Application()

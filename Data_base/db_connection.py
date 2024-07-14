# db_connection.py
from tkinter import messagebox
import psycopg2

def connect():
    try:
        conexion = psycopg2.connect(
            database='rsfr-db',
            user='postgres',
            password='admin',
            host='localhost',
            port="5432",
            client_encoding="UTF8"
        )
        return conexion
    except Exception as e:
        print(f"Ha ocurrido un error al conectar a la base de datos: {e}")

def insert_to_db_in(carnet, motivo, observacion):
    try:
        # Conecta a la base de datos
        conexion = connect()
        cursor = conexion.cursor()

        # Ejecuta la consulta SQL
        cursor.execute(f"""
        DO $$
        DECLARE 
            temp_id_persona INTEGER;
            temp_id_instructor INTEGER;
        BEGIN
            -- Primero, obtenemos el id_persona a través del número de carnet
            SELECT id_persona INTO temp_id_persona FROM persona WHERE ci = '{carnet}';

            -- Luego, obtenemos el id_instructor correspondiente a esa persona
            SELECT id_instructor INTO temp_id_instructor FROM instructor WHERE id_persona = temp_id_persona;

            -- Finalmente, insertamos en la tabla registro_salida
            INSERT INTO registro_salida (id_instructor, motivo, observaciones, fecha_salida) 
            VALUES (temp_id_instructor, '{motivo}', '{observacion}', NOW());
        END $$;
        """)

        # Confirma los cambios y cierra la conexión
        conexion.commit()
        cursor.close()
        conexion.close()

        print("Registro agregado exitosamente a la base de datos")  # Aviso de éxito
        messagebox.showinfo("Registro", "Registro agregado exitosamente a la base de datos")
    except Exception as e:
        print(f"Ha ocurrido un error al insertar en la base de datos: {e}")
        messagebox.showerror("Registro", f"Ha ocurrido un error al insertar en la base de datos: {e}")

def insert_to_db_out(carnet, observacion, motivo):
    try:
        # Conecta a la base de datos
        conexion = connect()
        cursor = conexion.cursor()

        # Ejecuta la consulta SQL
        cursor.execute(f"""
        DO $$
        DECLARE 
            temp_id_persona INTEGER;
            temp_id_instructor INTEGER;
        BEGIN
            -- Primero, obtenemos el id_persona a través del número de carnet
            SELECT id_persona INTO temp_id_persona FROM persona WHERE ci = '{carnet}';

            -- Luego, obtenemos el id_instructor correspondiente a esa persona
            SELECT id_instructor INTO temp_id_instructor FROM instructor WHERE id_persona = temp_id_persona;

            -- Finalmente, insertamos en la tabla registro_salida
            INSERT INTO registro_entrada (id_instructor, motivo, observaciones, fecha_entrada) 
            VALUES (temp_id_instructor,'{motivo}', '{observacion}', NOW());
        END $$;
        """)

        # Confirma los cambios y cierra la conexión
        conexion.commit()
        cursor.close()
        conexion.close()

        print("Registro agregado exitosamente a la base de datos")  # Aviso de éxito
        messagebox.showinfo("Registro", "Registro agregado exitosamente a la base de datos")
    except Exception as e:
        print(f"Ha ocurrido un error al insertar en la base de datos: {e}")
        messagebox.showerror("Registro", f"Ha ocurrido un error al insertar en la base de datos: {e}")

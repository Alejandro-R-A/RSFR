import pandas as pd
import psycopg2
from tkinter import filedialog, Tk, messagebox

def massive_register():
    # Crea una ventana de Tkinter y ocúltala
    root = Tk()
    root.withdraw()

    # Abre el cuadro de diálogo para seleccionar el archivo Excel
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])

    # Lee el archivo Excel, omitiendo las primeras 8 filas
    df = pd.read_excel(file_path, skiprows=8)
    #print(df.columns)

    # Después de leer el archivo Excel
    df['AÑO DE DOTACIÓN - P'] = df['AÑO DE DOTACIÓN - P'].fillna(0).astype(int)
    df['AÑO DE DOTACIÓN - C'] = df['AÑO DE DOTACIÓN - C'].fillna(0).astype(int)
    df['AÑO DE DOTACIÓN - E'] = df['AÑO DE DOTACIÓN - E'].fillna(0).astype(int)
    df['AÑO DE EGRESO'] = df['AÑO DE EGRESO'].fillna(0).astype(int)
    df['C.I.'] = df['C.I.'].fillna(0).astype(int)



    # Conecta a la base de datos
    conexion = psycopg2.connect(
        database='rsfr-db',
        user='postgres',
        password='admin',
        host='localhost',
        port="5432",
        client_encoding="UTF8"
    )
    cursor = conexion.cursor()

    # Itera sobre cada fila del DataFrame
    for _, row in df.iterrows():
        # Inserta en la tabla arma
        cursor.execute("""
            INSERT INTO arma
            (anio_dotacion, num_pistola, calibre, marca, modelo, procedencia, num_cargadores, observacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_arma;
        """, (row['AÑO DE DOTACIÓN - P'], row['N° DE PISTOLA'], row['CALIBRE'], row['MARCA - P'], row['MODELO - P'], row['PROCEDENCIA - P'], row['Nº DE CARGADORES'], row['OBS. - P']))
        id_arma = cursor.fetchone()[0]

        # Inserta en la tabla bayoneta
        cursor.execute("""
            INSERT INTO bayoneta
            (anio_dotacion, num_cuchillo, marca, modelo, procedencia, observacion)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_bayoneta;
        """, (row['AÑO DE DOTACIÓN - C'], row['N° DE CUCHILLO'], row['MARCA - C'], row['MODELO - C'], row['PROCEDENCIA - C'], row['OBS. - C']))
        id_bayoneta = cursor.fetchone()[0]

        # Inserta en la tabla espada
        cursor.execute("""
            INSERT INTO espada
            (anio_dotacion, descripcion, marca, procedencia, observacion)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_espada;
        """, (row['AÑO DE DOTACIÓN - E'], row['DESCRIPCION'], row['MARCA - E'], row['PROCEDENCIA - E'], row['OBS. - E']))
        id_espada = cursor.fetchone()[0]

        # Inserta en la tabla persona
        cursor.execute("""
            INSERT INTO persona
            (grado, ap_paterno, ap_materno, nombres, ci, "exp", año_egreso, inst_mil_egreso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_persona;
        """, (row['GRADO'], row['AP. PATERNO'], row['AP. MATERNO'], (str(row['NOMBRE']) if pd.notnull(row['NOMBRE']) else '') + ' ' + (str(row['SEGUNDO NOMBRE']) if pd.notnull(row['SEGUNDO NOMBRE']) else ''), row['C.I.'], row['EXP.'], row['AÑO DE EGRESO'], row['INST. MILITAR DE EGRESO']))
        id_persona = cursor.fetchone()[0]

        # Inserta en la tabla instructor
        cursor.execute("""
            INSERT INTO instructor
            (id_persona, id_arma, id_bayoneta, id_espada)
            VALUES (%s, %s, %s, %s);
        """, (id_persona, id_arma, id_bayoneta, id_espada))

    # Confirma los cambios y cierra la conexión
    conexion.commit()
    cursor.close()
    conexion.close()

    print("Registros agregados exitosamente a la base de datos")  # Aviso de éxito
    messagebox.showinfo("Registro", "Registros agregados exitosamente a la base de datos")

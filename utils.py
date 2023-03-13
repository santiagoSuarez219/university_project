import pandas as pd
import os

def create_folder(name_folder):
    if not os.path.exists(name_folder):
        os.makedirs(name_folder)

def add_date_csv(name_csv,nuevo_dato):
    df = pd.read_csv(os.path.join('csv_s',name_csv))
    nueva_fila = pd.DataFrame([nuevo_dato])
    df = df.append(nueva_fila, ignore_index=True)
    df.to_csv(os.path.join('csv_s',name_csv), index=False)
    print(f"Dato {nuevo_dato} añadido exitosamente.")
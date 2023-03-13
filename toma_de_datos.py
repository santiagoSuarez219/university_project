import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
import pandas as pd

def guardar_imagen_matriz(fig,data,data_interpolate):
    now = datetime.datetime.now()

    filename_image = f"plot_{now:%Y-%m-%d_%H-%M-%S}.png"
    file_name_npy_interpolate = f"data_{now:%Y-%m-%d_%H-%M-%S}.npy"
    file_name_npy_uninterpolate = f"data_{now:%Y-%m-%d_%H-%M-%S}.npy"
    
    if not os.path.exists('images_prueba'):
        os.makedirs('images_prueba')
    if not os.path.exists('npy_interpolate_prueba'):
        os.makedirs('npy_interpolate_prueba')
    if not os.path.exists('npy_uninterpolate_prueba'):
        os.makedirs('npy_uninterpolate_prueba')
    
    fig.savefig(os.path.join('images_prueba', filename_image))
    print('Imagen guardada')
    np.save(os.path.join('npy_interpolate_prueba', file_name_npy_interpolate), data_interpolate)
    np.save(os.path.join('npy_uninterpolate_prueba', file_name_npy_uninterpolate), data)
    print('Matrices guardadas')
    create_save_date_frame()
    add_date_csv()

def create_save_date_frame():
    if not os.path.exists('csv_s'):
        os.makedirs('csv_s')
    if not os.path.isfile('csv_s/data.csv'):
        data = {
        'valor_tempereratura': [],
        'temperatura_patron': [],
        'temperatura_sensor': []
        }
        df_data = pd.DataFrame(data)
        df_data.to_csv(os.path.join('csv_s', 'data.csv'),index = False)

def add_date_csv():
    valor_temperatura = float(input('Ingrese el valor de la temperatura: '))
    temperatura_patron = float(input('Ingrese el valor del patron: '))
    nuevo_dato = {
        'valor_tempereratura': valor_temperatura,
        'temperatura_patron': temperatura_patron,
        'temperatura_sensor': 25.3
        }

    df = pd.read_csv(os.path.join('csv_s','data.csv'))
    nueva_fila = pd.DataFrame([nuevo_dato])
    df = df.append(nueva_fila, ignore_index=True)
    df.to_csv(os.path.join('csv_s','data.csv'), index=False)
    print(f"Dato {nuevo_dato} añadido exitosamente.")

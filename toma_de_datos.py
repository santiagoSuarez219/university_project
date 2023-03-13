import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
import pandas as pd
import utils as ut
import uuid

def guardar_imagen_matriz(fig,data,data_interpolate_cubic,data_interpolate_linear,valor_temperatura,temperatura_sensor):
    
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
    temperatura_patron = float(input('Ingrese el valor del patron: '))
    id = str(uuid.uuid4())
    
    ut.create_folder('images_prueba')
    ut.create_folder('npy_interpolate_linear_prueba')
    ut.create_folder('npy_interpolate_cubic_prueba')
    ut.create_folder('npy_uninterpolate_prueba')
    
    fig.savefig(os.path.join('images_prueba', id + '.png'))
    print('Imagen guardada')
    np.save(os.path.join('npy_interpolate_linear_prueba', id + '.npy'), data_interpolate_linear)
    np.save(os.path.join('npy_interpolate_cubic_prueba', id + '.npy'), data_interpolate_cubic)
    np.save(os.path.join('npy_uninterpolate_prueba', id + '.npy'), data)
    print('Matrices guardadas')
    create_save_date_frame()
    create_row_csv(valor_temperatura, fecha_actual,hora_actual,temperatura_patron,id,temperatura_sensor)

def create_csv(folder, name):
    if not os.path.isfile(os.path.join(folder, name)):
        data = {
        'fecha':[],
        'hora':[],
        'temperatura_patron': [],
        'temperatura_sensor': [],
        'codigo':[]
        }
        df_data = pd.DataFrame(data)
        df_data.to_csv(os.path.join(folder, name),index = False)

def create_save_date_frame():
    ut.create_folder('csv_s')
    create_csv('csv_s','temperature_25.csv')
    create_csv('csv_s','temperature_30.csv')
    create_csv('csv_s','temperature_35.csv')
    create_csv('csv_s','temperature_40.csv')
    create_csv('csv_s','temperature_45.csv')
    create_csv('csv_s','temperature_50.csv')


def create_row_csv(valor_temperatura, fecha_actual,hora_actual,temperatura_patron,id, temperatura_sensor):
    nuevo_dato = {
        'fecha':fecha_actual,
        'hora':hora_actual,
        'temperatura_patron': temperatura_patron,
        'temperatura_sensor': temperatura_sensor,
        'error_relativo': (abs(temperatura_patron - temperatura_sensor)/temperatura_patron)*100,
        'codigo':id
        }
    
    if valor_temperatura == 25:
        ut.add_date_csv('temperature_25.csv',nuevo_dato)
    elif valor_temperatura == 30:
        ut.add_date_csv('temperature_30.csv',nuevo_dato)
    elif valor_temperatura == 35:
        ut.add_date_csv('temperature_35.csv',nuevo_dato)
    elif valor_temperatura == 40:
        ut.add_date_csv('temperature_40.csv',nuevo_dato)
    elif valor_temperatura == 45:
        ut.add_date_csv('temperature_45.csv',nuevo_dato)
    elif valor_temperatura == 50:
        ut.add_date_csv('temperature_50.csv',nuevo_dato)

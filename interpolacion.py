import numpy as np
import matplotlib.pyplot as plt
import serial
import sys
from improve_resolution import improve_resolution
import toma_de_datos as tp

def on_key_press(event):
    if event.key == 'g':
        tp.guardar_imagen_matriz(fig,data,data_interpolada)
    elif event.key == 'e':
        sys.exit()

# Configuración de la comunicación serial
ser = serial.Serial('/dev/ttyUSB1', 115200) 
ser.flushInput()

plt.ion()
fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(12, 7))
image_real_time = ax[0].imshow(np.zeros((24,32)),cmap='jet',vmin=0,vmax=60)
image_sin_interpolacion= ax[1].imshow(np.zeros((24,32)),cmap='jet',vmin=0,vmax=60)
barra_temperatura = fig.colorbar(image_real_time)
barra_temperatura_sin_interpolacion = fig.colorbar(image_sin_interpolacion)
barra_temperatura.set_label('Temperature [$^{\circ}$C]',fontsize=14)
barra_temperatura_sin_interpolacion.set_label('Temperature [$^{\circ}$C]',fontsize=14)
ax[0].set_title('Datos interpolados')
ax[1].set_title('Datos sin interpolacion')

cid = fig.canvas.mpl_connect('key_press_event', on_key_press)

while True:
    try:
        data = ser.readline().decode().strip().split(',')
        data = [element for element in data if element and 0 <= float(element) <= 100]
        if len(data) == 768:
            data = np.array(data, dtype=float).reshape(24, 32)
            data_interpolada = improve_resolution(data)
            image_real_time.set_data(data_interpolada)
            image_real_time.set_clim(vmin = np.min(data_interpolada), vmax=np.max(data_interpolada))
            image_sin_interpolacion.set_data(data)
            image_sin_interpolacion.set_clim(vmin = np.min(data), vmax=np.max(data))
            fig.tight_layout()
            plt.pause(0.01)
        
    except KeyboardInterrupt:
        ser.close()
        break
import numpy as np
import matplotlib.pyplot as plt
import serial
import sys
import improve_resolution as ims
import toma_de_datos as tp

def on_key_press(event):
    if event.key == 'g':
        tp.guardar_imagen_matriz(fig,data,data_interpolate_cubic,data_interpolate_linear,valor_temperatura)
    elif event.key == 'e':
        sys.exit()

# Configuración de la comunicación serial
ser = serial.Serial('/dev/ttyUSB0', 115200) 
ser.flushInput()

plt.ion()
fig, ax = plt.subplots(nrows=1,ncols=3,figsize=(12, 7))
image_real_time = ax[0].imshow(np.zeros((24,32)),cmap='jet',vmin=0,vmax=60)
image_sin_interpolacion= ax[1].imshow(np.zeros((24,32)),cmap='jet',vmin=0,vmax=60)
image_linear_interpolation= ax[2].imshow(np.zeros((24,32)),cmap='jet',vmin=0,vmax=60)

barra_temperatura = fig.colorbar(image_real_time)
barra_temperatura_sin_interpolacion = fig.colorbar(image_sin_interpolacion)
cbar_image_linear_interpolation = fig.colorbar(image_linear_interpolation)
ax[0].set_title('Datos interpolados cubica')
ax[1].set_title('Datos sin interpolacion')
ax[2].set_title('Datos interpolacion lineal')

cid = fig.canvas.mpl_connect('key_press_event', on_key_press)

valor_temperatura = 25

while True:
    try:
        data = ser.readline().decode().strip().split(',')
        data = [element for element in data if element and 0 <= float(element) <= 100]
        if len(data) == 768:
            data = np.array(data, dtype=float).reshape(24, 32)
            data_interpolate_cubic = ims.improve_resolution(data)
            data_interpolate_linear = ims.linear_interpolation(data)
            image_real_time.set_data(data_interpolate_linear)
            image_real_time.set_clim(vmin = np.min(data_interpolate_linear), vmax=np.max(data_interpolate_linear))
            image_sin_interpolacion.set_data(data)
            image_sin_interpolacion.set_clim(vmin = np.min(data), vmax=np.max(data))
            image_linear_interpolation.set_data(data_interpolate_cubic)
            image_linear_interpolation.set_clim(vmin = np.min(data_interpolate_cubic), vmax=np.max(data_interpolate_cubic))

            fig.tight_layout()
            plt.pause(0.01)
        
    except KeyboardInterrupt:
        ser.close()
        break
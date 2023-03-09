import numpy as np
import matplotlib.pyplot as plt
import serial
import cv2
from improve_resolution import improve_resolution

# Configuración de la comunicación serial
ser = serial.Serial('/dev/ttyUSB0', 115200) 
ser.flushInput()

plt.ion()
fig, ax = plt.subplots(figsize=(12,7))
image_real_time = ax.imshow(np.zeros((24,32)),cmap='jet',vmin=0,vmax=60)
barra_temperatura = fig.colorbar(image_real_time)
barra_temperatura.set_label('Temperature [$^{\circ}$C]',fontsize=14)
plt.title('Mlx90640 Real-time Image')

while True:
    try:
        data = ser.readline().decode().strip().split(',')
        data = [element for element in data if element and 0 <= float(element) <= 100]
        if len(data) == 768:
            data = np.array(data, dtype=float).reshape(24, 32)
            scale = 4
            data = improve_resolution(data, scale)
            image_real_time.set_data(data)
            image_real_time.set_clim(vmin = np.min(data), vmax=np.max(data))
            plt.pause(0.01)
    except KeyboardInterrupt:
        ser.close()
        break
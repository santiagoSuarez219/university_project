import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp
import serial
import time
from tkinter import *
import datetime
import os
import sys

detener = False

def save_fig_and_save_csv():
    now = datetime.datetime.now()
    
    filename_image = f"plot_{now:%Y-%m-%d_%H-%M-%S}.png"
    file_name_npy = f"data_{now:%Y-%m-%d_%H-%M-%S}.npy"  
    if not os.path.exists('images_liquido'):
        os.makedirs('images_liquido')
    if not os.path.exists('npy_files_liquido'):
        os.makedirs('npy_files_liquido')
    
    np.save(os.path.join('npy_files_liquido', file_name_npy), terp)
    plt.savefig(os.path.join('images_liquido', filename_image)) 
    
def close_fig():
    global detener
    detener = True
    sys.exit()

ser = serial.Serial('/dev/ttyUSB0')
# ser = serial.Serial('COM6')
ser.timeout = 1
ser.baudrate = 115200
ser.bytesize = 8
ser.parities = 0
ser.stopbits = 1

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

fig, ax = plt.subplots()
im = ax.imshow(np.zeros((24, 32)), cmap='jet')
cbar = fig.colorbar(im)
plt.title('Mlx90640 Real-time Image')

term = np.zeros([32,24])
x1 = np.arange(0,32)
y1 = np.arange(0,24)

x2 = np.arange(0,32,0.125)
y2 = np.arange(0,24,0.125)

root = Tk()
frame = Frame(root)
frame.pack(side=BOTTOM)

button1 = Button(frame, text="Save", command=save_fig_and_save_csv)
button1.pack()

button2 = Button(root, text="Close Figure", command=close_fig)
button2.pack()

valor_temperatura = 35

while not detener:
    b = str(ser.readline()).split(',')
    b.pop(0)
    if len(b) == 769:
        for x in range(0, 32):
            for y in range(0, 24):
                term[x][y] = float(b[x+y*32])

    teri = interp.interp2d(y1,x1,term,kind='cubic')
    terp = teri(y2,x2)
    #plt.matshow(term,fignum=0,vmin =np.min(term),vmax =np.max(term))
    print(f'temperatura maxima: {np.max(term)}')
    print(f'temperatura minima: {np.min(term)}')
    print(f'temperatura promedio: {np.mean(terp[(terp > valor_temperatura - 2) & (terp < valor_temperatura+2)])}')
    im.set_clim(np.min(term),np.max(term))
    #im.set_clim(np.min(terp),np.max(terp))
    #cbar.set_clim(np.min(term),np.max(term))
    # plt.matshow(terp,fignum=0,vmin =np.min(term),vmax =np.max(term),cmap = 'jet')
    plt.imshow(terp,vmin =np.min(term),vmax =np.max(term),cmap = 'jet')
    #cb = plt.colorbar()
    fig.canvas.draw()
    #cb.remove() 
    
    plt.pause(1e-17)
    time.sleep(0.3)

ser.close()
root.mainloop()



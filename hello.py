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
    file_name_csv = f"data_{now:%Y-%m-%d_%H-%M-%S}.npy"  
    if not os.path.exists('Images'):
        os.makedirs('Images')
    if not os.path.exists('npy_files'):
        os.makedirs('npy_files')
    
    np.save(os.path.join('npy_files', file_name_csv), terp)
    plt.savefig(os.path.join('Images', filename_image)) 
    
def close_fig():
    global detener
    detener = True
    sys.exit()

ser = serial.Serial('/dev/ttyUSB0')
# ser = serial.Serial('COM6')
ser.baudrate = 115200
ser.bytesize = 8
ser.parities = 0
ser.stopbits = 1

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# fig, ax = plt.subplots(ncols=1)
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

while not detener:
    M90640  = ser.readline()
    M90640S = str(M90640)
    b = M90640S.split(',')
    b.pop(0)
    if len(b) == 769:
        for x in range(0, 32):
            for y in range(0, 24):
                term[x][y] = float(b[x+y*32])

    teri = interp.interp2d(y1,x1,term,kind='cubic')
    terp = teri(y2,x2)
    #plt.matshow(term,fignum=0,vmin =np.min(term),vmax =np.max(term))

    plt.imshow(terp,vmin =np.min(term),vmax =np.max(term),cmap = 'jet')
    cb = plt.colorbar()
    fig.canvas.draw()
    cb.remove() 
    
    plt.pause(1e-17)
    time.sleep(0.3)

ser.close()
root.mainloop()



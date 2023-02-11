import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp
from scipy import ndimage
import serial
import time
import save_csv

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200
ser.bytesize = 8
ser.parities = 0
ser.stopbits = 1

i = 1

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
term = np.zeros([32,24])
x1 = np.arange(0,32)
y1 = np.arange(0,24)

x2 = np.arange(0,32,0.125)
y2 = np.arange(0,24,0.125)

while True:
    M90640  = ser.readline()
    M90640S = str(M90640)
    b = M90640S.split(',')
    b.pop(0)
    if len(b) == 769:
        for x in range(0, 32):
            for y in range(0, 24):
                term[x][y] = float(b[x+y*32])
    ax1.clear()
    teri = interp.interp2d(y1,x1,term,kind='cubic')
    terp = teri(y2,x2)
    plt.matshow(term,fignum=0,vmin =np.min(term),vmax =np.max(term))
    plt.matshow(terp,fignum=0,vmin =np.min(term),vmax =np.max(term))
    plt.pause(1e-17)
    time.sleep(0.3)
    i = i + 1
ser.close()

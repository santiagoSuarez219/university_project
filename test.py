import serial
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import sys

def close_fig():
    sys.exit()

def plot_data():
    plt.ion()
    # Set up the serial port
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    
    # Create a plot with the initial data
    fig, ax = plt.subplots()
    im = ax.imshow(np.zeros((24, 32)), cmap='jet')
    fig.colorbar(im)
    plt.title('Mlx90640 Real-time Image')
    
    # Continuously update the plot with new data
    while True:
        print('while')
        # Read the data from the serial port
        data = ser.readline().decode().strip().split(',')
        data.pop(0)
        data.pop()
        if len(data) == 768:
            print('if')
            # Convert the data to a numpy array and reshape it
            data_array = np.array(data, dtype=np.float32).reshape(24, 32)
            # Update the plot with the new data
            im.set_data(data_array)
            fig.canvas.draw()

# Create the tkinter window
root = Tk()

# Add a button to start the data plot
button = Button(root, text="Start Plot", command=plot_data)
button.pack()

button2 = Button(root, text="Close Figure", command=close_fig)
button2.pack()

# Display the window
root.mainloop()   
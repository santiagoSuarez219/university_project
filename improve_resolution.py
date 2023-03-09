import cv2
import numpy as np

def improve_resolution(data, scale):
    # Convertir los datos en una imagen en escala de grises
    img = cv2.resize(data, (24, 32), interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img.astype(np.float32), cv2.COLOR_GRAY2BGR)
    
    # Aplicar un filtro bicúbico para mejorar la resolución
    img = cv2.resize(img, (192,256), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    # Convertir la imagen de vuelta a escala de grises
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return img

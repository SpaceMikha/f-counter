"""
Configuracion global del proyecto
"""

import cv2

# Configuracion de camara
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Configuracion de MediaPipe
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5

# Configuracion de comunicacion serie
SERIAL_PORT = 'COM3'
SERIAL_BAUDRATE = 9600
SERIAL_TIMEOUT = 1

# Configuracion de interfaz
WINDOW_NAME = "Protecyo ING ETSE - Mikhael da Silva"
FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 0.20
FONT_THICKNESS = 0.25

# Colores 
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0 , 0)
COLOR_BLUE2 = (13, 162, 209)
COLOR_WHITE = (255, 255, 255)
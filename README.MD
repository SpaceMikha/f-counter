# Hand Gesture Detector 🤖✋

## Descripción
Sistema de detección de gestos con las manos que controla LEDs mediante Arduino, muy basico. El proyecto utiliza visión por computadora para reconocer el número de dedos levantados y envía comandos serie a un microcontrolador Arduino para encender los LEDs correspondientes.

##  Autor
**Mikhael da Silva**  
Politecnica ETSE Robótica - USC  
Primera versión: 27/09/2025

##  Características
- Detección en tiempo real del número de dedos levantados
- Control de LEDs mediante Arduino a través de comunicación serie
- Interfaz visual con cámara web
- Código modular y extensible

##  Requisitos

### Hardware
- Arduino (Uno/Nano/ESP32)
- LEDs (cantidad según diseño)
- Resistencias para LEDs
- Cables de conexión
- Cámara web o cámara integrada

### Software
- Python 3.7+
- Arduino IDE
- OpenCV
- MediaPipe
- PySerial

##  Instalación

### 1. Clonar el repositorio

### 2. Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

### 3. Cargar código en Arduino
1. Abrir Arduino IDE
2. Cargar el código desde la carpeta `arduino-code/`
3. Seleccionar puerto y placa correcta
4. Subir el código

## Uso

### 1. Ejecutar el sistema
```bash
cd python/src
python main.py
```

### 2. Calibración
- Asegúrate de que la cámara tenga buena iluminación
- Coloca la mano a una distancia apropiada de la cámara
- El sistema detectará automáticamente los dedos levantados

### 3. Control de LEDs
- **0 dedos**: Todos los LEDs apagados
- **1 dedo**: LED 1 encendido
- **2 dedos**: LEDs 1-2 encendidos
- **3 dedos**: LEDs 1-3 encendidos
- **4 dedos**: LEDs 1-4 encendidos
- **5 dedos**: Todos los LEDs encendidos

##  Configuración

### Puerto Serie
Modifica el puerto serie en `serial_comm.py`:
```python
SERIAL_PORT = 'COM3'  # Windows
# SERIAL_PORT = '/dev/ttyUSB0'  # Linux
# SERIAL_PORT = '/dev/tty.usbserial'  # macOS
```

### Parámetros de Detección
Ajusta la sensibilidad en `hand_detector.py`:
```python
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5
```

##  Desarrollo

### Estructura de Archivos
- **`main.py`**: Punto de entrada principal
- **`hand_detector.py`**: Lógica de detección de gestos
- **`serial_comm.py`**: Comunicación con Arduino
- **`test_camera.py`**: Utilidades de prueba

### Funciones Principales
```python
# Detectar número de dedos
fingers_count = detect_fingers(frame)

# Enviar comando a Arduino
send_command(fingers_count)

# Mostrar resultado visual
display_result(frame, fingers_count)
```

##  Solución de Problemas

### La cámara no se detecta
```bash
# Verificar cámaras disponibles
python test_camera.py
```

### Arduino no responde
- Verificar conexión USB
- Comprobar puerto serie correcto
- Reiniciar Arduino

### Detección imprecisa
- Mejorar iluminación
- Ajustar distancia de la mano
- Calibrar parámetros de confianza

##  Posibles Mejoras
- [ ] Reconocimiento de gestos específicos
- [ ] Control WiFi/Bluetooth
- [ ] Interfaz gráfica avanzada
- [ ] Múltiples usuarios
- [ ] Grabación de patrones
- [ ] Integración IoT

##  Licencia
Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

##  Contribuciones
Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

##  Contacto
**Mikhael da Silva**  
ETSE  Robótica - USC  
Email: [mikhaelmiro300@gmail.com]

---
*Proyecto desarrollado como parte del programa de la Politecnica de Santiago de Compostela*
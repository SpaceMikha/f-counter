"""
Aplicación principal del contador de dedos
"""

import cv2
import time
import sys
import argparse
from hand_detector import HandDetector
from serial_comm import SerialCommunicator
import utils.config as config

class FingerCounterApp:
    def __init__(self, serial_port: str):
        self.hand_detector = HandDetector(
            detection_confidence=config.DETECTION_CONFIDENCE,
            tracking_confidence=config.TRACKING_CONFIDENCE
        )
        
        self.serial_comm = SerialCommunicator(
            port=serial_port,
            baudrate=config.SERIAL_BAUDRATE,
            timeout=config.SERIAL_TIMEOUT
        )
        
        self.cap = None
        self.running = False
        self.last_finger_count = -1
        
    def initialize_camera(self) -> bool:
        """Inicializa la cámara"""
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        
        print("Cámara inicializada correctamente")
        return True
    
    def connect_arduino(self) -> bool:
        """Conecta con Arduino"""
        if self.serial_comm.connect():
            # Enviar comando de test
            time.sleep(1)
            self.serial_comm.send_test_command()
            return True
        return False
    
    def run(self):
        """Ejecuta la aplicación principal"""
        print("=== Contador de Dedos con Arduino ===")
        
        # Inicializar componentes
        if not self.initialize_camera():
            return
        
        if not self.connect_arduino():
            print("Advertencia: No se pudo conectar con Arduino")
            print("Ejecutando en modo solo detección...")
        
        self.running = True
        print("\nInstrucciones:")
        print("- Presiona 'q' para salir")
        print("- Presiona 't' para test de LEDs")
        print("- Presiona 'r' para reconectar Arduino")
        print("\nMuestra tu mano frente a la cámara...")
        
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario")
        finally:
            self._cleanup()
    
    def _main_loop(self):
        """Bucle principal de la aplicación"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se pudo leer frame de la cámara")
                break
            
            # Voltear horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)
            
            # Detectar manos y contar dedos
            processed_frame, finger_count = self.hand_detector.detect_hands(frame)
            
            # Enviar datos a Arduino solo si hay cambios
            if finger_count != self.last_finger_count and self.serial_comm.is_connected:
                success = self.serial_comm.send_finger_count(finger_count)
                if success:
                    self.last_finger_count = finger_count
                    print(f"Dedos detectados: {finger_count}")
            
            # Dibujar estado de conexión
            self._draw_connection_status(processed_frame)
            
            # Mostrar frame
            cv2.imshow(config.WINDOW_NAME, processed_frame)
            
            # Procesar teclas
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('t') and self.serial_comm.is_connected:
                self.serial_comm.send_test_command()
                print("Ejecutando test de LEDs...")
            elif key == ord('r'):
                print("Intentando reconectar Arduino...")
                self.serial_comm.disconnect()
                self.connect_arduino()
    
    def _draw_connection_status(self, frame):
        """Dibuja el estado de conexión en el frame"""
        status_text = "Arduino: "
        if self.serial_comm.is_connected:
            status_text += "CONECTADO"
            color = config.COLOR_BLUE2
        else:
            status_text += "DESCONECTADO"
            color = config.COLOR_RED
        
        cv2.putText(
            frame, status_text,
            (10, frame.shape[0] - 20),
            config.FONT, 0.7, color, 2
        )
    
    def _cleanup(self):
        """Limpia recursos"""
        print("Cerrando aplicación...")
        self.running = False
        
        if self.cap:
            self.cap.release()
        
        self.serial_comm.disconnect()
        cv2.destroyAllWindows()
        print("Aplicación cerrada correctamente")

def main():
    parser = argparse.ArgumentParser(description='Contador de Dedos con Arduino')
    parser.add_argument(
        '--port', '-p',
        default=config.SERIAL_PORT,
        help=f'Puerto serie de Arduino (default: {config.SERIAL_PORT})'
    )
    
    args = parser.parse_args()
    
    app = FingerCounterApp(args.port)
    app.run()

if __name__ == "__main__":
    main()
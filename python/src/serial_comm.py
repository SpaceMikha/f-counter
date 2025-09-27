"""
Maneja la comunicación serie con Arduino
"""

import serial
import time
import logging
from typing import Optional

class SerialCommunicator:
    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection: Optional[serial.Serial] = None
        self.is_connected = False
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """Establece conexión con Arduino"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Esperar a que Arduino se inicialice
            self.is_connected = True
            self.logger.info(f"Conectado a Arduino en {self.port}")
            return True
            
        except serial.SerialException as e:
            self.logger.error(f"Error conectando a {self.port}: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Cierra la conexión serie"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.is_connected = False
            self.logger.info("Desconectado de Arduino")
    
    def send_finger_count(self, count: int) -> bool:
        """Envía la cantidad de dedos a Arduino"""
        if not self.is_connected or not self.serial_connection:
            return False
        
        try:
            message = f"{count}\n"
            self.serial_connection.write(message.encode())
            self.serial_connection.flush()
            return True
            
        except serial.SerialException as e:
            self.logger.error(f"Error enviando datos: {e}")
            return False
    
    def send_test_command(self) -> bool:
        """Envía comando de test a Arduino"""
        if not self.is_connected or not self.serial_connection:
            return False
        
        try:
            self.serial_connection.write(b"test\n")
            self.serial_connection.flush()
            return True
            
        except serial.SerialException as e:
            self.logger.error(f"Error enviando comando test: {e}")
            return False
    
    def read_response(self) -> Optional[str]:
        """Lee respuesta de Arduino"""
        if not self.is_connected or not self.serial_connection:
            return None
        
        try:
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode().strip()
                return response
        except serial.SerialException as e:
            self.logger.error(f"Error leyendo datos: {e}")
        
        return None
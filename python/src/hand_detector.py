"""
Detector de manos y dedos usando MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, List, Optional

class HandDetector:
    def __init__(self, detection_confidence: float = 0.7, tracking_confidence: float = 0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # IDs de landmarks para las puntas de los dedos
        self.finger_tips = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique
        self.finger_pips = [3, 6, 10, 14, 18]  # Articulaciones PIP
        
    def detect_hands(self, image: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        Detecta manos y cuenta dedos levantados
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Tuple con imagen procesada y cantidad de dedos
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        finger_count = 0
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar landmarks
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                
                # Contar dedos
                finger_count = self._count_fingers(hand_landmarks, image.shape)
                
                # Dibujar información
                self._draw_finger_info(image, hand_landmarks, finger_count)
        
        return image, finger_count
    
    def _count_fingers(self, landmarks, image_shape: Tuple[int, int, int]) -> int:
        """Cuenta los dedos levantados"""
        fingers = []
        h, w, _ = image_shape
        
        # Convertir landmarks normalizados a coordenadas de píxeles
        points = []
        for lm in landmarks.landmark:
            x, y = int(lm.x * w), int(lm.y * h)
            points.append([x, y])
        
        # Pulgar (comparar con landmark 3)
        if points[self.finger_tips[0]][0] > points[self.finger_tips[0] - 1][0]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Otros dedos (comparar punta con articulación PIP)
        for i in range(1, 5):
            if points[self.finger_tips[i]][1] < points[self.finger_pips[i]][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers.count(1)
    
    def _draw_finger_info(self, image: np.ndarray, landmarks, finger_count: int):
        """Dibuja información adicional en la imagen"""
        h, w, _ = image.shape
        
        # Dibujar contador de dedos
        cv2.putText(
            image, f'Dedos: {finger_count}', 
            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
            2, (0, 255, 0), 3
        )
        
        # Dibujar puntos de las puntas de dedos
        for tip_id in self.finger_tips:
            x = int(landmarks.landmark[tip_id].x * w)
            y = int(landmarks.landmark[tip_id].y * h)
            cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
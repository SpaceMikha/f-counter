import cv2

print("Probando índices de cámara...")

for i in range(5):
    print(f"\nProbando índice {i}:")
    cap = cv2.VideoCapture(i)
    
    if cap.isOpened():
        print(f" Cámara detectada en índice {i}")
        
        # Intentar leer un frame
        ret, frame = cap.read()
        if ret:
            print(f"Puede capturar video correctamente")
            print(f"Resolución: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print(f"No puede capturar video")
        
        cap.release()
    else:
        print(f"No hay cámara en índice {i}")

print("\nTest completado.")
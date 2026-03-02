import cv2
import mediapipe as mp
import serial
import time
import pyttsx3
import threading

# ---------------------------
# FUNCIÓN PARA HABLAR
# ---------------------------
def hablar(texto):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(texto)
        engine.runAndWait()
    threading.Thread(target=run).start()

# ---------------------------
# CONEXIÓN ARDUINO
# ---------------------------
arduino = serial.Serial('COM3', 9600) 
time.sleep(2)

# ---------------------------
# MEDIAPIPE
# ---------------------------
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

estado_anterior = "INDETERMINADO"

# ---------------------------
# ENLACE PRINCIPAL
# ---------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]

        diferencia = knee.y - hip.y

        # RANGOS
        if diferencia > 0.20:
            estado = "PARADO"
        elif diferencia < 0.10:
            estado = "SENTADO"
        else:
            estado = estado_anterior #MANTIENE EL ESTADO SI NO ES CLARO

        # SOLO SI CAMBIA
        if estado != estado_anterior:

            if estado == "PARADO":
                arduino.write(b'P')
                hablar("Persona parada")

            elif estado == "SENTADO":
                arduino.write(b'S')
                hablar("Persona sentada")

            estado_anterior = estado

        cv2.putText(frame, estado, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Pose Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
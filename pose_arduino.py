import cv2
import mediapipe as mp
import serial
import time
import pyttsx3

# Inicializar voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Conectar Arduino 
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

estado_anterior = ""

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

        if knee.y - hip.y > 0.15:
            estado = "PARADO"
            comando = b'P'
        else:
            estado = "SENTADO"
            comando = b'S'

        if estado != estado_anterior:
            arduino.write(comando)
            engine.say(estado)
            engine.runAndWait()
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
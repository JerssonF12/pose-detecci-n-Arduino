# Pose Landmark Detection - Arduino
Sistema de detección de postura con MediaPipe y Arduino

## Explicación del código
El sistema se basa en el uso de la librería MediaPipe Pose, la cual permite detectar puntos clave del cuerpo humano mediante modelos de aprendizaje automático. Se emplean los puntos anatómicos de la cadera (hip) y la rodilla (knee) para determinar la postura.
La condición utilizada fue:

kneey − hipy > 0,15
Si la diferencia es mayor al umbral definido, el sistema interpreta que la persona está de pie; de lo contrario, se considera que está sentada.

## Descripción del trabajo

El trabajo implementa un sistema de detección de postura corporal utilizando visión artificial en tiempo real mediante Python y MediaPipe. 

El sistema identifica si una persona está:
- De pie
- Sentada

Cuando detecta un cambio de estado:
- Envía un carácter por comunicación serial al Arduino
- Activa un mensaje de voz indicando el estado actual

---

## Aplicaciones y repositorios Utilizados

- Python 3.11.x
- OpenCV
- MediaPipe
- PySerial
- pyttsx3 (adicional implementando voz)
- Arduino

---

## Funcionamiento del Sistema

1. Se captura video desde la cámara web.
2. MediaPipe detecta los puntos clave del cuerpo.
3. Se analizan las coordenadas de la cadera y la rodilla.
4. Se aplica la condición:
   knee.y - hip.y > 0.15
5. Si la condición se cumple → Estado: PARADO
6. Si no se cumple → Estado: SENTADO
7. Se envía:
   - 'P' al Arduino para parado
   - 'S' al Arduino para sentado
8. Se activa un mensaje de voz únicamente si hay cambio de estado.

---

## Pruebas Realizadas

Durante las pruebas se verificó:

- Correcta detección en tiempo real. (ver video Pruebas.mp4)
- Comunicación serial estable.
- No repetición innecesaria de mensajes de voz.
- Funcionamiento correcto bajo iluminación adecuada.(ver video Pruebas.mp4 o imagenes adjuntas)

El sistema respondió correctamente en múltiples pruebas consecutivas.
---

## Creado por:

Jersson Farid Jimenez Galindo

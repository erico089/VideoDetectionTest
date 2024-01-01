import cv2
import threading

### Pip install list ###
# pip install -q imageio
# pip install -q opencv-python
# pip install -q git+https://github.com/tensorflow/docs

# Inicializa la captura de video
cap = cv2.VideoCapture(0)

# Frontal face
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Mode controller
mode = 0

def switch(frame):
    global mode
    if mode == 0:
        if animationController:
            showRectangle(frame,"NO MODEL")
    elif mode == 1:
        cv2FaceDetector(frame)
        if animationController:
            showRectangle(frame,"CV2 FF")

# Show rectangle controller
animationController = False

# Animation functions
def stopAnimation():
    global animationController
    animationController = False

def startAnimation():
    temporizador = threading.Timer(3.0, stopAnimation)
    temporizador.start()

# rectangle show function
def showRectangle(frame, message) :
    _, width = frame.shape[:2]

    topLeftCorner = (width - 10, 10)
    bottomRightCorner = (width - 120, 40)
    textPosition = (width - 119,30)

    cv2.rectangle(frame, topLeftCorner, bottomRightCorner, (0, 31, 63), -1)
    cv2.putText(frame, message, textPosition, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# Frontal face detector using cv2
def cv2FaceDetector(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se puede recibir el frame (stream end?). Exiting ...")
        break

    ### Drawing control ###
    height, width = frame.shape[:2]

    if cv2.waitKey(1) == ord("0") and not animationController:
        animationController = True
        mode = 0
        startAnimation()

    if cv2.waitKey(1) == ord("1") and not animationController:
        animationController = True
        mode = 1
        startAnimation()

    # Switch mode controller
    switch(frame)

    cv2.imshow('Frame', frame)

    ### Close control ###
    if cv2.waitKey(1) == 27 or cv2.waitKey(1) in [10, 13]:
        break

# Cuando todo esté hecho, libera la captura
cap.release()
cv2.destroyAllWindows()

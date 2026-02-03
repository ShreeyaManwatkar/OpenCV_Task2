"""
Member1 - Open cv & Camera Handling
This file prvide  base for:
. Webcam access using OpenCV
. Frame processing (resize, flip)
. Face detection using Haar Cascade
. Drawing bounding boxes
Camera Usage:
Run the file and press 'q' to exit.
"""

import cv2

# Loading face detection model
face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

# Starting webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

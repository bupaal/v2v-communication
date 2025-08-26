from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import cv2
import time
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("E:\Comms project\comms-project-27524-firebase-adminsdk-fbsvc-dd4b61ef3f.json")  # Replace with your actual JSON file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://comms-project-27524-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace with your Firebase Database URL
})

def send_alert_to_firebase(car_id, message):
    ref = db.reference(f"alerts/{car_id}")
    
    # Get the last message from Firebase
    last_message = ref.get()

    # Update only if the message is different
    if not last_message or last_message.get("message") != message:
        ref.set({"message": message})
        print(f"Alert sent to Firebase: {car_id} - {message}")

# Initialize Pygame sound
mixer.init()
mixer.music.load("E:\Comms project\music.wav")

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

thresh = 0.25  # Eye aspect ratio threshold
frame_check = 20  # Frames required to trigger alert
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("E:\Comms project\shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

cap = cv2.VideoCapture(0)
flag = 0
last_sent_message = ""  # To store the last sent message

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)

    drowsy_detected = False  # Track if drowsiness is detected

    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < thresh:
            flag += 1
            if flag >= frame_check:
                drowsy_detected = True
                cv2.putText(frame, "ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                mixer.music.play()

        else:
            flag = 0  # Reset flag if eyes are open

    # Update Firebase with drowsiness status
    if drowsy_detected:
        message = "Drowsiness Detected!"
    else:
        message = "Driver Awake"

    if message != last_sent_message:
        send_alert_to_firebase("Car_A", message)
        last_sent_message = message  # Store last sent message to avoid duplicates

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
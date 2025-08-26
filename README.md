# 🚗 Drowsiness Detection & Alert System (Python + Arduino + Firebase)

This project is a **real-time drowsiness detection system** using computer vision and machine learning.  
It detects driver fatigue by monitoring eye landmarks, sends alerts via **Arduino**, and logs data to **Firebase**.

---

## 📌 Features
- Face & eye detection using **dlib** and **OpenCV**.
- 68-point facial landmark detection.
- Real-time drowsiness alert via **Arduino buzzer**.
- Cloud data logging with **Firebase**.
- Works with webcam or external camera.

---

## 📂 Required Files
Make sure you have these files before running:

1. **Facial Landmark Model (68 points)**  
   - [Download shape_predictor_68_face_landmarks.dat](https://huggingface.co/matt3ounstable/dlib_predictor_recognition/resolve/main/shape_predictor_68_face_landmarks.dat)

2. **Haarcascade Models (Face & Eyes)**  
   - [haarcascade_frontalface_default.xml]
   - [haarcascade_eye.xml]

Or download them from your repo’s `models/` folder if uploaded.

---

## ⚙️ Installation


### 🔹 Arduino Setup

* Use an **Arduino Uno/Nano** with a buzzer or relay module.
* Upload the provided `arduino_alert.ino` code from this repo to your Arduino using Arduino IDE.
* Connect Arduino via USB for serial communication.

---

## ▶️ Usage

```bash
python drowsiness_detection.py
```

* The system captures video from webcam.
* If eyes remain closed beyond a threshold → **Alert is triggered**.
* An alert is sent to **Arduino** → buzzer/alarm sounds.
* Detection data is uploaded to **Firebase**.

---

## 🔗 Firebase Setup

1. Create a **Firebase project**.
2. Download the `serviceAccountKey.json` file.
3. Place it in your project root.
4. Configure `firebase_admin` in your Python script.

---

## 📊 Workflow

1. **Face Detection** → Haarcascade (`.xml` files).
2. **Facial Landmarks** → `shape_predictor_68_face_landmarks.dat`.
3. **Eye Aspect Ratio (EAR)** → Determines drowsiness.
4. **Alert Trigger** → Arduino buzzer + Firebase log.

---

## 📷 System Architecture

```
[ Webcam ] → [ Python (OpenCV + dlib) ] → [ Drowsiness Detection ] 
      → [ Alert Signal → Arduino ] 
      → [ Log Data → Firebase ]
```

---

## ⚠️ Alert Levels

* **Level 1:** Eyes closed briefly → Warning.
* **Level 2:** Eyes closed continuously → Arduino buzzer ON + Firebase Alert.

---



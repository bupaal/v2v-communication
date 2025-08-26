# 🚗 Drowsiness Detection & Alert System (Python + Arduino + Firebase)


This project integrates **Python (OpenCV + Dlib)**, **Arduino**, and **Firebase** to enhance road safety by detecting driver drowsiness and monitoring vehicles.

## 🚗 Features
- **Face and Eye Detection**  
  Uses OpenCV Haarcascade classifiers (`haarcascade_frontalface_default.xml`, `haarcascade_eye.xml`) and Dlib’s `shape_predictor_68_face_landmarks.dat` for real-time detection.
  
- **Drowsiness Detection**  
  Calculates **Eye Aspect Ratio (EAR)** to identify prolonged eye closure, signaling possible drowsiness.

- **Alert System**  
  - Triggers a buzzer/alarm via Arduino.  
  - Sends warning notifications to **Firebase**.

- **Multiple Vehicle Detection**  
  Detects multiple vehicles in camera view and flags risky driver behavior.

- **Firebase Integration**  
  Uploads driver status (**Normal / Drowsy / Alert**) to Firebase Realtime Database for cloud-based monitoring.



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



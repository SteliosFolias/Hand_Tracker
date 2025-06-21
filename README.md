# Hand_Tracker
Hand Cursor Control is a lightweight Python application that runs in the background on Windows and uses your webcam to track your hand. It moves the mouse cursor based on your index finger and supports stable, gesture-based left and right clicks without a graphical interface. It's built using OpenCV, MediaPipe, and PyAutoGUI.

# 🖐️ Hand Cursor Control (No GUI)

Control your mouse cursor using your hand gestures via your webcam — no GUI, just a background service!

## 🔧 Features

- Move your mouse with your **index finger**.
- Perform a **left click** by pinching your **thumb and index finger** for ~0.3s.
- Perform a **right click** by pinching your **thumb and middle finger** for ~0.3s.
- Cursor movement is **smoothed** to avoid jitter.
- **Failsafe-free**, safe for edge-of-screen usage.
- Runs silently in the background (console-free mode possible).

## 🛠️ Requirements

- Python 3.10 or later  
- Webcam

Install dependencies:

```bash
pip install opencv-python mediapipe pyautogui

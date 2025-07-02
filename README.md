# Hand Gesture Mouse Controller

Control your mouse using just your hand via webcam, powered by OpenCV, MediaPipe, and PyAutoGUI.

### ✨ Features
- 🖱️ **Move the mouse** with your hand
- 👍 **Left-click** with a "thumbs-down" gesture (thumb down, all other fingers up)
- 🧊 **Smoothed cursor movement** to avoid jitter
- 🧱 **Failsafe-free**: works near screen edges without interruptions
- 🕶️ **Silent background operation** (console-free mode possible)

### 🛠️ Requirements
- OpenCV
- MediaPipe
- PyAutoGUI
- Python 3.9.13  (https://www.python.org/downloads/windows/) and check the option “Add Python to PATH” during installation.
- Webcam

Install dependencies:
```bash
pip install opencv-python mediapipe pyautogui
py -m pip install pyinstaller
pyinstaller hand_tracker.spec
```




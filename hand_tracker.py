import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

# Settings
click_delay = 0.6  # delay between allowed clicks
gesture_hold_time = 0.3  # how long gesture must persist
move_threshold = 25  # pixels to ignore small hand shakes

# State
prev_x, prev_y = None, None
last_left_click = 0
last_right_click = 0
gesture_start_time = None
gesture_type = None  # 'left' or 'right'

def get_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

try:
    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            lm = hand.landmark

            index_tip = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = lm[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = lm[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            now = time.time()

            dist_index_thumb = get_distance(index_tip, thumb_tip)
            dist_middle_thumb = get_distance(middle_tip, thumb_tip)

            # Check for gesture
            new_gesture = None
            if dist_index_thumb < 0.045:
                new_gesture = 'left'
            elif dist_middle_thumb < 0.045:
                new_gesture = 'right'

            # Handle gesture hold
            if new_gesture:
                if gesture_type != new_gesture:
                    gesture_type = new_gesture
                    gesture_start_time = now
                elif now - gesture_start_time >= gesture_hold_time:
                    if new_gesture == 'left' and now - last_left_click >= click_delay:
                        pyautogui.click(button='left')
                        last_left_click = now
                        gesture_type = None  # reset
                    elif new_gesture == 'right' and now - last_right_click >= click_delay:
                        pyautogui.click(button='right')
                        last_right_click = now
                        gesture_type = None  # reset
            else:
                gesture_type = None
                gesture_start_time = None

            # Only move mouse if not trying to click
            if gesture_type is None:
                cx = int(index_tip.x * screen_w)
                cy = int(index_tip.y * screen_h)

                if prev_x is None or abs(cx - prev_x) > move_threshold or abs(cy - prev_y) > move_threshold:
                    pyautogui.moveTo(cx, cy)
                    prev_x, prev_y = cx, cy

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()

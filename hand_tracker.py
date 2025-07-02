import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

if not cap.isOpened():   
  print("Error: Could not open camera")  
  exit() 
else:     
  print("camera connected")
  
# Settings
click_delay = 0.3
move_threshold = 28          # <--- Consider increasing this value further
gesture_hold_time = 0.3

# State
prev_x, prev_y = None, None
last_left_click = 0
gesture_start_time = None
gesture_active = False

def finger_is_up(lm, tip_idx, pip_idx):
    return lm[tip_idx].y < lm[pip_idx].y

try:
    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        now = time.time()

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            lm = hand.landmark

            # Check finger states for thumbs-up gesture
            thumb_up = finger_is_up(lm, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP)
            index_up = finger_is_up(lm, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP)
            middle_up = finger_is_up(lm, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP)
            ring_up = finger_is_up(lm, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP)
            pinky_up = finger_is_up(lm, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)

            # Thumbs up gesture: thumb up, all other fingers down
            is_thumbs_up = thumb_up and not (index_up or middle_up or ring_up or pinky_up)

            #is_thumbs_up = thumb_up and not (index_up or middle_up or ring_up or pinky_up)
            is_thumbs_down = (index_up and middle_up and ring_up and pinky_up) and not thumb_up 
            print("is_thumbs_down",is_thumbs_down)
            
            if is_thumbs_down:
                if not gesture_active:
                    gesture_active = True
                    gesture_start_time = now
                else:
                    held_time = now - gesture_start_time
                    if held_time >= gesture_hold_time:
                        if now - last_left_click >= click_delay:
                            pyautogui.click(button='left')
                            last_left_click = now
                            print("Single click!")
            else:
                gesture_active = False
                gesture_start_time = None

            # Move mouse with index finger tip only if no active click gesture
            # This is the crucial part that limits movement when gesture_active is True
            if not gesture_active:
                cx = int(lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screen_w)
                cy = int(lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * screen_h)

                # Only move if the change in position is greater than the threshold
                if prev_x is None or abs(cx - prev_x) > move_threshold or abs(cy - prev_y) > move_threshold:
                    pyautogui.moveTo(cx, cy)
                    prev_x, prev_y = cx, cy

        else:
            # No hand detected, reset everything
            gesture_active = False
            gesture_start_time = None

        # Optional: show frame if you want visual feedback
        # cv2.imshow('Hand Tracking', frame)
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()

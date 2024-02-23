import cv2
import time
import mediapipe as mp 
import numpy as np
from detectActions import detectAction
from collections import deque
import pyautogui
from screeninfo import get_monitors
pyautogui.FAILSAFE = False

global scr_resolution 
global pointer_resolution
pointer_resolution = (1184, 688)
scr_resolution = (get_monitors()[0].width, get_monitors()[0].height)
print("DEBUG:",scr_resolution)
class clear_alert_cache():

    def check_clear(self,status):

        if self.len1 == 300:
            self.cache_clear.popleft()
            self.len1 -= 1

        self.cache_clear.append(status)            
        self.len1 += 1
        
        return all(self.cache_clear)

    def update_cache(self,clear_status):
        
        ret = []
        
        clear_seq_current = self.check_clear(clear_status)

        if clear_seq_current and (not self.prev_bent):
            ret.append('clear')

        self.prev_bent = clear_seq_current

        return ret

    def __init__(self):
        self.cache_clear = deque([])
        self.len1 = 0
        self.prev_bent = False

class ExponentialSmoothing:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.smooth_x = None
        self.smooth_y = None

    def update(self, x, y):
        if self.smooth_x is None or self.smooth_y is None:
            # Initialize with the first set of coordinates
            self.smooth_x, self.smooth_y = x, y
        else:
            # Apply exponential smoothing
            self.smooth_x = int(self.alpha * x + (1 - self.alpha) * self.smooth_x)
            self.smooth_y = int(self.alpha * y + (1 - self.alpha) * self.smooth_y)
        
        return self.smooth_x, self.smooth_y
    
smoother = ExponentialSmoothing(alpha=0.3)  # Adjust alpha as needed
global prev_action 
prev_action ="unknown"
def mediapipe_results(frame, pen_color, mpHands, hands, mp_draw):
    global prev_action
    flip = True 
    eraser_size = 100

    frame = cv2.flip(frame, 1) if flip else frame
    h, w, c = frame.shape
    frame = cv2.resize(frame, (w*2, h*2))
    clear_dots = False

    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
            action = detectAction(hand_landmarks, (h*2, w*2))
            pen_color = pen_color
            print("real:",action)
            if action == 'Point':
                smoothed_pos = smoother.update(int(hand_landmarks.landmark[8].x * w * 2),int(hand_landmarks.landmark[8].y * h * 2))
                # index_pos = (int(hand_landmarks.landmark[4].x * w*2), int(hand_landmarks.landmark[4].y * h*2))
                index_pos = smoothed_pos

                # print("DEBUG::::::",index_pos)
                scaled_w = (index_pos[0]/pointer_resolution[0]) * scr_resolution[0]
                scaled_h = (index_pos[1]/pointer_resolution[1]) * scr_resolution[1]
                pyautogui.moveTo(scaled_w, scaled_h)
            elif action == 'Click':
                print("CLICKED")
                print(prev_action)
                if(prev_action!='Click'):
                    pyautogui.click()
            elif action =='ScrollUp':
                pyautogui.scroll(-100)
            elif action =='ScrollDown':
                pyautogui.scroll(100)
            
            prev_action = action

    return frame

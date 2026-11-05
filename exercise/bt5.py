#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, vẽ màu tím cho ngón trỏ
#Hiển thị video kết quả lên màn hình
#điều khiển chuột máy tính bằng ngón trỏ
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = False,max_num_hands = 1)
mp_draw = mp.solutions.drawing_utils
screen_w,screen_h = pyautogui.size()
pyautogui.FAILSAFE = False
while True:
    ret, frame = cap.read()
    if not ret:
        print('Error')
        break
    frame = cv2.flip(frame, 1)
    h,w = frame.shape[:2]
    nframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(nframe)
    kq = result.multi_hand_landmarks
    if kq:
        for hand_landmarks in kq:
            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            lm8 = hand_landmarks.landmark[8]
            lm8x,lm8y = int(lm8.x*w),int(lm8.y*h)
            cv2.circle(frame,(lm8x,lm8y),10,(0,255,0),-1)
            screen_x = int(np.interp(lm8x,[0,w],[0,screen_w]))
            screen_y = int(np.interp(lm8y,[0,h],[0,screen_h]))
            pyautogui.moveTo(screen_x,screen_y,duration=0.05)
    cv2.imshow('webCam',frame)
    if cv2.waitKey(1)== ord('q'):
        break
cv2.destroyAllWindows()


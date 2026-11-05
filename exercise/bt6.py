#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, vẽ màu tím cho ngón trỏ và ngón cái
#In fps web cam góc dưới phải
#điều khiển chuột máy tính bằng ngón trỏ
#click chuột khi ngón trỏ chạm ngón cái, trong khi click thì không di chuyển chuột
#Hiển thị video kết quả lên màn hình
import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = False, max_num_hands = 1)
mp_draw = mp.solutions.drawing_utils
screen_w,screen_h = pyautogui.size()
pyautogui.FAILSAFE = False
time_clicks = 0
fps = cap.get(5)
while True:
    ret, frame = cap.read()
    if not ret:
        print('Error')
        break
    frame = cv2.flip(frame,1)
    h,w = frame.shape[:2]
    nframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(nframe)
    kq = result.multi_hand_landmarks
    if kq:
        for hand_landmarks in kq:
            for hand_landmarks in kq:
                mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                lm4 = hand_landmarks.landmark[4]
                lm8 = hand_landmarks.landmark[8]
                lm4x,lm4y = int(lm4.x*w), int(lm4.y*h)
                lm8x,lm8y = int(lm8.x*w), int(lm8.y*h)
                cv2.circle(frame, (lm4x,lm4y),5,(0,255,0),-1)
                cv2.circle(frame, (lm8x,lm8y),5,(0,255,0),-1)
                cv2.line(frame,(lm4x,lm4y),(lm8x,lm8y),(0,255,0),2)
                dist = ((lm8x - lm4x)**2+(lm8y-lm4y)**2)**0.5
                if dist < 30:
                    if time.time() - time_clicks > 0.5:
                        pyautogui.click()
                        print('click')
                        time_clicks = time.time()
                screen_x = int(np.interp(lm8x,[0,w],[0,screen_w]))
                screen_y = int(np.interp(lm8y,[0,h],[0,screen_h]))
                pyautogui.moveTo(screen_x,screen_y,duration=0.05)
                cv2.imshow('webcam',frame)
        if cv2.waitKey(1) == ord('q'):
            break
cv2.putText(frame,f'fps:{fps}',({screen_h-150},{screen_w-50}),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
cv2.destroyAllWindows()
                    
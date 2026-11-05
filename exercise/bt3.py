#Đọc ảnh bằng OpenCV
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, 
#vẽ hình tròn và in ra tọa độ của ngón trỏ và ngón cái
#Hiển thị kết quả lên màn hình
import cv2
import mediapipe as mp
img = cv2.imread(r"D:\pythonTH\Virtual_mouse\tay.jpg")
mp_hands = mp.solutions.hands
h,w = img.shape[:2]
hands = mp_hands.Hands(static_image_mode = True, max_num_hands = 2)
mp_draw = mp.solutions.drawing_utils
rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
result = hands.process(rgb)
kq = result.multi_hand_landmarks
if kq:
    for hand_landmarks in kq:
        mp_draw.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS)
        lm4 = hand_landmarks.landmark[4]
        lm8 = hand_landmarks.landmark[8]
        lm4x,lm4y = int(lm4.x*w), int(lm4.y*h)
        lm8x,lm8y = int(lm8.x*w), int(lm8.y*h)
        cv2.circle(img,(lm4x,lm4y),10,(0,255,1),-1)
        cv2.circle(img,(lm8x,lm8y),10,(0,255,1),-1)
cv2.imshow('tay',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

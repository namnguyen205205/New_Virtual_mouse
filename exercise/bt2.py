#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh
#Hiển thị video kết quả lên màn hình
import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = False, max_num_hands = 2)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame,1)
    nframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(nframe)
    kq = result.multi_hand_landmarks
    if kq:
        for hand_landmarks in kq:
            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
    cv2.imshow('tay',frame)
    if cv2.waitKey(10) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
img = cv2.imread(r'D:\pythonTH\Virtual_mouse\tay.jpg')
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = True, max_num_hands = 2)
mp_draw = mp.solutions.drawing_utils
rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
result = hands.process(rgb)
kq = result.multi_hand_landmarks
if kq:
    for hand_landmarks in kq:
        mp_draw.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS)
    print('detect OK')
else:
    print('detect no OK')
cv2.imshow('tay',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
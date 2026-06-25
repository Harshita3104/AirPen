
import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)

# For drawing landmarks
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

prev_x = 0
prev_y = 0

canvas = None

while True:
    success, frame = cap.read()
    
    if canvas is None:
        canvas = frame.copy()
        canvas[:] = 0

    if not success:
        break

    # Mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            ring_up = landmarks[16].y < landmarks[14].y
            index_up = landmarks[8].y < landmarks[6].y
            middle_up = landmarks[12].y < landmarks[10].y
            
            if index_up and middle_up and ring_up:
                canvas[:] = 0
                prev_x = 0
                prev_y = 0
    
            if index_up:
                cv2.putText(
                    frame,
                    "INDEX UP",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            h, w, c = frame.shape

            index_tip = hand_landmarks.landmark[8]

            cx = int(index_tip.x * w)
            cy = int(index_tip.y * h)

            print(cx, cy)
        
            if index_up and not middle_up:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = cx, cy

                cv2.line(canvas,
                    (prev_x, prev_y),
                    (cx, cy),
                    (0, 255, 0),
                    5)

                prev_x, prev_y = cx, cy
        
            elif index_up and middle_up:
                prev_x = 0
                prev_y = 0

    frame = cv2.add(frame, canvas)
    
    cv2.imshow("Hand Tracking", frame)

    key=cv2.waitKey(1) & 0xFF 
    
    if key == ord('s'):
        cv2.imwrite("writing.png", canvas)
        print("Saved!")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
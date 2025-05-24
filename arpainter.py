import cv2 as cv
import mediapipe as mp
import numpy as np

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

vdo = cv.VideoCapture(0)

tips = [8, 12, 16, 20]  # Fingertips for detection
draw_points = []
prev_point = None

# Default drawing settings
current_color = (255, 0, 0)  # Start with blue
line_thickness = 5  # Default thickness

font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2

while True:
    success, img = vdo.read()
    flipped = cv.flip(img, 1)
    imgRGB = cv.cvtColor(flipped, cv.COLOR_BGR2RGB)
    flipped1 = flipped.copy()
    result = hands.process(imgRGB)

    points = []
    fingers_up = []
    h, w, c = img.shape

    # Color selection and thickness control positions (spaced equally at the top)
    redpos = (int(h/5), 50)
    bluepos = (int(2*(h/5)), 50)
    greenpos = (int(3*(h/5)), 50)
    pluspos = (int(4*(h/5)+50), 50)  # "+" for increasing thickness
    minuspos = (int(5*(h/5)+50), 50)  # "-" for decreasing thickness

    if result.multi_hand_landmarks:
        for hndlm in result.multi_hand_landmarks:
            single_handp = []
            for id1, lm in enumerate(hndlm.landmark):
                x = int(lm.x * w)
                y = int(lm.y * h)
                single_handp.append([id1, x, y])
            points = single_handp
            mpDraw.draw_landmarks(flipped, hndlm, mpHands.HAND_CONNECTIONS)

    if points:
        index_finger_tip = (points[8][1], points[8][2])

        # Check proximity to color positions
        def is_near(point1, point2, threshold=40):
            return abs(point1[0] - point2[0]) < threshold and abs(point1[1] - point2[1]) < threshold

        if is_near(index_finger_tip, redpos):
            current_color = (0, 0, 255)  # Red
        elif is_near(index_finger_tip, bluepos):
            current_color = (255, 0, 0)  # Blue
        elif is_near(index_finger_tip, greenpos):
            current_color = (0, 255, 0)  # Green

        # Adjust line thickness based on fingertip position
        if is_near(index_finger_tip, pluspos):
            line_thickness += 1 if line_thickness < 20 else 0  # Max thickness capped
        elif is_near(index_finger_tip, minuspos):
            line_thickness -= 1 if line_thickness > 1 else 0  # Min thickness capped

        # Drawing logic
        for tip in tips:
            if points[tip][2] < points[tip - 2][2]:  # Check if finger is raised
                fingers_up.append(1)
            else:
                fingers_up.append(0)

        if fingers_up == [1, 0, 0, 0]:  # Index finger up
            current_point = (points[8][1], points[8][2])
            if prev_point:
                draw_points.append((prev_point, current_point, current_color, line_thickness))
            prev_point = current_point
        elif fingers_up == [0, 0, 0, 0]:  # All fingers down (erase)
            draw_points = []
            prev_point = None
        else:
            prev_point = None

        for pt1, pt2, clr, thick in draw_points:
            cv.line(flipped1, pt1, pt2, clr, thick)

    # Blend original and drawn images
    op = cv.addWeighted(flipped, 0.5, flipped1, 0.5, 0)

    # Display color selection and thickness control at the top
    cv.putText(op, "RED", redpos, font, font_scale, (0, 0, 255), thickness)
    cv.putText(op, "BLUE", bluepos, font, font_scale, (255, 0, 0), thickness)
    cv.putText(op, "GREEN", greenpos, font, font_scale, (0, 255, 0), thickness)
    cv.putText(op, "+", pluspos, font, font_scale, (255, 255, 255), thickness)
    cv.putText(op, "-", minuspos, font, font_scale, (255, 255, 255), thickness)


    cv.imshow("Final Output", op)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vdo.release()
cv.destroyAllWindows()

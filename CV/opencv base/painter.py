import cv2
import time
import numpy as np
import os
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

drawColor = (255, 0, 255)
colorDict = {0:(0, 255,0),1:(0, 100,255)}
brushThickness=10
img_shape=(1920,886,3),(720, 1280, 3),(1080,1920, 3),(1920,1080, 3)


def run_static():
    # For static images:
    IMAGE_FILES = []
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
      for idx, file in enumerate(IMAGE_FILES):
        # Read an image, flip it around y-axis for correct handedness output (see
        # above).
        image = cv2.flip(cv2.imread(file), 1)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        print('Handedness:', results.multi_handedness)
        if not results.multi_hand_landmarks:
          continue
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
          print('hand_landmarks:', hand_landmarks)
          print(
              f'Index finger tip coordinates: (',
              f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
              f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
          )
          mp_drawing.draw_landmarks(
              annotated_image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
        cv2.imwrite(
            '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
        # Draw hand world landmarks.
        if not results.multi_hand_world_landmarks:
          continue
        for hand_world_landmarks in results.multi_hand_world_landmarks:
          mp_drawing.plot_landmarks(
            hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)


def run_webcam():
    # For webcam input:
    video_path = './RPReplay_Final1656813938.MP4'
    # cap = cv2.VideoCapture(video_path)
    # ip_camera='http://admin:admin@192.168.1.4:8081'
    # cap = cv2.VideoCapture(ip_camera)
    cap = cv2.VideoCapture(0)
    init_canvas= np.zeros(img_shape[1],np.uint8)
    img_canvas = {0:init_canvas.copy(), 1:init_canvas.copy()}
    loc_prev = {0:(0,0),1:(0,0)}
    current_loc = {0:(0,0), 1:(0,0)}
    hand_idx=0
    # cap = cv2.VideoCapture(0)
    with mp_hands.Hands(model_complexity=1,min_detection_confidence=0.8,min_tracking_confidence=0.2) as hands:
        while cap.isOpened():
            # fps = cap.get(cv2.CAP_PROP_FPS)
            # print(fps)
            success, image = cap.read()
            pressedKey = cv2.waitKey(5) & 0xFF # ref:https://www.pudn.com/news/62a1b9f285c2c25613112c88.html
            if pressedKey== ord('c'):

                img_canvas = {0:init_canvas, 1:init_canvas}
            else:
                pass
            # if pressedKey & 0xFF == 27:
            #     break
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue


            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            hand_marks = results.multi_hand_landmarks

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            h,w,c = image.shape
            if hand_marks:
                hand_num = len(hand_marks)
                if hand_num==2:
                    a,b = hand_marks
                    try:
                        hand_marks = [a,b] if a.landmark[0].x < b.landmark[0].x else [b,a]
                    except AttributeError:
                        pass
                for idx,hand_landmark in enumerate(hand_marks):
                    mp_drawing.draw_landmarks(
                    image,
                    hand_landmark,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                    # Flip the image horizontally for a selfie-view display.
                    lm = hand_landmark.landmark[8]
                    plam = hand_landmark.landmark[0]
                    current_loc[idx] = int(lm.x * w), int(lm.y * h)
                    # if plam.x*w<=400 and hand_num==1:  # two hands restriction use
                    #     # current_loc[idx] = (0,0)
                    #     idx=0
                    # if plam.x*w>=400 and hand_num==1:
                    #     # current_loc[idx] = (0,0)
                    #     idx=1
                    print(loc_prev[idx],current_loc[idx])
                    if loc_prev[idx][0] == 0 and loc_prev[idx][1] == 0:
                      loc_prev[idx] = current_loc[idx]
                    # cv2.line(image, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(img_canvas[idx], loc_prev[idx], current_loc[idx], colorDict[idx], brushThickness)
                    loc_prev[idx] = current_loc[idx]
            # imgGray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
            # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            # imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            # image = cv2.bitwise_and(image, imgInv)
            # image = cv2.bitwise_or(image, img_canvas)
            img_canvas_both = img_canvas[0] + img_canvas[1]  # TODO test; may error in the future?
            alpha = 0.5
            img_final = cv2.addWeighted(src1=image, alpha=alpha, src2=img_canvas_both,beta=1-alpha,gamma=0)
            # cv2.imshow("Image", img_final)
            # cv2.imshow("Image", image)
            # cv2.imshow("Canvas", img_canvas_both)
            # cv2.imshow("canvas0", img_canvas[0])
            # cv2.imshow("canvas1", img_canvas[1])
            cv2.imshow('MediaPipe Hands', cv2.flip(img_final, 1))
            # cv2.imshow('MediaPipe Hands', image)
    cap.release()


run_webcam()
"""
reading list:
1. OpenCV&Python 编程中对此语句的理解：if cv2.waitKey(25) & 0xFF == 27: https://zhuanlan.zhihu.com/p/38443324
"""

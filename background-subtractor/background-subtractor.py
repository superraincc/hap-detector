import cv2
import heapq

vedio = r'.\data\hap-small-2.mp4'
videoroute = r'.\output'

cap = cv2.VideoCapture(vedio)

# 提高history, 提高var可以减弱闪烁效应
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

cv2.namedWindow('frame', 0)
cv2.resizeWindow('frame', 576*2, 324*2)
cv2.namedWindow('fgmask', 0)
cv2.resizeWindow('fgmask', 576*2, 324*2)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    fgmask = fgbg.apply(frame)
    fgmask = cv2.erode(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=1)
    fgmask = cv2.dilate(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=2)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0))

    # contours_square = []
    # for c in contours:
    #     contours_square.append(cv2.contourArea(c))
    # contours_index = heapq.nlargest(10, contours_square)
    contours = [c for c in contours if cv2.contourArea(c) > 10]
    for c in contours:
        if len(contours) < 50:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)



    cv2.imshow('frame', frame)
    cv2.imshow('fgmask', fgmask)



    key = cv2.waitKey(20) & 0xff
    if key == 27:
        break

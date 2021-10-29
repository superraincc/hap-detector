import cv2
from detector import Detector

video = r'.\data\hap-big.mp4'
videoroute = r'.\output'

cap = cv2.VideoCapture(video)

detector = Detector()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    _, _, fgmask = detector.apply(frame)

    cv2.imshow('frame', frame)
    cv2.imshow('fgmask', fgmask)
    cv2.waitKey(20)

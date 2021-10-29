import cv2

vedio = r'D:\mint-src\hap-detector\data\hap-small-2.mp4'
# videoroute = r'D:\000AAA MINT\SCDX\HAP\HAP-output-MOG2\HAP-big\out.avi'

cap = cv2.VideoCapture(vedio)

cv2.namedWindow('frame', 0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.resizeWindow('frame', 576*2, 324*2)
    cv2.imshow('frame', frame)

    cv2.waitKey(20)

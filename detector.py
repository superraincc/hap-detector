import numpy as np
import cv2

class Detector(object):

    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=800, varThreshold=100, detectShadows=False)

    def apply(self, frame):
        # 背景模型中添加帧
        fgmask = self.fgbg.apply(frame, learningRate=0.1)

        # 图像腐蚀和膨胀操作
        fgmask = cv2.erode(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=1)
        fgmask = cv2.dilate(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=2)

        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (0, 255, 0))

        contours = [c for c in contours if cv2.contourArea(c) > 10]

        centers = []
        for c in contours:
            if len(contours) < 100:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # centers.append(np.round(np.array([[x], [y]])))
                centers.append([[x], [y]])

        return centers, frame, fgmask

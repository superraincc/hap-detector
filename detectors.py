'''
    File name         : detectors.py
    File Description  : Detect objects in video frame
    Author            : Srini Ananthakrishnan
    Date created      : 07/14/2017
    Date last modified: 07/16/2017
    Python Version    : 2.7
'''

# Import python libraries
import numpy as np
import cv2

# set to 1 for pipeline images
debug = 0


class Detectors(object):
    """Detectors class to detect objects in video frame
    Attributes:
        None
    """
    def __init__(self):
        """Initialize variables used by Detectors class
        Args:
            None
        Return:
            None
        """
        self.fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)

    def Detect(self, frame):
        """Detect objects in video frame using following pipeline
            - Convert captured frame from BGR to GRAY
            - Perform Background Subtraction
            - Detect edges using Canny Edge Detection
              http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
            - Retain only edges within the threshold
            - Find contours
            - Find centroids for each valid contours
        Args:
            frame: single video frame
        Return:
            centers: vector of object centroids in a frame
        """

        # Convert BGR to GRAY
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if (debug == 1):
            cv2.imshow('gray', gray)

        # Perform Background Subtraction
        fgmask = self.fgbg.apply(gray)

        # 图像腐蚀和膨胀操作
        fgmask = cv2.erode(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)), iterations=4)
        fgmask = cv2.dilate(fgmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        
        cv2.namedWindow('fgmask', 0)
        cv2.resizeWindow('fgmask', int(576*1.5), int(324*1.5))

        if (debug == 0):
            cv2.imshow('fgmask', fgmask)

        # Detect edges
        # edges = cv2.Canny(fgmask, 50, 190, 3)

        # if (debug == 1):
            # cv2.imshow('Edges', edges)

        # Retain only edges within the threshold
        # ret, thresh = cv2.threshold(edges, 127, 255, 0)

        # Find contours
        # _, contours, hierarchy = cv2.findContours(thresh,
        #                                           cv2.RETR_EXTERNAL,
        #                                           cv2.CHAIN_APPROX_SIMPLE)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bounds = [cv2.boundingRect(c) for c in contours if 10 < cv2.contourArea(c) < 1000]

        # if (debug == 0):
            # cv2.imshow('thresh', thresh)

        centers = []  # vector of object centroids in a frame
        # we only care about centroids with size of bug in this example
        # recommended to be tunned based on expected object size for
        # improved performance
        blob_radius_thresh = 8
        # Find centroid for each valid contours
        for cnt in bounds:
            try:
                x, y, w, h = cnt
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                b = np.array([[x], [y]])
                centers.append(np.round(b))

                # Calculate and draw circle
                # (x, y), radius = cv2.minEnclosingCircle(cnt)
                # centeroid = (int(x), int(y))
                # radius = int(radius)
                # if (radius > blob_radius_thresh):
                #     cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                #     b = np.array([[x], [y]])
                #     centers.append(np.round(b))
            except ZeroDivisionError:
                pass

        # show contours of tracking objects
        # cv2.imshow('Track Bugs', frame)

        return centers

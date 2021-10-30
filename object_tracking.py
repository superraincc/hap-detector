'''
    File name         : object_tracking.py
    File Description  : Multi Object Tracker Using Kalman Filter
                        and Hungarian Algorithm
    Author            : Srini Ananthakrishnan
    Date created      : 07/14/2017
    Date last modified: 07/16/2017
    Python Version    : 2.7
'''

# Import python libraries
import cv2
import copy
from detector import Detector
from tracker import Tracker

vedio = r'D:\000AAA MINT\SCDX\HAP\HAP-small.mp4'
videoroute = r'D:\000AAA MINT\SCDX\HAP\HAP-output-MOG2\HAP-big\out.avi'

# 超过这一下落高度，则报警为高空抛物事件
hap_Threshold = 500

def main():
    """Main function for multi object tracking
    Usage:
        $ python2.7 objectTracking.py
    Pre-requisite:
        - Python2.7
        - Numpy
        - SciPy
        - Opencv 3.0 for Python
    Args:
        None
    Return:
        None
    """

    # Create opencv video capture object
    # cap = cv2.VideoCapture('data/TrackingBugs.mp4')
    cap = cv2.VideoCapture(vedio)

    # 用于输出结果
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # decoder
    videoout = cv2.VideoWriter(videoroute, fourcc, fps, (width, height))
    print((width, height))

    # Create Object Detector
    detector = Detector()

    # Create Object Tracker
    tracker = Tracker(dist_thresh=200, max_frames_to_skip=10, max_trace_length=30, trackIdCount=100)

    # Variables initialization
    skip_frame_count = 0
    track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]
    pause = False

    cv2.namedWindow('Tracking', 0)
    cv2.resizeWindow('Tracking', 576*2, 324*2)

    # Infinite loop to process video frames
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Make copy of original frame
        orig_frame = copy.copy(frame)

        # Skip initial frames that display logo
        if (skip_frame_count < 15):
            skip_frame_count += 1
            continue

        # Detect and return centeroids of the objects in the frame
        centers, _, _ = detector.apply(frame)

        # If centroids are detected then track them
        if (len(centers) > 0):

            # Track object using Kalman Filter
            tracker.Update(centers)

            # For identified object tracks draw tracking line
            # Use various colors to indicate different track_id
            for i in range(len(tracker.tracks)):
                # tracks是一个存储跟踪目标对象的数组
                if (len(tracker.tracks[i].trace) > 1):
                    y_array = [tracker.tracks[i].trace[j][1][0] for j in range(len(tracker.tracks[i].trace))]
                    if max(y_array) - min(y_array) > hap_Threshold:
                        print('Warning!!')
                        cv2.putText(frame, 'WARNING!!', (50, 150), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 12)
                        for j in range(len(tracker.tracks[i].trace)-1):
                            # Draw trace line
                            x1 = tracker.tracks[i].trace[j][0][0]
                            y1 = tracker.tracks[i].trace[j][1][0]
                            x2 = tracker.tracks[i].trace[j+1][0][0]
                            y2 = tracker.tracks[i].trace[j+1][1][0]
                            clr = tracker.tracks[i].track_id % 9
                            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                    track_colors[clr], 2)

        # Display the resulting tracking frame
        cv2.imshow('Tracking', frame)

        # Display the original frame
        # cv2.imshow('Original', orig_frame)

        # 写视频文件
        videoout.write(frame)

        # Slower the FPS
        # cv2.waitKey(30)

        # Check for key strokes
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # 'esc' key has been pressed, exit program.
            break
        if k == 112:  # 'p' has been pressed. this will pause/resume the code.
            pause = not pause
            if (pause is True):
                print("Code is paused. Press 'p' to resume..")
                while (pause is True):
                    # stay in this loop until
                    key = cv2.waitKey(30) & 0xff
                    if key == 112:
                        pause = False
                        print("Resume code..!!")
                        break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # execute main
    main()

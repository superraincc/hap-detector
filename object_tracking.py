import cv2
import copy
from detector import Detector
from tracker import Tracker

filename = 'hap-middle'
video_route = '.\\data\\' + filename + '.mp4'
output_route = '.\\output\\' + filename + '-output.avi'

# 是否保存输出文件
ifsave = True

# 超过这一下落高度，则报警为高空抛物事件
hap_Threshold = 500

def main():

    cap = cv2.VideoCapture(video_route)

    # 获取视频参数
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('size=', (width, height), 'fps=', fps)

    if ifsave:
        videoWriter = cv2.VideoWriter(output_route, 
            cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))

    detector = Detector()

    tracker = Tracker(dist_thresh=100, max_frames_to_skip=30, max_trace_length=30, trackIdCount=100)

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

        # # Make copy of original frame
        # orig_frame = copy.copy(frame)

        # # Skip initial frames that display logo
        # if (skip_frame_count < 15):
        #     skip_frame_count += 1
        #     continue

        centers, frame, _ = detector.apply(copy.copy(frame))

        if (len(centers) > 0):

            # Track object using Kalman Filter
            tracker.Update(centers)

        # For identified object tracks draw tracking line
        # Use various colors to indicate different track_id
        for i in range(len(tracker.tracks)):
            # tracks是一个存储跟踪目标对象的数组
            if (len(tracker.tracks[i].trace) > 1):
                # y_array = [tracker.tracks[i].trace[j][1][0] for j in range(len(tracker.tracks[i].trace))]
                # if max(y_array) - min(y_array) > hap_Threshold:
                #     print('Warning!!')
                #     cv2.putText(frame, 'WARNING!!', (50, 150), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 12)
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
        videoWriter.write(frame)

        # Slower the FPS
        # cv2.waitKey(30)

        # Check for key strokes
        k = cv2.waitKey(10) & 0xff
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

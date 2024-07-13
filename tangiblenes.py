import cv2
import cv2.aruco as aruco
import sys
import time
from pynput.keyboard import Controller, Key







press_flag = [False,False,False,False,False,False,False,False,False]
release_flag = []





# default video id
video_id = 0

# possible change of video id in command line
if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

# aruco dictionary and parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco_params = aruco.DetectorParameters()

cap = cv2.VideoCapture(video_id)
if not cap.isOpened():
    print(f"Error: Could not open video device {video_id}")
    sys.exit()

keyboard = Controller()

#mapping ids and keys
key_mappings = {
    1: Key.up,
    2: Key.right,
    3: Key.down,
    4: Key.left,
    5: None,  # A
    6: None,  # B
    7: None,  # select
    8: None   # start
}


def handling_release():
    for i in range(1,len(release_flag)):
        if release_flag[i] == True:
            keyboard.release(key)
            press_flag[i] = False
            print("release")
    pass





while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from video device")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    release_flag = press_flag[:]

    # Check if marker is detected
    if ids is not None:
        # Draw lines along the sides of the marker
        aruco.drawDetectedMarkers(frame, corners)

        #bounding boxes
        for corner in corners:
            corner = corner.reshape((4, 2))
            corner = corner.astype(int)
            cv2.polylines(frame, [corner], True, (0, 255, 0), 2)

        #marker to key
        for marker_id in ids:
            #print(f"Detected marker ID: {marker_id[0]}")
            key = key_mappings.get(marker_id[0], None)
            if key:
                if press_flag[marker_id[0]] == False:
                    print("press")
                    keyboard.press(key)
                    press_flag[marker_id[0]] = True
                release_flag[marker_id[0]] = False
    #print(press_flag)
    #print(release_flag)
    #print("-------------")    
    handling_release()
    
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #time.sleep(0.5)
    
cap.release()
cv2.destroyAllWindows()

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

GREEN_MIN = np.array([29, 89, 8],np.uint8)
GREEN_MAX = np.array([74, 255, 255],np.uint8)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
lastTime = None
lowCenter = [9999, 9999]
highCenter = [0, 0]
centerInit = 15
startCount = 0;
CENTER_OFFSET = 10;

#
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2) 

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # print center[0], center[1]

        if centerInit is not None and centerInit > 0:
           centerInit -= 1
           if centerInit < 10:
	       if lowCenter[0] > center[0]:
	          lowCenter[0] = center[0]
	       if lowCenter[1] > center[1]:
	          lowCenter[1] = center[1]
	       if highCenter[0] < center[0]:
	          highCenter[0] = center[0] 
               if highCenter[1] < center[1]:
	          highCenter[1] = center[1] 
               print "lowCenter, highCenter: ", lowCenter, highCenter

        if centerInit is not None and centerInit == 0:
           lowCenter[0] = lowCenter[0] - CENTER_OFFSET
           lowCenter[1] = lowCenter[1] - CENTER_OFFSET
           highCenter[0] = highCenter[0] + CENTER_OFFSET
           highCenter[1] = highCenter[1] + CENTER_OFFSET
           print "lowCenter, highCenter: ", lowCenter, highCenter
           centerInit = None


        if (lowCenter[0] <= center[0] <= highCenter[0]) and (lowCenter[1] <= center[1] <= highCenter[1]): 
           startCount += 1
           print "Start found!!  ", startCount
       
        # if lastTime is None:
        #    lastTime = time.time()
        # curTime = time.time()
        # print "Center, radius, delay: ", center, radius, (curTime - lastTime)
        # lastTime = curTime

        # only proceed if the radius meets a minimum size
        # if radius > 1:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(image, center, 5, (0, 0, 255), -1)
    else:
        print "No contours found"

    
    # Show to the window
    cv2.imshow("Frame", image) 

    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

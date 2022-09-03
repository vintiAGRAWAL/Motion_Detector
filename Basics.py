import cv2
import pandas as pnd
import time
from datetime import datetime
# Assigning our static back position as None for initial frames
staticBack = None
# List of the tracks when any motion is detected in the frame
motionList = [None, None]
# A new list for capturing the time when movement detected
time = []
# Initializing DataFrame using pandas with Initial and Final column
dFrame = pnd.DataFrame(columns=["Start", "End"])
# Capturing Video from our system's Webcam
mainVideo = cv2.VideoCapture(0)
# Using an infinite while loop to capture images as a video
while True:
    # Reading each frame or image from the video
    check, frame = mainVideo.read()
    # Initializing motion as Statics frame
    motion = 0
    # Creating a gray frame from colour images
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Creating a GaussianBlur from the gray scale image to find changes
    grayFrame = cv2.GaussianBlur(grayImage, (21, 21), 0)
    # In first iteration, we make a gray frame from initial static frame
    if staticBack is None:
        staticBack = grayFrame
        continue
    # Calculation of difference between static and gray frame we created
    differFrame = cv2.absdiff(staticBack, grayFrame)
    # Highlighting the change between static background and current gray frame
    threshFrame = cv2.threshold(differFrame, 30, 255, cv2.THRESH_BINARY)[1]
    threshFrame = cv2.dilate(threshFrame, None, iterations=2)
    # Finding contour from the moving object in the frame
    contis, _ = cv2.findContours(threshFrame.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contr in contis:
        if cv2.contourArea(contr) < 10000:
            continue
        motion = 1
        (x, y, w, h) = cv2.boundingRect(contr)
        # Creating a green rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
   # Adding the motion status from frame
    motionList.append(motion)
    motionList = motionList[-2:]
    # Adding the motion Start time
    if motionList[-1] == 1 and motionList[-2] == 0:
        time.append(datetime.now())
   # Adding the motion End time
    if motionList[-1] == 0 and motionList[-2] == 1:
        time.append(datetime.now())
   # Displaying captured image in the gray scale
    cv2.imshow("This is the image captured in the Gray Frame", grayFrame)
    # Displaying the difference between current frame and the initial static frame
    cv2.imshow("Difference between the two frames", differFrame)
    # Displaying the black and white images from the video on the frame screen
    cv2.imshow(
        "This is a Threshold Frame created from the system's Webcam", threshFrame)
    # Displaying contour of the object through the color frame
    cv2.imshow(
        "This is one example of the Color Frame from the system's webcam", frame)
    # Creating a key to wait
    key = cv2.waitKey(1)
    # Ending the whole process with the 'm' key of our system
    if key == ord('q'):
        # Appending time when something is moving on the screen
        if motion == 1:
            time.append(datetime.now())
        break
# Adding the time of motion inside the data frame
for a in range(0, len(time), 2):
    dFrame = dFrame.append(
        {"Start": time[a], "End": time[a + 1]}, ignore_index=True)
# Creating a CSV file where all movements will be recorded
dFrame.to_csv("MovementsTimeFile.csv")
# Releasing the video
mainVideo.release()

cv2.destroyAllWindows()

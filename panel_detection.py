
import cv2
import numpy as np
import os
 
from os.path import isfile, join
 

def detect_panels(frame):
    gauss = cv2.GaussianBlur(frame, (7, 7), 0)
    edged = cv2.Canny(gauss, 25, 70)

    # find contours in the edged image, keep only the largest
    # ones

    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    screenCnt = []
    area = []
    e = 0
    # loop over our contours

    for (i, c) in enumerate(cnts):
        # approximate the contour
        epsilon = 0.1*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        # if our approximated contour has four points, then
        # we can assume that we have found a panel
        if len(approx) == 4:	
            screenCnt.append(approx)
            area.append(cv2.contourArea(approx))
            e+=1

    cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
    cv2.imshow("Panel detection", frame)
    cv2.waitKey(0)



def read_video(nameIn):
    cap = cv2.VideoCapture(nameIn)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
 
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        
            # Display the resulting frame
            cv2.imshow('Frame',frame)
            detect_panels(frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(15) & 0xFF == ord('q'):
                break
    
        # Break the loop
        else: 
            break
        
    # When everything done, release the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()


 
def main():
    nameIn= '/home/victoria/code testing/python/video3.avi'
    pathOut = 'video3.avi'
    read_video(nameIn)


if __name__=="__main__":
   main()
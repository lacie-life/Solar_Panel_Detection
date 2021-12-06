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
    cnts = cnts[0]
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    screenCnt = []
    area = []
    e = 0
    # loop over our contours

    for (i, c) in enumerate(cnts):
        # approximate the contour
        epsilon = 0.05*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        # if our approximated contour has four points, then
        # we can assume that we have found a panel
        if len(approx) == 4:	
            screenCnt.append(approx)
            area.append(cv2.contourArea(approx))
            e+=1

    print(type(screenCnt))
    cv2.drawContours(image=frame, contours=np.array(screenCnt), contourIdx=-1, color=(0, 255, 0), thickness=3)
    #cv2.imshow("Panel detection", frame)
    cv2.imwrite("result.jpg", frame)
    print("OK")
    #cv2.waitKey(0)

def read_image(frame):

    # Display the resulting frame
    #cv2.imshow('Frame', frame)
    #cv2.waitKey(0)
    detect_panels(frame)

    # Closes all the frames
    #cv2.destroyAllWindows()


if __name__=="__main__":
   im = cv2.imread("/home/jun/Github/Solar_Panel_Detection/Solar-Web/assets/images/real1.JPG")
   read_image(im)
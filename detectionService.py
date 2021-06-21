import numpy as np
import cv2 as cv

font = cv.FONT_HERSHEY_COMPLEX_SMALL

'''
Receives a raw frame and returns, in the first position the same frame with labels 
on the the panels and in the second position an image with only the panels.
'''
def nothing(x):
    pass

cv.namedWindow("options")
cv.createTrackbar("L-H","options",53,180,nothing)
cv.createTrackbar("L-S","options",49,255,nothing)
cv.createTrackbar("L-V","options",52,255,nothing)
cv.createTrackbar("H-H","options",135,255,nothing)
cv.createTrackbar("H-S","options",166,255,nothing)
cv.createTrackbar("H-V","options",173,255,nothing)
cv.createTrackbar("Size","options",5000,100000,nothing)
cv.createTrackbar("Kernel Size","options",4,10,nothing)
cv.createTrackbar("SizeImg","options",100,100,nothing)
cv.createTrackbar("Dilute","options",1,1,nothing)
cv.createTrackbar("Erode","options",1,1,nothing)
cv.createTrackbar("H-H Garbage","options",135,255,nothing)
cv.createTrackbar("H-S Garbage","options",166,255,nothing)
cv.createTrackbar("H-V Garbage","options",173,255,nothing)
cv.createTrackbar("Size Garbage","options",20,100,nothing)

'''LH = cv.getTrackbarPos("L-H")
LS = cv.getTrackbarPos("L-S")
LV = cv.getTrackbarPos("L-V")
UH = cv.getTrackbarPos("U-H")
US = cv.getTrackbarPos("U-S")
UV = cv.getTrackbarPos("U-V")
LHB = cv.getTrackbarPos("L-H")
LSB = cv.getTrackbarPos("L-S")
LVB = cv.getTrackbarPos("L-V")
UHB = cv.getTrackbarPos("U-H")
USB = cv.getTrackbarPos("U-S")
UVB = cv.getTrackbarPos("U-V")'''


#

def _getPanels(frame,
              scale_percent = 100,
              hsvValues = (80,28,63,135,166,173),
              kernelSize = 2,
              dilute = 0,
              erode = 0

              ):
    #print(hsvValues)
    normalized = np.zeros((800, 800))
    normalized = cv.normalize(frame,normalized, 0, 255, cv.NORM_MINMAX)
    hsv = cv.cvtColor(normalized, cv.COLOR_BGR2HSV)

    lower_red = np.array([hsvValues[0],hsvValues[1],hsvValues[2]])
    upper_red = np.array([hsvValues[3],hsvValues[4],hsvValues[5]])
    mask = cv.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    if dilute == 1:
        mask = cv.dilate(mask, kernel)
        mask = cv.dilate(mask, kernel/2)
    if erode == 1:
        mask = cv.erode(mask,kernel)
    cv.imshow("mascara 1", cv.resize(mask,(800,600)))

    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    #cv.imshow("Mask",mask)
    found = False
    mask2 = np.zeros_like(mask)
    for cnt in contours:
        area = cv.contourArea(cnt)
        approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > scale_percent:
            if len(approx) <= 4:
                found = True
                cv.fillPoly(mask2, [approx], 255)
                cv.drawContours(frame, [approx], 0, (0, 0, 0), 3)
                cv.putText(frame, "Panel", (x, y), font, 1, (0, 255,0))
    out = np.zeros_like(frame)  # Extract out the object and place into output image
    out[mask2 == 255] = frame[mask2 == 255]
    #cv.imshow("Out",out)
    return found, frame, out

'''
It receives a frame with only the panel and detects garbage on it. 
It returns a tagged image of the frame
'''
def _findObjectsInPanel(frame,
                       panelsImage,
                       scale_percent = 100,
                       hsvValues = (80,0,0,135,255,255)
                       ):
    hsv = cv.cvtColor(panelsImage, cv.COLOR_BGR2HSV)
    found = False

    lower_red = np.array([hsvValues[0],hsvValues[1], hsvValues[2]])
    upper_red = np.array([hsvValues[3], hsvValues[4], hsvValues[5]])
    mask = cv.inRange(hsv, lower_red, upper_red)
    #kernel = np.ones((4, 4), np.uint8)
    #mask = cv.erode(mask, kernel)

    mask = 255 - mask

    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    #mask2 = np.zeros_like(mask)
    for cnt in contours:
        area = cv.contourArea(cnt)
        approx = cv.approxPolyDP(cnt, 0.02 * cv.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if 10000 * scale_percent/100 > area > 100  * scale_percent/100:
            found = True
            cv.drawContours(frame, [approx], 0, (0, 0, 0), 1)
            cv.putText(frame, "Basura", (x, y), font, 1, (0,0,255))
    #cv.imshow("mask2",mask)
    #cv.imshow("Panel Objects",panelsImage)
    return frame, found



'''
Find cells
'''
def _findCells(frame,
                       panelsImage,
                       scale_percent = 100,
                       hsvValues = (80,0,0,135,255,255)
                       ):
    #print(hsvValues)
    hsv = cv.cvtColor(panelsImage, cv.COLOR_BGR2HSV)
    found = False

    lower_red = np.array([hsvValues[0],hsvValues[1], hsvValues[2]])
    upper_red = np.array([hsvValues[3], hsvValues[4], hsvValues[5]])
    mask = cv.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((2, 2), np.uint8)
    mask = cv.dilate(mask, kernel)

    #mask = 255 - mask

    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    #mask2 = np.zeros_like(mask)
    for cnt in contours:
        area = cv.contourArea(cnt)
        approx = cv.approxPolyDP(cnt, 0.04 * cv.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if 20000 * scale_percent/100 < area:
            if(len(approx) == 4):
                found = True
                cv.drawContours(frame, [approx], 0, (0, 0, 0), 3)
                cv.putText(frame, "Celda", (x, y), font, 1, (0, 0, 255))
    show = cv.resize(mask,(600,400))
    cv.imshow("mask2",show)
    #cv.imshow("Panel Objects",panelsImage)
    return frame, found


'''
Receives a raw frame and returns, 
resizes the image and detects the panels and garbage on it.
'''
def processFrame(frame):


    LH = cv.getTrackbarPos("L-H","options")
    LS = cv.getTrackbarPos("L-S","options")
    LV = cv.getTrackbarPos("L-V","options")
    UH = cv.getTrackbarPos("H-H","options")
    US = cv.getTrackbarPos("H-S","options")
    UV = cv.getTrackbarPos("H-V","options")
    SIZE = cv.getTrackbarPos("Size","options")
    KSize = cv.getTrackbarPos("Kernel Size","options")
    SIZEIMG = cv.getTrackbarPos("SizeImg","options")
    DIL = cv.getTrackbarPos("Dilute","options")
    ERO = cv.getTrackbarPos("Erode","options")
    UHB = cv.getTrackbarPos("H-H Garbage","options")
    USB = cv.getTrackbarPos("H-S Garbage","options")
    UVB = cv.getTrackbarPos("H-V Garbage","options")
    SIZEB = cv.getTrackbarPos("Size Garbage", "options")

    scale_percent = SIZEIMG  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    frame = cv.resize(frame, (width, height))
    garbage = False
    panel, frame, out = _getPanels(frame, SIZE, (LH,LS,LV,UH,US,UV),KSize, DIL, ERO);
    if panel:
        frame, garbage = _findObjectsInPanel(frame, out)
    return frame,panel,garbage

#'''
cap = cv.VideoCapture("VIDSC.MOV")
##################MAIN LOOP #####################
_, frame = cap.read()
while True:


     procesedframe, found, garbage = processFrame(frame)
     procesedframe = cv.resize(procesedframe,(800,600))
     cv.imshow("Frame",procesedframe)
     key = cv.waitKey(1)
     #print(key)
     if key == 27:
         break
     if key == 110:
         _, frame = cap.read()

cap.release()
cv.destroyAllWindows()
#'''
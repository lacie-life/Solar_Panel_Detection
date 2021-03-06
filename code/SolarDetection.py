from __future__ import print_function
import numpy as np
import argparse
import cv2
import sys
import glob
from PIL import Image
import math
import argparse
import imutils

lost_flag = 1
rot = 1
print("check")

im =cv2.imread("/home/jun/Github/Solar_Panel_Detection/Solar-Web/assets/images/real1.JPG")

scale_percent = 60  # percent of original size
width = int(im.shape[1] * scale_percent / 100)
height = int(im.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)


h_f, width_f, n = im.shape

original = im
img = im
visited = []
flag_frame = 0
max = 0
ypos = 0
sys.setrecursionlimit(1000000000)

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)

def prepro(original):
    all = []
    for gamma in np.arange(0.0, 1.5, 0.5):
        # ignore when gamma is 1 (there will be no change to the image)
        if gamma == 1:
            continue

        # apply gamma correction and show the images
        gamma = gamma if gamma > 0 else 0.1
        adjusted = adjust_gamma(original, gamma=gamma)
        cv2.putText(adjusted, "g={}".format(gamma), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

        gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

        size = 2
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)

        wide = cv2.Canny(blurred, 10, 200)
        wide = cv2.dilate(wide, np.ones((size, size)))
        squares = find_squares(wide)

        tight = cv2.Canny(blurred, 225, 250)
        tight = cv2.dilate(tight, np.ones((size, size)))
        squares2 = find_squares(tight)

        auto = auto_canny(blurred)
        auto = cv2.dilate(auto, np.ones((size, size)))
        squares3 = find_squares(auto)

        # cv2.namedWindow('original', cv2.WINDOW_NORMAL)
        # cv2.imshow("original", original)
        # cv2.waitKey(0)

        for i in range(0, len(squares)):
            all.append(squares.pop(0))
        for i in range(0, len(squares2)):
            all.append(squares2.pop(0))
        for i in range(0, len(squares3)):
            all.append(squares3.pop(0))

    return all

def find_white(x,y,lengthy):
    for i in range(int(y-(lengthy/2)),int(y+(lengthy/2))):
        if im[i][x] == 255:
            return 1
        return 0

def maxim(x, y):
    if x > y:
        return x
    return y

def minim(x, y):
    if x < y:
        return x
    return y

def in_list(x,y):
    global visited
    length = len(visited)
    for i in range(0,length):
        if(visited[i][0] == x and visited[i][1] == y):
            return 1
    return 0

def sort(unique):
    dimension = 0

    for i in range(len(unique)):
        dimension = (unique[i][1] - unique[i][0]) + dimension

    dimension = int(dimension / len(unique))
    i = 0

    sorted = []
    miny_pos = 0
    miny_pos2 = 0
    flag_min_pos = 0
    while len(unique) != 0:  # sort all frames
        miny = unique[0][2]
        miny_pos = 0
        flag_min_pos = 0

        for j in range(0, len(unique)):  # find the minY
            if miny > unique[j][2]:
                miny = unique[j][2]
                miny_pos = j
                flag_min_pos = 1

        temp = unique[0]

        miny = int(miny + (dimension*0.20))
        miny2 = int (miny + dimension*0.60)
        s = []
        sorted_temp = []
        j = 0
        flag = 1
        flag_exit = 0

        while (flag == 1):  # sort unique in temp by y
            if (miny < unique[j][3] and miny > unique[j][2]) or (miny2 < unique[j][3] and miny2 > unique[j][2]):
                temp = unique.pop(j)

                sorted_temp.append(temp)
                flag_exit = 1
            else:
                j = j + 1
            if (j == len(unique)):
                flag = 0

        # sorted_temp has all y frames
        temp2 = []

        while (len(sorted_temp) != 0):  # sort temp in temp2 by x
            i_pos = 0
            temp = sorted_temp[0]
            for i in range(0, len(sorted_temp)):  # find minx
                if temp[0] > sorted_temp[i][0]:
                    temp = sorted_temp[i]
                    i_pos = i

                    flag_exit = 1
            temp2 = sorted_temp.pop(i_pos)

            sorted.append(temp2)
            # extra kodikas gia diplotipa
        if flag_exit == 0 and miny_pos < len(unique):  # an den yparxei plaisio stn a3ona y
            unique.pop(miny_pos)

    print("Sorted: ", sorted)
    return sorted

def rec(pos, y, length):
    global max
    global visited
    global flag_frame
    global ypos
    global h_f

    if (pos < 0 or y==h_f-1 or y==0):
        return
    if length == pos:
        flag_frame = 1
        ypos = y
        return

    if in_list(pos, y) == 1 and len(visited) != 0:
        return
    else:
        temp = []
        temp.append(pos)
        temp.append(y)
        visited.append(temp)

    if (flag_frame == 0 and im[y][pos - 1]) == 255:
        rec(pos - 1, y, length)
    if (flag_frame == 0 and im[y + 1][pos]) == 255:
        rec(pos, y + 1, length)
    if flag_frame == 0 and im[y + 1][pos - 1] == 255:
        rec(pos - 1, y + 1, length)
    if flag_frame == 0 and im[y - 1][pos - 1] == 255:
        rec(pos - 1, y - 1, length)

def rec2(pos, y,length):

    global max
    global visited
    global flag_frame
    global ypos
    global h_f
    global width_f

    if (pos == width_f-1 or y==0 or y==h_f-1 or pos==0):
        max = width_f-1
        return

    if length == pos :
        flag_frame = 1
        ypos = y

    if(pos == length):
        return

    if in_list(pos,y) == 1 and len(visited) != 0:
        return
    else:
        temp = []
        temp.append(pos)
        temp.append(y)
        visited.append(temp)

    max = maxim(pos, max)


    if (flag_frame == 0 and im[y][pos + 1]) == 255:
        rec2(pos + 1, y,length)
    if(flag_frame == 0 and im[y+1][pos]) == 255:
        rec2(pos,y+1,length)
    if flag_frame == 0 and im[y+1][pos + 1] == 255:
        rec2(pos+1, y+1,length)
    if flag_frame == 0 and im[y-1][pos + 1] == 255:
        rec2(pos +1, y-1,length)

def find_lines(pos,y,length,flag):
    global visited
    global flag_frame
    global max
    global ypos

    visited = []
    flag_frame = 0
    max = 0
    ypos = 0

    if flag == 1:
        rec2(pos,y,length)
    elif flag == 0:
        rec(pos,y,length)

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )



def print_list(list):
    print(len(list[0]),"\n")
    print(list[0])
    for i in range(0,len(list)):
        print(list[i])
    print("\n")

def exist(t,all):
    for i in range(0,len(all)):
        if same_range(t[0],t[1],all[i][0],all[i][1]) == 1 and same_range(t[2],t[3],all[i][2],all[i][3]) == 1:
            return 1
    return 0

def same_range( x1,x2,nx,nx2 ):
    if (nx2-nx) > ((x2-x1)*1.5): # orthogonia apo dipla plaisia epistrefei false
        return 0

    if (x1 >= nx and x1 <=nx2) or (x2 >= nx and x2 <=nx2) or (nx >= x1 and nx <=x2) or (nx2 >= x1 and nx2 <=x2):
        return 1

    return 0

def same_in_x (x1,x2,pos):
    if(pos >= x1 and pos <= x2):
        return 1
    return 0

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)

    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.2:
                        squares.append(cnt)
    return squares

def write_and_crop(list,original_crop):
    if len(list) == 0 :
        print("Empty List")
        return 0

    temp = list[0]
    string = "./Panels/" # vale dame to path
    f=open("./results/where.txt",'w')
    #f.write(str(len(list))+"\n")
    for i in range(0, len(list)):
        str_path = (string + str(i+1) + ".jpg")
        cropped = original_crop[list[i][2]:list[i][3],
                  list[i][0]:list[i][1]]
        f.write(str(list[i][2])+" "+str(list[i][3])+" "+str(list[i][0])+" "+str(list[i][1])+"\n")
        #cv2.imwrite(str_path, cropped)
    f.close()
    print("Number of frames :",i+1)


def extra(list):
    #print_list(list)
    if len(list) == 0 :
        return []
    temp = []
    y = []
    dimension = int((list[0][3] - list[0][2])/2)
    y = dimension + list[0][2]
    count = 0
    list_int = []

    for i in range(0,len(list)):
        if y < list[i][3] and y > list[i][2] :
            y = dimension + list[i][2]
            count = count +1
            temp.append(list[i])
            list_int.append(i)
    for j in range(0,count):
        p = list_int[len(list_int)-1]
        # print(p)
        list.pop(p)
        list_int.pop(len(list_int)-1)
    return temp

    i_temp = []
    # i=0
    # av = 0
    # if len(temp) != 0:
    #     for i in range(0,len(temp)) :
    #         av = av + (temp[i][1] - temp[i][0])
    #     av = int(av/(i+1))
    # else:
    #     return []
    #
    #
    #
    # wrong_pos = []
    # correct = []
    #
    # for i in range(0,len(temp)):
    #     if av*1.1 > (temp[i][1]-temp[i][0]) and av/2 < (temp[i][1]-temp[i][0]) and temp[i][1]-temp[i][0] > int(av*0.5):
    #         correct.append(temp[i])
    #
    #
    # temp = correct
    #
    # # print("len(wrong) : ",len(wrong_pos))
    #
    #
    #
    # return temp
    #
    #     # list2 = []
    #     # op_flag = 1
    #     #
    #     #
    #     # while (flag_frame == 1 and op_flag == 1):
    #     #     find_lines(temp2[0], temp2[3], temp2[0] - avg1, 0)
    #     #     if (flag_frame == 1):
    #     #         x2 = list[0][0] - int((list[0][1] - list[0][0]) * 0.1)
    #     #         x1 = list[0][0] - int(avg * 1.1)
    #     #         y1 = list[0][2]
    #     #         y2 = ypos
    #     #         temp2 = []
    #     #         temp2.append(x1)
    #     #         temp2.append(x2)
    #     #         temp2.append(y1)
    #     #         temp2.append(y2)
    #     #         temp2.append(1)
    #     #         temp2.append(x1 - int(avg / 2))
    #     #
    #     #         if (exist(temp2, list) or exist(temp2, final)):
    #     #             op_flag = 0
    #     #         else:
    #     #             list2.insert(0, temp2)
    #     #
    #     #         temp2 = list2[0]
    #     # for l in range(0, len(list2)):
    #     #     list.append(list2[l])

def mark_frames(list,original):

    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(0, len(list)):
        temp = list[i]
        x = (int((temp[1]-temp[0])/2) + temp[0])
        y = (int((temp[3]-temp[2])/2) + temp[2])

        im = cv2.circle(original, (x, y), 10, (255, 255, 255), -1)  # aspro

        cv2.circle(original, (temp[0], temp[2]), 5, cv2.QT_FONT_BLACK, -1)
        cv2.circle(original, (temp[0], temp[3]), 5, cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, -1)
        cv2.circle(original, (temp[1], temp[2]), 5, (255, 0, 0), -1)
        cv2.circle(original, (temp[1], temp[3]), 5, 255, -1)

def find_lost_frames (list):
    temp = []
    temp = list[0]
    length = list [0][1] - list [0][0]
    lengthy = list[0][3] - list[0][2]

    flag = 0
    temp2 = []
    count = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    av = 0
    k=0

    for k in range(0,len(list)):
        av = av + (list[k][1] - list[k][0])
    av = int(av/k)

    if(list[0][0] - int(av/2) > av): # lost frames in x -
        pos = list[0][0] - int(av / 2)
        print("----------------- ",av)
        #pos = pos - 12
        while(pos > 0):

            for i in range(0,len(list)):
                temp = list[i]
                if( same_in_x(temp[0],temp[1],pos)):
                    flag = 1

            if(flag == 0):
               x2 = pos + int(length/2)
               x1 = pos - int(length/2)
               print("x1 is : ",x1)
               print("x2 is : ",x2)
               if(x1>=0) :
                temp2.append(x1)
                temp2.append(x2)
                temp2.append(list[0][2])
                temp2.append(list[0][3])
                count = count +1

                cv2.putText(im, "#",
                            (x1 + int(length/2) ,int((list[0][3]-list[0][2])/2)+list[0][2]), font, 1,
                            (0, 0, 0), 8)

            pos = pos - av
            flag = 0
            print("pos is : ", pos)


    else : # lost frames in x +
        pos = list[0][1] + int(av/2)

        print("--------av--------- ", av)

        h, width, n = im.shape

        cur_pos = 0
        k = 2
        while (pos < (width-av/2)):

            print("\n\n",pos,"\n\n" ,k)


            for i in range(0, len(list)): # forward frames and find lost

                temp = list[i]
                cur_pos = (temp[1]) + int(av / 2)

                if (same_in_x(temp[0], temp[1], pos) and flag==0):
               #     print("yparxei : ", k)
                    print("cur   :   ",cur_pos,"  ",temp)
                    pos = cur_pos
                    flag = 1
                    #pos = pos + (temp[1] - temp[0])


            if (flag == 0):
               # print("k is : ", k)
                x2 = pos + int(length / 2) # new position
                x1 = pos - int(length / 2)
                print("x1 is : ", x1)
                print("x2 is : ", x2)

                if (x1 < width):#################################
                    temp2.append(x1)
                    temp2.append(x2)
                    temp2.append(list[0][2])
                    temp2.append(list[0][3])
                    count = count + 1

                    cv2.putText(im, "#",
                                (x1 + int(length / 2), int((list[0][3] - list[0][2]) / 2) + list[0][2]), font, 1,
                                (0, 0, 0), 8)
                    pos = pos + x2-x1

            flag = 0
            print("pos is : ", pos )
            k = k+1

    print("count is  : ",count)

def lost(list,final):
    global max
    global flag_frame
    global visited
    global ypos
    global im
    plus = 0
    list_temp = []

    if len(list)==0:
        return []

    font = cv2.FONT_HERSHEY_SIMPLEX
    avg = 0
    avg_y =0
    i = 0
    for i in range(0,len(list)):
        avg = avg + (list[i][1] - list[i][0])
        avg_y = avg_y + (list[i][3]-list[i][2])

    avg = int(avg/(i+1))
    avg_y = int(avg_y / (i))
    avg1 = avg - int(avg * 0.4)

    lost= []
    temp = list[0]

    flag_pixel = 1

    while(flag_pixel == 1):


        find_lines(list[0][0], list[0][3], list[0][0] - avg1, 0) # aristera

        if(flag_frame == 1):
            x2 = list[0][0] - int((list[0][1]-list[0][0]) * 0.1)
            x1 = list[0][0] - int(avg*1.1)
            y1 = list[0][2]
            y2 = ypos
            temp_pos = []
            temp_pos.append(x1)
            temp_pos.append(x2)
            temp_pos.append(y1)
            temp_pos.append(y2)
            temp_pos.append(1)
            temp_pos.append(x1 - int(avg/2))

            if x1 > 0 and exist(temp_pos,list) == 0 and exist(temp_pos,final) == 0 and im[temp_pos[2]][temp_pos[0]] == 255:
                list.insert(0,temp_pos)
            else :
                flag_pixel=0
        else :
            flag_pixel = 0

    i=0
    # length = len(list)
    while i < len(list):

        temp2 = []
        flag_frame = 1
        temp2 = list[i]
        temp_pos = []
        if(temp[1] + avg1) < list[i][0]: # an den yparxei plaisio meta
            print("is in and i is :",i)
            find_lines(temp[1],temp[3],temp[1]+avg1,1)
            print("flag ",flag_frame)

            if(flag_frame == 1): #an yparxei gramh
                x1 = temp[1] + int(avg * 0.1)
                x2 = temp[1] + int(avg*1.1)
                y1 = ypos - (temp[3] - temp[2])
                y2 = ypos

                temp_pos.append(x1)
                temp_pos.append(x2)
                temp_pos.append(y1)
                temp_pos.append(y2)
                temp2.append(1)
                temp2.append(x2 - int(avg / 2))

                if (exist(temp_pos,list) == 0 ) and (exist(temp2,final) == 0) and im[temp_pos[2]][temp_pos[0]] == 255:
                        list.insert(i,temp_pos)

        if (list[i][0] - avg1) > temp[1]:

            find_lines(list[i][0], list[i][3], list[i][0] - avg1, 0)

            if (flag_frame == 1):  # an yparxei gramh

                x2 = list[i][0] - int(avg * 0.10)#temp[1] + int(avg * 0.10)
                x1 = list[i][0] - int(list[i][1] - list[i][0])#temp[1] + avg
                y1 = ypos - (temp[3] - temp[2])
                y2 = ypos

                temp_pos = []
                temp_pos.append(x1)
                temp_pos.append(x2)
                temp_pos.append(y1)
                temp_pos.append(y2)
                temp_pos.append(1)
                temp_pos.append(x2 + int(avg / 2))

                if exist(temp_pos, list) == 0 and exist(temp_pos,final) == 0 and im[temp_pos[2]][temp_pos[0]] == 255:
                        list.insert(i, temp_pos)

        temp = list[i]
        i = i + 1

    flag_frame = 1

    while(flag_frame == 1):
        size = len(list)
        find_lines(list[size-1][1], list[size-1][3], list[size-1][1] + avg1, 1)
        print("this is the new test---------->    ",flag_frame)
        if (flag_frame == 1):
            x2 = list[size-1][1] + int(avg * 1.1)
            x1 = list[size-1][1] + int(avg * 0.1)
            y1 = ypos - (list[size-1][3] - list[size-1][2])
            y2 = ypos
            temp_pos = []
            temp_pos.append(x1)
            temp_pos.append(x2)
            temp_pos.append(y1)
            temp_pos.append(y2)


            if x2 < 4000 and exist(temp_pos, list) == 0 and exist(temp_pos, final) == 0 and im[temp_pos[2]][temp_pos[0]] == 255:
                    list.append(temp_pos)
            else:
                flag_frame = 0

    return


def duplicate(list_all):
    unique = []
    flag = 0
    dimension = 0
    dimension_y = 0

    list_int = []

    for i in range(len(list_all)):
        dimension = (list_all[i][1] - list_all[i][0]) + dimension
        dimension_y = (list_all[i][3] - list_all[i][2]) + dimension_y
    dimension_y = int(dimension_y / len(list_all))
    dimension = int(dimension / len(list_all))

    print("Dimension: ", dimension)
    print("Dimension y :", dimension_y )

    i = 0

    while flag:  # large frames
        avx = (list_all[i][1] - list_all[i][0])
        if (avx > int(dimension * 1.5)) or (avx < int(dimension*0.5)) or ((list_all[i][3]-list_all[i][2])<(dimension_y*0.65)):
            list_all.pop(i)
        else:
            i = i + 1

        if i == len(list_all):
            flag = 0

    print(len(list_all))

    flag = 1
    p = dimension*0.2
    for i in range(0, len(list_all)):
        flag = 1
        temp = list_all.pop()

        for j in range(0, len(unique)):  # if already exist
            if same_range(temp[0], temp[1], unique[j][0]+p, unique[j][1]-p) and same_range(temp[2], temp[3],
                                                                                           unique[j][2]+p,
                                                                                           unique[j][3]-p):
                # if unique[j][0] > temp[0]:
                #     unique[j][0] = temp[0]
                # if unique[j][2] > temp[2]:
                #     unique[j][2] = temp[2]
                # if unique[j][1] < temp[1]:
                #     unique[j][1] = temp[1]
                # if unique[j][3] > temp[3]:
                #     unique[j][3] = temp[3]

                flag = 0
        if flag == 1:
            unique.append(temp)
    print("Duplicate: ", unique)
    return unique


def auto_canny(image, sigma=0.55):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    print(sigma,"   ",v,"   ")
    # apply automatic Canny edge detection using the computed median
    temp = (1.0 - sigma) * v
    if temp<0:
        lower = 0
    else:
        lower = int(temp)
    # lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def positions(squares):
    list_all = []
    for j in range(0, len(squares)):  # get min and max of x,y of all frames
        temp = squares.pop(0)
        xmax = 0
        xmin = temp[0][0]
        ymax = 0
        ymin = temp[0][1]
        i = 0

        for numx in temp:

            if xmax < numx[0]:
                xmax = numx[0]
            if xmin > numx[0]:
                xmin = numx[0]
            if ymax < numx[1]:
                ymax = numx[1]
            if ymin > numx[1]:
                ymin = numx[1]

        list = []
        list.append(xmin)
        list.append(xmax)
        list.append(ymin)
        list.append(ymax)
        list.append(0)
        list.append(0)
        #print(list)

        list_all.append(list)
    print(len(list_all))
    return list_all

def angle (a, b, c):
    return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

def rotation(original):

    global h_f, width_f

    img = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)  # gray
    img = cv2.blur(img, (3, 3))

    kernel = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    img = cv2.Canny(img, 50, 200)

    img = cv2.dilate(img, np.ones((5, 5)))
    t, img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)

    # cv2.imshow("check", img)
    # cv2.waitKey(0)

    pos_list = find_squares(img)
    print("Size pos_list: ", len(pos_list))
    #print(pos_list)

    print(len(pos_list),"  ->before")

    pos_list = positions(pos_list)

    pos_list = duplicate(pos_list)
    
    print(len(pos_list),"  ->after")
    #pos_list = sort(pos_list)

    #print("Check: ", pos_list)
    max_pos = []
    next = []
    max_len = 0

    while(True):
        next = extra(pos_list)
        if(len(next)>max_len):
            max_len=len(next)
            max_pos=next

        if(len(pos_list)==0):
            break

    print("Max pose: ")
    print(len(max_pos),"\t",max_pos)
    one=[]
    two=[]
    three=[]

    print("Max Pose length: ", len(max_pos))
    print(max_pos[0],max_pos[len(max_pos)-1])

    if(len(max_pos)>1):
        one.append(max_pos[0][0])
        one.append(max_pos[0][3])
        two.append(max_pos[2][1])
        two.append(max_pos[2][3])

        three.append(two[0])
        three.append(one[1])

    ypotinousa= math.sqrt(pow((two[0]-one[0]),2)+pow((two[1]-one[1]),2))
    platos = math.sqrt(pow((three[0]-one[0]),2)+pow((three[1]-one[1]),2))
    ipsos = math.sqrt(pow((two[0]-three[0]),2)+pow((two[1]-three[1]),2))

    num = int(angle(ypotinousa, platos, ipsos)+1)

    print(num," This is a num")
    rotated = original


    if(one[1]>two[1]):
       rotated = imutils.rotate_bound(original,num)
    else:
       rotated = imutils.rotate_bound(original,-num)

        # h,width,n = rotated.shape
        # print(rotated.shape)

    h_f, width_f, n = rotated.shape

    return rotated

###################################################### main #################################################################
if __name__ == '__main__':

        original = rotation(original)
        
        original_crop = original.copy()
        original2 = original

        img = original2
        im = original2

        img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # gray
        img = cv2.blur(img, (3, 3))

        kernel = np.ones((5, 5), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        img = cv2.Canny(img, 50 ,200)


        img = cv2.dilate(img, np.ones((5, 5)))
        t, img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)

        im = img

        squares = prepro(original)
        # cv2.drawContours(original, squares, -1, (0, 255, 0), 1)
        #cv2.namedWindow('marked', cv2.WINDOW_NORMAL)
        #cv2.imshow("marked", original)
        #cv2.waitKey(0)

        new = img
        count_frames = 0

        list_all = []
        list=[]

        list_all = positions(squares) #change the types of positions

        monadika = []

        print("Nubrer of frames : ",len(list_all))

        monadika = list_all
        dup = duplicate(list_all)
        sorted = sort(dup)
        mark_frames(sorted,original)
        write_and_crop(sorted,original_crop)
        # final = []

        # while(len(sorted)!=0):
        #     t = extra(list_all)
        #     lost(t,final)
        #     if(len(t)>2):
        #         mark_frames(final)

        cv2.namedWindow('marked', cv2.WINDOW_NORMAL)
        # cv2.imshow("marked", original)
        # cv2.waitKey(0)
        print("frames marked = ",count_frames)
        cv2.imwrite("./images/output/rotated.jpg", original_crop)
        cv2.imwrite("./images/output/foundSolar.jpg", original)


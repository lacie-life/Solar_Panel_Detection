# import cv2, numpy as np

# # Path to source video:
# output_path = 'clicks.csv'

# # Mouse callback function
# global click_list
# click_list = []
# def callback(event, x, y, flags, param):
#     if event == 1: click_list.append((x,y))
# cv2.namedWindow('img')
# cv2.setMouseCallback('img', callback)

# img = cv2.imread('dataset/0.jpg')

# # Mainloop - show the image and collect the data
# while True:
#     cv2.imshow('img', img)
#     # Wait, and allow the user to quit with the 'esc' key
#     k = cv2.waitKey(1)
#     # If user presses 'esc' break
#     if k == 27: break
# cv2.destroyAllWindows()

# # Write data to a spreadsheet
# import csv
# with open(output_path, 'w') as csvfile:
#     fieldnames = ['x_position', 'y_position']
#     writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
#     writer.writeheader()
#     for position in click_list:
#         x, y = position[0], position[1]
#         writer.writerow({'x_position': x, 'y_position': y})



import cv2, numpy as np
import json
import os

global click_list
click_list = []
def callback(event, x, y, flags, param):
    if event == 1: click_list.append((x,y))
cv2.namedWindow('img')
cv2.setMouseCallback('img', callback)
box = {}
path = 'drone'
for filename in os.listdir(path):
    img_file = os.path.join(path, filename)
    img = cv2.imread(img_file)
    click_list = []
    while len(click_list)!=4:
        cv2.imshow('img', img)
        # Wait, and allow the user to quit with the 'esc' key
        k = cv2.waitKey(1)
        # If user presses 'esc' break
        if k == 27: break
    if len(click_list)==4:
        box[filename] = click_list

box_file = open('box_{}.json'.format(path), "w")
json.dump(box, box_file)
box_file.close()

import cv2 as cv
import numpy as np
from math import floor
from math import ceil

img = cv.imread("river_img.JPG")
assert img is not None, "file could not be read, check with os.path.exist()"

def Show_img(img_list):
    index = 0
    for img in img_list:
        cv.imshow(str(index),img)
        index+=1
    cv.waitKey(0)
    cv.destroyAllWindows()

def Get_center(coord): 
    return ceil((coord-1)/2.0)

""" (1) Padding the image """

row, col, colors = img.shape

PADDING_LR = floor(col/2)
PADDING_TB = floor(row/2)

pad = cv.copyMakeBorder(img, PADDING_TB, PADDING_TB, 
                        PADDING_LR, PADDING_LR, borderType = cv.BORDER_CONSTANT, value = (0, 0,0))

""" (2) Rotating the image """

THETA = 10

pad_row, pad_col, pad_colors = pad.shape

# centerx = floor((pad_col-1)/2.0)
# centery = floor((pad_row-1)/2.0)

centerx = Get_center(pad_col)
centery = Get_center(pad_row)

matrix = cv.getRotationMatrix2D((centerx, centery), THETA, 1)
rot = cv.warpAffine(pad, matrix, (pad_col, pad_row))

""" (3) Upsample the image """

FACT = 1.6

# for each 5 degrees, increase fact by 0.3x

res = cv.resize(rot, None, fx=FACT, fy=FACT, interpolation = cv.INTER_CUBIC)

""" (4) Crop the image """

res_row, res_col, res_color = res.shape

centerx = Get_center(res_col)
centery = Get_center(res_row)

print("this is res ", res.shape)
print("this is the center of res ", centery, centerx)

# col is x
# row is y

quarterx = Get_center(col)
quartery = Get_center(row)

print('this is quarterx ', quarterx)
print('this is quartery ', quartery)

crop = res[centery-quartery:centery+quartery, centerx-quarterx:centerx+quarterx]

print("this is img ", img.shape)
print("this is crop ", crop.shape)

Show_img([img, pad, rot, res, crop])








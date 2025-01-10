"""
UTILIES SCRIPT FOR 
SITE_ID_BALANCER.PY
"""

import cv2 as cv
import os
from math import ceil, floor
import shutil

"""-----DATA AUGMENTATION-----"""
def Data_augmentation(img, THETA, FACT, flipped):
   img = cv.imread(img)
   if flipped == False: # if regular rotation
       pad = Pad_img(img)   
       rot = Rotate_img(pad, THETA)
       up = Upsample_img(rot, FACT)
       return Center_crop(up, img)
   else:                # if horizontal flip rotation
       flip = Flip_img(img)
       pad = Pad_img(flip)   
       rot = Rotate_img(pad, THETA)
       up = Upsample_img(rot, FACT)
       return Center_crop(up, img)

def Pad_img(img):
   row, col, colors = img.shape
   padding_lr = floor(col/2) # left and right
   padding_tb = floor(row/2) # top and bottom
   return cv.copyMakeBorder(img, padding_tb, padding_tb,
                       padding_lr, padding_lr, borderType = cv.BORDER_CONSTANT, value = (0, 0,0))
def Flip_img(img):
   return cv.flip(img, 1)

def Get_center(coord):
   return ceil((coord-1)/2.0)

def Rotate_img(img, THETA):
   row, col, colors = img.shape
   centerx = Get_center(col)
   centery = Get_center(row)
   matrix = cv.getRotationMatrix2D((centerx, centery), THETA, 1)
   return cv.warpAffine(img, matrix, (col,row))

def Upsample_img(img, FACT):
   # for each 5 degrees, increase fact by 0.3x
   return cv.resize(img, None, fx=FACT, fy=FACT, interpolation = cv.INTER_CUBIC)

def Center_crop(img, og_img):
   row, col, color = img.shape
   og_row, og_col, og_color = og_img.shape
   centerx = Get_center(col)
   centery = Get_center(row) # --> padded, rotated and upscaled image center
   ogx = Get_center(og_col)
   ogy = Get_center(og_row) # ---> image center of original image
   return img[centery-ogy:centery+ogy, centerx-ogx:centerx+ogx]

"""------HELPER FUNCTIONS------"""
def CreateDir(folder_name):
   if not os.path.exists(folder_name):
       os.makedirs(folder_name)   

def SortDict(dict):
   # Sort the dictionary by its value in ascending order
   sorted_items = sorted(dict.items(), key=lambda item: item[1])
   return sorted_items

def Get_center(coord):
   return ceil((coord-1)/2.0)

def Copy_dir(src, dst): 
   try: 
      shutil.copytree(src, dst)
   except Exception as e:
      print(f"Error copying {src} to {dst}: {e}")
      print("This does not mean the program is not working correctly, it just means that the directory already exists\n")

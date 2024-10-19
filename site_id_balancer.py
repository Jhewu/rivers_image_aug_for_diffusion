"""
This script analyses processed and labeled
image folder with river images, and then 
creates a new folder with the data balanced 
through augmentation. This script must be within 
the same directoy as the labeled images, and 
the same directoy as the data_is_balanced.py
script
"""

# Import external libraries
import os
import shutil
import random
import cv2 as cv
from math import floor
from math import ceil

# Import script to check if data is balanced
from data_is_balanced import Data_Is_Balanced

"""------HELPER FUNCTIONS------"""

# MAIN DATA AUGMENTATION FUNCTION
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
   return cv.flip(img, 1);

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

def CreateDir(folder_name):
   if not os.path.exists(folder_name):
       os.makedirs(folder_name)   

def SortDict(dict):
   # Sort the dictionary by its value in ascending order
   sorted_items = sorted(dict.items(), key=lambda item: item[1])
   return sorted_items

def Get_center(coord):
   return ceil((coord-1)/2.0)

"""------Main Runtime------"""
def DataBalancer(label):
    """
    Data Balancer, balances the data by comparing the
    site with the minimum amount of images (with a multiplier),
    to the site with the maximum amount of images. If the multiplier,
    does not reach, then ignore this site. For all of the others that do
    meet, apply the data augmentation required to meet the number of images
    in the max. We are sacrificing some diversity, in order to get the maximum
    amount of data, since diffusion models work well with a lot of data,
    to generalize better.

    The specific augmentations are rotations every 5 degrees, from 5-60,
    and then do horizontal flip, and then do 5-60 again. Therefore, we have
    a total of 23x multiplier per site ID.
    """
    LABEL = label
    folder_name = f"{LABEL}"
    new_folder_name = f"balanced_{LABEL}"

    # obtain image directory
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    image_dir = os.path.join(file_dir, folder_name)
    dir_list = os.listdir(image_dir)
    
    # declare dictionary to count site_id
    # NOTICE THE DIFFERENCE BETWEEN site_ids (dict)
    # AND site_id (IMAGE NAME)
    site_ids = {}

    # declare dictionary to store the full_paths of
    # each image within a site id
    site_path = {} # dictionary with a list inside

    # declare dictionary to store file names, for the
    # augmented files
    filename_dict = {}

    # count site_id and append full_file_path
    total_files = 0
    for file_name in dir_list:
        total_files += 1
        full_file_path = os.path.join(image_dir, file_name)
        image_name = os.path.basename(full_file_path)
        site_id = image_name.split("_")[0]
    
        if site_id in site_ids:
            site_ids[site_id] += 1
            site_path[site_id].append(full_file_path)
            filename_dict[site_id].append(file_name)
        else:
            site_ids[site_id] = 1
            site_path[site_id] = [full_file_path]
            filename_dict[site_id] = [file_name]

    # sort the dictionary, and turn it into a list
    sorted_list = SortDict(site_ids)
    max = sorted_list[-1][1]

    # delete the site_ids with the least number images with the
    # multiplier (23x) that do not meet the max
    deleted_counter = 0
    total_deleted = 0
    for item in sorted_list[:]: # when you delete from the same lists, problems, so use [:]
        min = item[1]*23
        if min >= max:
            break
        else: # min <= max
            # delete for all dict and lists
            deleted_counter+=1
            total_deleted += item[1]
            del site_path[item[0]]
            del site_ids[item[0]]
            del filename_dict[item[0]]
            sorted_list.remove(item)
            #print(f"Removed {item}")

    CreateDir(new_folder_name)
    destination = os.path.join(file_dir, new_folder_name)

    # Transfer all the images from the max to the
    # new directory
    max_site = sorted_list[-1][0]
    for site_img in range(max):
        shutil.copy(site_path[max_site][site_img], destination)

    # delete the site from all dict and list
    del site_path[max_site]
    del site_ids[max_site]
    del filename_dict[max_site]
    sorted_list.remove(sorted_list[-1])

    # for both the shuffling between the site_path
    # and filename_dict to be the same
    seed = 42

    # copy image_count amount of images from each site ids
    # onto the new folder, and augment the rest to meet the
    # max amount of images
    site_number = 0
    for site in site_path:
        # copy all the original images
        for site_img in range(site_ids[site]):
            shutil.copy(site_path[site][site_img], destination)
        
        # randomly shuffle the list contents
        # so that the balancing is not deterministic
        random.seed(seed)
        random.shuffle(site_path[site])
        random.shuffle(filename_dict[site])

        # already used all of the original images
        # ... now augment the original images,
        # to reach the max. The code is applying
        # the minimum degree of rotation to each
        # image in order to reach the image count
        image_count_aug = max - site_ids[site]    # --> number of images to augment to reach max
        counter = 1                               # --> counter for number of images currently augmented 
        switch = -1                               # --> (see more down), rotations only or horizontal flipped rotations

        switch_ended = 1                          # ---> after the switch is triggered two times, increase THETA and FACT
        THETA = 5                                 # --> angle of rotations (for augmentation)
        FACT = 1.3                                # --> factor to upsample

        while counter <= image_count_aug:            # --> continue to augment in case rotation or flip rotation is not enough
            #print(f"There are {image_count_aug} images to augment in site {site}, and we are in {counter}")
            for site_img in range(site_ids[site]):
                new_destination = os.path.join(destination, f"{filename_dict[site][site_img]}_augmented_{counter}.JPG")
                if counter > image_count_aug:       # --> if we reached enough images within the loop
                    #print(f"\nBroke when counter was {counter}, and image_count_aug was {image_count_aug}\n")
                    break
                elif switch == -1: #  case 1: only rotations
                    augmented_img = Data_augmentation(site_path[site][site_img], THETA, FACT, False)
                    cv.imwrite(new_destination, augmented_img)
                    counter+=1
                elif switch == 1:  # case 2: only horizontal flipped rotations
                    augmented_img = Data_augmentation(site_path[site][site_img], THETA, FACT, True)
                    cv.imwrite(new_destination, augmented_img)
                    counter+=1
            switch = switch*-1
            if switch_ended % 2 == 0:
                THETA+=5
                FACT+=0.3 # --> these THETA and FACT values ensure no black padding on final image
            switch_ended+=1
        site_number+=1
        #print(f"There are {len(site_path)+1} number of sites, and we are in {site_number}")

    print(f"\n Data balanced is completed for {LABEL}!\n")
    print(f"\n Original dataset contained {total_files} number of images\n")
    print(f"\n Augmented dataset contains {max * (len(sorted_list)+1)} number of images\n")

if __name__ == "__main__":
    folder_labels = ["1", "2", "3", "4", "5", "6"]
    print(f"\n-----Balancing/augmenting dataset-----\n")
    for label in folder_labels: 
        print(f"\nProcessing label {label}\n")
        DataBalancer(label)
    print(f"\n-----Checking if the dataset is balanced-----\n")
    for label in folder_labels:
        Data_Is_Balanced(f"balanced_{label}")















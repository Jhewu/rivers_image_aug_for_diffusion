"""
Data Balancer, balances the river image data. It compares the
site with the minimum amount of images (times a multiplier),
to the site with the maximum amount of images. If the multiplier,
does not reach, then the site is ignore. For all of the others that do
meet, apply the data augmentation required to meet the number of images
in the max. We are sacrificing some diversity, in order to get the maximum
amount of data, since diffusion models work well with a lot of data,
to generalize better.

The default augmentations are rotations every 5 degrees, from 5-30,
and then do horizontal flip, and then do 5-30 again. Therefore, we have
a total of 13x multiplier per site ID.

If you want to change the angle of rotations, you can change THETA, but you will 
need to recalculate the factor for upsampling (how much you will need to zoom into
the new image to crop out the padding). 

If you want to change the range of rotations, change MULTIPLIER. If you're doing
5-30 rotations, then it's 6x (from degree 5 to degree 10, there are 6 iterations). 
DO NOT CHANGE TOTAL_MULTIPLIER as it accounts for the original image and the horizontal flip. 
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

"""HYPERPARAMETERS"""
THETA = 5                                       # --> degree of rotations (per augmentation)   
FACT = 1.3                                      # --> multiplication factor to upsample (e.g. zoom into the image)
                                                # If you're using 5 degrees interval, then it takes 1.3x zoom factor on each 
                                                # image to crop out the padding resulted from rotation

                                                # If you change THETA, you must change FACT, recommended
                                                # to keep its default value


MULTIPLIER = 6                                  # If rotations from degree 5-30 (there are 6 iterations).
                                                # this number represnents how many times, we need to iterate
                                                # to reach the final rotation degree
TOTAL_MULTIPLIER = (MULTIPLIER*2) + 1           # DO NOT CHANGE THIS VALUE


FOLDER_LABELS = ["1", "2", "3", "4", "5", "6"]  # the name of the folder

"""------HELPER FUNCTIONS------"""
def Data_augmentation(img, THETA, FACT, flipped):
   """Main Data Augmentation Function"""
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
def DataBalancer(label, THETA, FACT):
    folder_name = f"{label}"
    new_folder_name = f"balanced_{label}"

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
        min = item[1]*MULTIPLIER
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
        theta = THETA
        fact = FACT

        switch_ended = 1                          # ---> after the switch is triggered two times, increase THETA and FACT
        while counter <= image_count_aug:            # --> continue to augment in case rotation or flip rotation is not enough
            #print(f"There are {image_count_aug} images to augment in site {site}, and we are in {counter}")
            for site_img in range(site_ids[site]):
                new_destination = os.path.join(destination, f"{filename_dict[site][site_img]}_augmented_{counter}.JPG")
                if counter > image_count_aug:       # --> if we reached enough images within the loop
                    #print(f"\nBroke when counter was {counter}, and image_count_aug was {image_count_aug}\n")
                    break
                elif switch == -1: #  case 1: only rotations
                    augmented_img = Data_augmentation(site_path[site][site_img], theta, fact, False)
                    cv.imwrite(new_destination, augmented_img)
                    counter+=1
                elif switch == 1:  # case 2: only horizontal flipped rotations
                    augmented_img = Data_augmentation(site_path[site][site_img], theta, fact, True)
                    cv.imwrite(new_destination, augmented_img)
                    counter+=1
            switch = switch*-1
            if switch_ended % 2 == 0:
                theta+=5
                fact+=0.3 # --> these THETA and FACT values ensure no black padding on final image
            switch_ended+=1
        site_number+=1
        #print(f"There are {len(site_path)+1} number of sites, and we are in {site_number}")

    print(f"\n Data balanced is completed for {label}!\n")
    print(f"\n Original dataset contained {total_files} number of images\n")
    print(f"\n Augmented dataset contains {max * (len(sorted_list)+1)} number of images\n")

if __name__ == "__main__":
    print(f"\n-----Balancing/augmenting dataset-----\n")
    for label in FOLDER_LABELS: 
        print(f"\nProcessing label {label}\n")
        DataBalancer(label, THETA, FACT)
    print(f"\n-----Checking if the dataset is balanced-----\n")
    for label in FOLDER_LABELS:
        Data_Is_Balanced(f"balanced_{label}")















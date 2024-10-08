"""
This script analyses a processed labeled 
image folder, and then creates a new folder
with the data balanced through site_ids
"""

import os
import shutil
import random
import cv2 as cv


""" Parameters to change """

# CHANGE THIS ONLY
LABEL = "label_3" 
SITES_TO_EXAMINE = 5 # how many site-ids to examine from least to highest
TOLERANCE = 20       # site-ids without these many images will not be used

# DO NOT CHANGE THESE
folder_name = f"{LABEL}"
new_folder_name = f"balanced_{LABEL}"

""" Simple Horizontal Flip """

def FlipImageAndSave(img, destination): 
    img = cv.imread(img)
    horizontal_flip = cv.flip(img, 1); 
    cv.imwrite(destination, horizontal_flip)

def CreateDir(folder_name): 
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)    

def SortDict(dict):
    # Sort the dictionary by its values
    sorted_items = sorted(dict.items(), key=lambda item: item[1])
    return sorted_items

""" Main Runtime """
def DataBalancer(): 
    """
    SUBJECT TO CHANGE
    
    Data Balancer, balances the data by first obtaining the
    how many images are in the site id with the least amount of
    images, and then balancing it out to other site_id 

    eg. if site_1 = 10 images, then every other site will have 
    10 images
    """

    # obtain image directory
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    image_dir = os.path.join(file_dir, folder_name) 
    dir_list = os.listdir(image_dir)
    
    # declare dictionary to count site_id 
    # notice the difference between site_ids (dict)
        # and site_id (image name)
    site_ids = {}

    # declare dictionary to store the full_paths of 
        # each image within a site id
    site_path = {} # dictionary with a list inside

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
        else:
            site_ids[site_id] = 0
            site_path[site_id] = [full_file_path]

    # check if the length of dictionary is not the same as SITES_TO_EXAMINES
    if len(site_ids) <= SITES_TO_EXAMINE: 
        raise Exception("SITES_TO_EXAMINE greater than the amount of site_ids we have")
    
    sorted_list = SortDict(site_ids) # the sorted dict, is now a list

    # delete site-ids if it does not meet TOLERANCE
    # TURN THIS INTO A FUNCTION
    counter = 0
    for item in sorted_list[:]: # when you delete from the same lists, problems...
        counter+=1 
        print(item)
        if counter == SITES_TO_EXAMINE: 
            break
        elif item[1] < TOLERANCE: 
            del site_path[item[0]]
            del site_ids[item[0]]
            sorted_list.remove(item)
            print("Removed ", item)

    CreateDir(new_folder_name)
    destination = os.path.join(file_dir, new_folder_name)

    image_count = sorted_list[0][1]
    
    # copy image_count amount of images from each site ids
    # onto the new folder
    # TURN THIS INTO A FUNCTION
    for site in site_path: 
        # randomly shuffle the list contents
        # so that the balancing is not deterministic
        random.shuffle(site_path[site])
        for site_img in range(image_count):
            shutil.copy(site_path[site][site_img], destination)
            #print(f"Copied {site_path[site][site_img]} to {destination}")

    print("This is length before augmentation: ", len(site_ids)*image_count)

    image_count_aug = image_count*2

    print(len(site_ids))

    # apply data augmentation (for the remaining images)
    # and meet image_count_aug number of images
    # TURN THIS INTO A FUNCTION
    for site in site_path: 
        random.shuffle(site_path[site])
        for site_img in range(image_count):
            new_destination = os.path.join(destination, f"{site}_horizontal_flip_{site_img}.JPG")
            FlipImageAndSave(site_path[site][site_img], new_destination)
            #print(f"Copied {site_path[site][site_img]} to {destination}")
    
    print("This is the legnth after augmentation: ", len(site_ids)*image_count_aug)

if __name__ == "__main__":
    DataBalancer()








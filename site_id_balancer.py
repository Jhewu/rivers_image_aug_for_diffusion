"""
This script analyses a processed labeled 
image folder, and then creates a new folder
with the data balanced through site_ids
"""

import os
import shutil
import random
import cv2 as cv
import argparse

""" Parameters to change """

# CHANGE THESE ONLY
LABEL = "label_3"
SITES_TO_EXAMINE = 5 # how many site-ids to examine from least to highest
TOLERANCE = 20       # site-ids without these many images will not be used

"""Other Parameters"""

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
    Data Balancer, balances the data by deleting the first
    SITES_TO_EXAMINE sites_ids if it does not meet the TOLERANCE, 
    and then populate a new folder for each site_ids with both
    original images and augmented images (horizontal flip). If 
    the site_ids has more images than the max (max = the site_id 
    with least amount of images * 2, because of horizontal flip), 
    then just copy from the original images. If the site_id has less
    images than the max, then copy the original images and then populate
    the rest with augmented images
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

    # only to keep track of names, for the
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
            site_ids[site_id] = 0
            site_path[site_id] = [full_file_path]
            filename_dict[site_id] = [file_name]

    # check if the length of dictionary is not the same as SITES_TO_EXAMINES
    if len(site_ids) <= SITES_TO_EXAMINE: 
        raise Exception("SITES_TO_EXAMINE greater than the amount of site_ids we have")
    
    sorted_list = SortDict(site_ids) # the sorted dict, is now a list
    og_sorted_list = sorted_list

    # delete site-ids if it does not meet TOLERANCE
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

    max = sorted_list[0][1]*2
    
    # copy image_count amount of images from each site ids
    # onto the new folder, and augment the rest to meet the 
    # max amount of images
    for site in site_path: 
        # randomly shuffle the list contents
        # so that the balancing is not deterministic
        random.shuffle(site_path[site])

        if site_ids[site] < max:
            # copy all the original images
            for site_img in range(site_ids[site]):
                shutil.copy(site_path[site][site_img], destination)
                print(f"Copied {site_path[site][site_img]} to {destination}")
            
            # shuffle 1 more time
            random.shuffle(site_path[site])

            # already used all of the original images
            # ... now duplicate the original images, 
            # to reach the max
            image_count_aug = max - site_ids[site]

            for site_img in range(image_count_aug): 
                new_destination = os.path.join(destination, f"{filename_dict[site][site_img]}_horizontal_flip_{site_img}.JPG") #CHANGE THIS LATER FOR THE FULL NAME
                FlipImageAndSave(site_path[site][site_img], new_destination)
                print(f"Augmented {site_path[site][site_img]} to {destination}")

        else: # if site_ids[site] > image_count
            for site_img in range(max):
                shutil.copy(site_path[site][site_img], destination)
                print(f"Copied {site_path[site][site_img]} to {destination}")

    print("\n This is the original sorted dictionary: \n", og_sorted_list, "\n")

    print("\n This is the current sorted dictionary: \n", sorted_list, "\n")

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Data Balancer")
    #parser.add_argument('-l', '--label', type=str, help='Image Label')
    #args = parser.parse_args()
    #LABEL = args.label
    #print("This is label:", LABEL)
    DataBalancer()





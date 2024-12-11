"""
This script adds the data from site IDs 
that was discarded by the site_id_balancer.py
"""

# Import external libraries
import os
import shutil
import random
import cv2 as cv

"""-----Helper Function-----"""
def SortDict(dict):
   # Sort the dictionary by its value in ascending order
   sorted_items = sorted(dict.items(), key=lambda item: item[1])
   return sorted_items

def CreateDir(folder_name):
   if not os.path.exists(folder_name):
       os.makedirs(folder_name)   

"""------Main Runtime------"""
def AddDiscardedData(label):
    """
    This script copies the data from site IDs that was
    discarded by the site_id_balancer.py into a new directory. 
    For you to combine them together with the balanced dataset, 
    to maximize the amount of data. 
    """
    LABEL = label
    folder_name = f"{LABEL}"
    new_folder_name = f"discarded_{LABEL}"

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

    # print the sorted list
    print(f"this is sorted list {sorted_list}\n")

    # create new directory to copy the images
    CreateDir(new_folder_name)
    destination = os.path.join(file_dir, new_folder_name)

    # transfer the discarded files into a new directory
    total = 0
    for item in sorted_list[:]:
        min = item[1]*23
        if min >= max:
            print(f"All images less than this site {item}, will be copied to {destination}\n")
            break
        else: # min <= max
            # copy the images into the new destination
            for site in range(item[1]): 
                total+=1
                shutil.copy(site_path[item[0]][site], destination)

    print(f"Copied a total of {total} for label {LABEL} images\n")
    print(f"----------\n")
                
if __name__ == "__main__":
    folder_labels = ["1", "2", "3", "4", "5", "6"]
    print(f"\n-----adding discarded data-----\n")
    for label in folder_labels: 
        print(f"\nProcessing label {label}\n")
        AddDiscardedData(label)















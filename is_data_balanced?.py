# Check if the dataset is balanced

import os
import shutil
import random
import cv2 as cv
from math import floor
from math import ceil

def DataBalancer(folder): 
    folder_name = f"{folder}"

    # obtain image directory
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    image_dir = os.path.join(file_dir, folder_name) 
    dir_list = os.listdir(image_dir)

    print("\n Examining this directory: ", image_dir, "\n")
    
    # declare dictionary to count site_id 
    site_ids = {}

    # count site_id and append full_file_path
    total_files = 0
    for file_name in dir_list: 
        total_files += 1
        full_file_path = os.path.join(image_dir, file_name)
        image_name = os.path.basename(full_file_path)
        site_id = image_name.split("_")[0]
    
        if site_id in site_ids: 
            site_ids[site_id] += 1
        else:
            site_ids[site_id] = 0

    # sort the dictionary, and turn it into a list
    a_list = list(site_ids.items()) 

    # count how many images in the list
    for i in range(len(a_list)):
        j = i+1
        if a_list[i][1] != a_list[j][1]:
            print("\nThe dataset is not balanced\n")
            print("\nHere's the distribution: \n")
            print(a_list)
            return

    print("\nThe dataset is balanced \n")
    print("\nHere's the distribution: \n")
    print(a_list)

if __name__ == "__main__":
    folder = "balanced_label_3"
    DataBalancer(folder)


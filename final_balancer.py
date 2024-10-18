""" 
Since the data balancer has a bug where the smaller
site ID has 1 image less than the others, this is 
a temporarily hard code solution to fix the issue
"""

import os
import random

def SortDict(dict):
   # Sort the dictionary by its value in ascending order
   sorted_items = sorted(dict.items(), key=lambda item: item[1])
   return sorted_items

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
            site_ids[site_id] = 1
            site_path[site_id] = [full_file_path]

    # sort the dictionary, and turn it into a list
    a_list = SortDict(site_ids)

    # get the min
    min = a_list[0][1]
    print(f"\nHere's min {min} \n")

    # remove it from the list
    a_list.remove(a_list[0])

    # iterate over the list and remove 1 image per site ID
    for item in a_list: 
        if item[1] > min:
            random.shuffle(site_path[item[0]])
            os.remove(site_path[item[0]][0])

    print(f"Finished balancing your data, check with is_data_balanced?.py")

if __name__ == "__main__":
    folder = "balanced_3"
    DataBalancer(folder)



"""
Accompanying script for site_id_balancer. 
It checks if the balanced and augmented 
image folder is balanced
"""

# import necessary libraries
import os

""" Main Runtime """
def Data_Is_Balanced(folder): 
    folder_name = f"{folder}"

    # obtain image directory
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    image_dir = os.path.join(file_dir, folder_name) 
    dir_list = os.listdir(image_dir)

    print(f"\n---Examining this directory: {image_dir}---\n")
    
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
            site_ids[site_id] = 1

    # sort the dictionary, and turn it into a list
    a_list = sorted(site_ids.items(), key=lambda item: item[1])
    a_length = len(a_list)

    # count how many images in the list
    for i in range(len(a_list)-1):
        j = i+1
        if a_list[i][1] != a_list[j][1]:
            print("\nThe dataset is not balanced\n")
            print("\nHere's the distribution: \n")
            print(a_list)
            return

    print("\nThe dataset is balanced \n")
    print("\nHere's the distribution: \n")
    print(a_list)
    print(f"\nThere should be: {a_length * a_list[0][1]} number of images\n")



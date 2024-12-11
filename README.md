BALANCES RIVER FLOW IMAGES

Data Balancer, balances the data by comparing the
site with the minimum amount of images (with a multiplier),
to the site with the maximum amount of images. If the multiplier,
does not reach, then ignore this site. For all of the others that do meet, apply the data augmentation required to meet the number of images in the max. We are sacrificing some diversity, in order to get the maximum amount of data, since diffusion models work well with a lot of data, to generalize better.

The specific augmentations are rotations every 5 degrees, from 5-60, and then do horizontal flip, and then do 5-60 again. Therefore, we have a total of 23x multiplier per site ID.

site_id_balancer.py works alongside with data_is_balanced.py. Meanwhile use add_discarded_data.py back onto the dataset in order to maximize the amount of data onto the dataset.
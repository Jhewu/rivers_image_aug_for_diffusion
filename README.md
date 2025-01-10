# Site ID Balancer/Augmentation (for Diffusion Models)

This repository contains a tool that balances and performs the necessary image augmentations (e.g., 5-degree rotations + horizontal flips) on river stream images from CT DEEP, to prepare the dataset for diffusion model training. Since the dataset is unbalanced, training it directly (without augmentation) may cause the diffusion model to generate more images from certain site IDs. To compensate for this, we augment the dataset, ensuring a balanced distribution for training.

## The Augmentation Process

The default augmentation process includes:
- **Rotations**: Every 5 degrees, from 5 to 30 degrees.
- **Horizontal flip**: Applied before moving to the next degree of rotation.

The script augments all images from each `site_id` folder until the number of images matches the folder with the maximum number of images. If there are not enough unique augmentations to match the maximum number of images, the process will stop after running out of available augmentations. This ensures that all `site_ids` are adequately represented in the dataset.

## How to Use

The script takes several input arguments:

- **in_dir**: (required) The directory containing labeled folders (e.g., `1`, `2`, ... `6`).
- **out_dir** (optional): The directory where augmented images will be saved. If not provided, the augmented images will be saved in the `in_dir`.
- **labels** (default = 3): The number of labels (site IDs) to balance and augment. For example:
  - If `labels=3`, the script will augment labels `1`, `2`, and `3`.
  - If `labels=6`, the script will augment labels `1` through `6`.
- **theta** (default = 5): The angle of rotation in degrees. If you change `theta`, you should also adjust the `fact` parameter to ensure the image is properly cropped after rotation. The default setting of 5-degree intervals requires a `fact` of 1.3 to account for the padding caused by rotation.
- **fact** (default = 1.3): The zoom factor applied after rotation to crop out any black padding that may result from the image rotation.
- **multiplier** (default = 6): The number of rotations to apply. If `multiplier=6`, the image will be rotated from 5 to 30 degrees, with horizontal flips in between, resulting in a final multiplier of 13x for each image.

### Example Usage
```bash
python3 site_id_balancer.py --in_dir /path/to/images --labels 3 --theta 5 --fact 1.3 --multiplier 6

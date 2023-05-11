import numpy as np
import sys
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import load_model
from PIL import Image
import matplotlib.pyplot as plt
from random import randint
import imageio
import argparse
from skimage.util.shape import view_as_blocks

# Construct argument parser
parser = argparse.ArgumentParser(description='Use block shuffle')
parser.add_argument('--shuffle', action='store_true', default=False)
parser.add_argument("--model", required=True, help="path to trained model")
parser.add_argument("--container_image", required=True, help="path to container image")
args = vars(parser.parse_args())

'''
Retrieves secret image from container image
Input: Container Image, Reveal Model
Output: Secret Image
'''

# Load the model
model_reveal = load_model(args['model'], compile=False)


# Normalize inputs
def normalize_batch(images):
    """Performs channel-wise z-score normalization"""

    return (images - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])


# Denormalize outputs
def denormalize_batch(images, should_clip=True):
    images = (images * np.array([0.229, 0.224, 0.225])) + np.array([0.485, 0.456, 0.406])

    if should_clip:
        images = np.clip(images, 0, 1)
    return images


# Custom block shuffling
def shuffle(img, inverse=False):
    # Configure block size, rows and columns
    blk_size = 56
    rows = np.uint8(img.shape[0] / blk_size)
    cols = np.uint8(img.shape[1] / blk_size)

    # Create a block view on image
    img_blocks = view_as_blocks(img, block_shape=(blk_size, blk_size, 3)).squeeze()
    img_shuffle = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # Secret key maps
    map = {0: 2, 1: 0, 2: 3, 3: 1}
    inv_map = {v: k for k, v in map.items()}

    # Perform block shuffling
    for i in range(0, rows):
        for j in range(0, cols):
            x, y = i * blk_size, j * blk_size
            if inverse:
                img_shuffle[x:x + blk_size, y:y + blk_size] = img_blocks[inv_map[i], inv_map[j]]
            else:
                img_shuffle[x:x + blk_size, y:y + blk_size] = img_blocks[map[i], map[j]]

    return img_shuffle


# Normalize input images [float: 0-1]
stego_image = np.array(Image.open(args['container_image']).convert('RGB')).reshape(1, 224, 224, 3) / 255.0

# Predict the output
secret_out = model_reveal.predict([normalize_batch(stego_image)])

# Post-process the output
secret_out = denormalize_batch(secret_out)
secret_out = np.squeeze(secret_out) * 255.0
secret_out = np.uint8(secret_out)

# Reshuffle the output
if args["shuffle"] == True:
    secret_out = shuffle(secret_out, inverse=True)

# Save and plot stego image output
imageio.imsave("test/secret_out.png", secret_out)
plt.imshow(secret_out)

'''
Sample run :-
# Without shuffle
python image_reveal.py --model models/reveal.h5 --container_image test/cover_output.png
# With shuffle
python image_reveal.py --model models/reveal.h5 --container_image test/cover_output.png --shuffle 
'''

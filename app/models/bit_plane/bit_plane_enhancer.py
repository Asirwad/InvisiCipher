import cv2
import numpy as np


def enhance(image_path, n):
    # Load the extracted bit plane
    bit_plane = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Convert the bit plane back to its orginal form
    converted_image = bit_plane * (1 << n)

    # Save the converted image
    cv2.imwrite(f'enhanced_final_{n}_bit.png', converted_image)

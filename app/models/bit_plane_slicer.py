import numpy as np


def bit_plane_slicing(image, bit_plane):
    # Convert image to binary
    binary_image = np.unpackbits(image, axis=2)

    # Extract bit plane
    plane = binary_image[..., bit_plane]

    # Convert bit plane back to uint8
    plane = np.packbits(plane, axis=2)

    return plane

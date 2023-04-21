import numpy as np


def bit_plane_slicing(image, bit_plane):
    # Convert image to binary
    binary_image = np.unpackbits(image, axis=2)

    # Extract bit plane
    plane = binary_image[..., bit_plane]

    # Convert bit plane back to uint8
    plane = np.packbits(plane, axis=2)

    return plane


def count_bit_planes(image):
    # Convert the image to grayscale if it's not already
    if image.mode != "L":
        image = image.convert("L")

    # Convert the image to a two-dimensional array of pixel values
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    # Calculate the maximum pixel value in the image
    max_val = max(map(max, pixels))

    # Calculate the number of bits required to represent the maximum value
    bits_required = max_val.bit_length()

    # Return the number of bits required
    return bits_required


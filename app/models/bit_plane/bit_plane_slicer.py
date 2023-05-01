import numpy as np


class BitPlaneProcessor:
    @staticmethod
    def get_bit_plane(image, plane):
        plane_image = np.zeros((image.height, image.width))
        for i in range(image.height):
            for j in range(image.width):
                pixel = image.get_pixel(j, i)
                pixel_value = pixel[0]
                plane_image[i][j] = (pixel_value & (1 << plane)) >> plane
        return plane_image


def count_bit_planes(image):
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

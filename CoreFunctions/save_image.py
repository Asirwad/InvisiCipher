"""
    Save the modified image as a new file.

    Parameters:
        image_pixels (list): A list of tuples representing the modified pixel values of the image.
        image_size (tuple): The size of the original image.
        new_image_path (str): The path to save the new image file.
"""
from PIL import Image


def save_image(image_pixels, image_size, new_image_path):
    new_image = Image.new('RGB', image_size)
    new_image.putdata(image_pixels)
    new_image.save(new_image_path)

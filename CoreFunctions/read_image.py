from PIL import Image
"""
    Read an image file and return its pixel values.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        list: A list of tuples representing the pixel values of the image.
    """
def read_image(image_path):
    with Image.open(image_path) as img:
        pixels = list(img.getdata())
    return pixels


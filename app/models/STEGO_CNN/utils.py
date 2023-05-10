import numpy as np
from PIL import Image


def read_files(cover_image_path, secret_file_path):
    cover_image = Image.open(cover_image_path)
    secret_file = Image.open(secret_file_path)
    return cover_image, secret_file


def convert_to_pixels(image):
    pixels = np.array(image)
    return pixels.flatten()


def concatenate_vectors(cover_image_vector, secret_file_vector):
    concat = np.concatenate((cover_image_vector, secret_file_vector))
    return concat

import numpy as np
from PIL import Image


def hide_secret_file(model, concatenated_vector):
    steg_image_vector = model.predict(concatenated_vector)
    steg_image_pixels = steg_image_vector.reshape((256, 256, 3))
    steg_image = Image.fromarray(steg_image_pixels.astype(np.uint8))


def retrieve_secret_file(model, steg_image_vector, secret_file_vector_shape):
    retrieved_secret_file_vector = model.predict(steg_image_vector)
    retrieved_secret_file = retrieved_secret_file_vector[:secret_file_vector_shape].tobytes()
    return retrieved_secret_file

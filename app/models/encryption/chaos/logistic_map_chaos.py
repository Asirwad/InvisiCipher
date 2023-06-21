import cv2
import numpy as np
from tkinter import filedialog


def encrypt(image_path, key):
    img = cv2.imread(image_path)

    # Get the dimensions of the image
    rows, cols, _ = img.shape

    # Create a copy of the image to store the encrypted image
    encrypted_img = np.zeros_like(img)

    # Set the initial conditions of the logistic map
    x = key
    r = 4

    # Iterate over each pixel in the image
    for i in range(rows):
        for j in range(cols):
            # Generate a pseudo-random number using the logistic map
            x = r * x * (1 - x)

            # Normalize the logistic map value to [0, 1]
            normalized_value = x - np.floor(x)

            # Encrypt each color channel value using XOR
            encrypted_img[i, j, 0] = img[i, j, 0] ^ int(normalized_value * 255)
            encrypted_img[i, j, 1] = img[i, j, 1] ^ int(normalized_value * 255)
            encrypted_img[i, j, 2] = img[i, j, 2] ^ int(normalized_value * 255)

    # Save the encrypted image
    cv2.imwrite('output_encrypted.png', encrypted_img)


def decrypt(image_path, key):
    # Load the encrypted image
    encrypted_image = cv2.imread(image_path)

    # Get the dimensions of the image
    rows, cols, _ = encrypted_image.shape

    # Create a copy of the image to store the decrypted version
    decrypted_image = np.zeros_like(encrypted_image)

    # Set the initial conditions for the logistic map
    x = key
    r = 4

    # Iterate over each pixel in the image
    for i in range(rows):
        for j in range(cols):
            # Generate a pseudo-random number using the logistic map
            x = r * x * (1 - x)

            # Normalize the logistic map value to [0, 1]
            normalized_value = x - np.floor(x)

            # Decrypt each color channel value using XOR
            decrypted_image[i, j, 0] = encrypted_image[i, j, 0] ^ int(normalized_value * 255)
            decrypted_image[i, j, 1] = encrypted_image[i, j, 1] ^ int(normalized_value * 255)
            decrypted_image[i, j, 2] = encrypted_image[i, j, 2] ^ int(normalized_value * 255)

    # Save the decrypted image
    cv2.imwrite('output_decrypted.png', decrypted_image)


print("input the image filename")
filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
encrypt(filename,4)

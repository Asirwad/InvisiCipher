import cv2
import numpy as np


def encrypt(image_path, key):
    img = cv2.imread(image_path)

    # convert the image to greyscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get the dimensions of the image
    rows, cols = gray.shape

    # create a copy of the image to store the encrypted image
    encrypted_img = np.zeros_like(gray)

    # set the initial conditions of the logistic map
    x = key
    r = 4

    # Iterate over each pixel in the image
    for i in range(rows):
        for j in range(cols):
            # Generate a pseudo random number using logistic map
            x = r * x * (1 - x)
            # Encrypt the pixel value using XOR
            encrypted_img[i, j] = int(gray[i, j]) ^ int(x * 256)

    # Save the encrypted image
    cv2.imwrite('output_encrypted.png', encrypted_img)


def decrypt(image_path, key):
    # Load the encrypted image
    encrypted_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Get the dimensions of the image
    rows, cols = encrypted_image.shape

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
            # Decrypt the pixel value using XOR
            decrypted_image[i, j] = int(encrypted_image[i, j]) ^ int(x * 256)

    # Save the encrypted image
    cv2.imwrite('output_decrypted.png', decrypted_image)

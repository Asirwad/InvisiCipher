import numpy as np
from PIL import Image
from tkinter import filedialog


def logistic_map(x, r):
    return r*x*(1-x)


def encrypt(image_path):
    r, x0 = 3.9, 0.5
    # Load the image
    img = Image.open(image_path)

    # Convert the image to RGB mode
    img = img.convert("RGB")

    # Resize the image to 224x224 pixels
    img = img.resize((224, 224))

    # Convert the image to a NumPy array
    pixels = np.array(img)

    # Flatten the array
    pixels = pixels.reshape(-1, 3)

    # Generate the chaotic sequence for each channel
    sequences = []
    for _ in range(3):
        sequence = []
        x = x0
        for _ in range(len(pixels)):
            x = logistic_map(x, r)
            sequence.append(x)
        sequences.append(sequence)

    # Expand the sequences for key generation
    expanded_sequences = np.array(sequences) * 255

    # Transpose and reshape the expanded sequences to match the shape of pixels
    expanded_sequences = expanded_sequences.transpose(1, 0).reshape(pixels.shape)

    # Encrypt each pixel
    encrypted_pixels = np.bitwise_xor(pixels, expanded_sequences.astype(int))

    # Permute the encrypted pixels
    permutation_indices = np.random.permutation(len(encrypted_pixels))
    encrypted_pixels = encrypted_pixels[permutation_indices]

    # Reshape the encrypted pixels back to the original image shape
    encrypted_pixels = encrypted_pixels.reshape(img.size[0], img.size[1], 3)

    # Create an encrypted image from the encrypted pixels
    encrypted_image = Image.fromarray(encrypted_pixels.astype('uint8'), "RGB")

    # save the encrypted image
    encrypted_image.save("output_encrypted.png")


def decrypt(image_path):
    r, x0 = 3.9, 0.5
    # Load the encrypted image
    encrypted_img = Image.open(image_path)

    # Convert the image to a NumPy array
    encrypted_pixels = np.array(encrypted_img)

    # Flatten the array
    encrypted_pixels = encrypted_pixels.reshape(-1, 3)

    # Reverse the permutation step
    permutation_indices = np.argsort(np.random.permutation(len(encrypted_pixels)))
    encrypted_pixels = encrypted_pixels[permutation_indices]

    # Generate the chaotic sequence for each channel
    sequences = []
    for _ in range(3):
        sequence = []
        x = x0
        for _ in range(len(encrypted_pixels)):
            x = logistic_map(x, r)
            sequence.append(x)
        sequences.append(sequence)

    # Expand the sequences for key generation
    expanded_sequences = np.array(sequences) * 255

    # Transpose and reshape the expanded sequences to match the shape of encrypted_pixels
    expanded_sequences = expanded_sequences.transpose(1, 0).reshape(encrypted_pixels.shape)

    # Decrypt each pixel
    decrypted_pixels = np.bitwise_xor(encrypted_pixels, expanded_sequences.astype(int))

    # Reshape the decrypted pixels back to the original image shape
    decrypted_pixels = decrypted_pixels.reshape(encrypted_img.size[0], encrypted_img.size[1], 3)

    # Create a decrypted image from the decrypted pixels
    decrypted_image = Image.fromarray(decrypted_pixels.astype('uint8'), "RGB")

    # save the encrypted image
    decrypted_image.save("output_decrypted.png")


print("input the image filename")
filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
decrypt(filename)
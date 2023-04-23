from tkinter import filedialog
import numpy as np
from PIL import Image

from app.models.bit_plane.bit_plane_slicer import BitPlaneProcessor
from app.models.bit_plane.image import ImageProcessor
from app.models.encryption.chaos import logistic_map_chaos, aes_chaos
from app.models.encryption import blowfish
from app.models.bit_plane import bit_plane_enhancer

""" Bit-plane slicing """

# Load the input image
filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
image = ImageProcessor(filename)
num_of_bit_planes = image.num_bit_planes
plane_image = BitPlaneProcessor.get_bit_plane(image, (num_of_bit_planes * 2) - 1)
# Save output
output_filename = "output_sliced.png"
plane_image_pil = Image.fromarray(np.uint8(plane_image * 255))
plane_image_pil.save(output_filename)
print(f"Sliced output saved to {output_filename}")

print("1. AES")
print("2. logistic map encryption")
print("3. Blowfish")
enc_choice = int(input("What type of encryption do you want? :"))
print("Your choice is : ", enc_choice)

if enc_choice == 1:
    # AES Encryption
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    key = input("Enter your secret key : ")
    aes_chaos.encrypt(filename, key)

    # AES Decryption
    print("AES Decryption")
    key = input("Enter your secret key : ")
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("All files", "*.*"), ("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png")))
    aes_chaos.decrypt(filename, key)

elif enc_choice == 2:
    # logistic map encryption
    key = 0.1
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    logistic_map_chaos.encrypt(filename, key)
    print("Encrypted output saved to output_encrypted.png")

    # logistic map decryption
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    logistic_map_chaos.decrypt(filename, key)
    print("Encrypted output saved to output_decrypted.png")

elif enc_choice == 3:
    print("Hello")
    # Blowfish Encryption
    key = input("Enter your secret key : ")
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    blowfish.encrypt(filename, key)
    print("Encrypted output saved to output_encrypted.png")

    # Blowfish Decryption
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    key = input("Enter your secret key : ")
    blowfish.decrypt(filename, key)

else:
    print('Invalid choice')

"""n-1 bit only to n-bit image"""
filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
image = ImageProcessor(filename)
num_of_bit_planes = image.num_bit_planes
bit_plane_enhancer.enhance(filename, num_of_bit_planes)

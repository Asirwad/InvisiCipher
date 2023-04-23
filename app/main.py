import io
import secrets
from tkinter import filedialog
import numpy as np
from PIL import Image

from app.models.bit_plane.bit_plane_slicer import BitPlaneProcessor
from app.models.bit_plane.image import ImageProcessor
from app.models.chaos import logistic_map_chaos

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
"""
 AES Encryption 

filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
image = Image.open(filename)

key = secrets.token_bytes(16)
print("key = ", key)

iv, encrypted_image = aes_chaos.encrypt(image, key)
print("IV = ", iv)
encrypted_image.show()
output_filename = "output_encrypted.png"
encrypted_image.save(output_filename)
print(f"Encrypted output saved to {output_filename}")

 AES Decryption 
filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
image = Image.open(filename)
decrypted_image = aes_chaos.decrypt(encrypted_image, key, iv)
decrypted_image.show()
"""

# logistic map encryption
key = 0.1
filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
logistic_map_chaos.encrypt(filename, key)
print("Encrypted output saved to output_encrypted.png")

# logistic map decryption
filename = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
logistic_map_chaos.decrypt(filename, key)
print("Encrypted output saved to output_decrypted.png")

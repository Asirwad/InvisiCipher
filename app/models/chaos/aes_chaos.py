import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import io
from PIL import Image


def encrypt(image, key):
    # convert the image to bytes
    with io.BytesIO() as output:
        image.save(output, format=image.format)
        image_bytes = output.getvalue()
    # Encryption object
    cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
    # generating random initialization vector (IV)
    iv = cipher.iv
    padded_image = pad(image_bytes, 16)
    encrypted_image = cipher.encrypt(padded_image)
    # convert encrypted image bytes to image format
    encrypted_image_array = np.frombuffer(encrypted_image, dtype=np.uint8)
    encrypted_image_pil = Image.fromarray(encrypted_image_array)
    return iv, encrypted_image_pil


def decrypt(encrypted_image, key, iv):
    # convert the image to bytes
    with io.BytesIO() as output:
        encrypted_image.save(output, format=encrypted_image.format)
        image_bytes = output.getvalue()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_image = cipher.decrypt(image_bytes)
    unpadded_image = unpad(decrypted_image, 16)
    # convert bytes to image
    image = Image.open(io.BytesIO(unpadded_image))
    return image

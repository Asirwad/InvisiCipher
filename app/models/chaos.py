import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os


def aes_encrypt(image, key):
    # Encryption object
    cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
    # generating random initialization vector (IV)
    iv = cipher.iv
    padded_image = pad(image, AES.block_size)
    encrypted_image = cipher.encrypt(padded_image)
    return iv, encrypted_image


def aes_decrypt(encrypted_image, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_image = cipher.decrypt(encrypted_image)
    unpadded_image = unpad(decrypted_image, AES.block_size)
    return unpadded_image


def xor_encrypt(image, key):
    np.random.seed(key)
    mask = np.random.randint(256, size=image.shape, dtype=np.uint8)
    encrypted_image = np.bitwise_xor(image, mask)
    return mask, encrypted_image


def xor_decrypt(encrypted_image, key, mask):
    np.random.seed(key)
    decrypted_image = np.bitwise_xor(encrypted_image, mask)
    return decrypted_image

from tkinter import filedialog

from app.models.encryption import blowfish
from app.models.DEEP_STEGO.hide_image import hide_image
from app.models.DEEP_STEGO.reveal_image import reveal_image
from app.models.ESRGAN.upscale_image import upscale_image
from app.models.encryption import aes as aes_chaos

print("InvisiCipher CLI")

""" DEEP STEGANO """
print("Image hiding")
print("input the cover image filename")
cover_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
print("input the secret image filename")
secret_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
hide_image(cover_filename, secret_filename)

print("image hidden successfully\n\n")


print("1. AES")
print("2. Blowfish")
enc_choice = int(input("What type of encryption do you want? :"))
print("Your choice is : ", enc_choice)

if enc_choice == 1:
    # AES Encryption
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    key = input("Enter your secret key : ")
    aes_chaos.encrypt(filename, key)

    # AES Decryption
    print("AES Decryption")
    key = input("Enter your secret key : ")
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("All files", "*.*"), ("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png")))
    aes_chaos.decrypt(filename, key)


elif enc_choice == 2:
    print("Blowfish Encryption")
    # Blowfish Encryption
    key = input("Enter your secret key : ")
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    blowfish.encrypt(filename, key)
    print("Encrypted output saved to output_encrypted.png")

    # Blowfish Decryption
    filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
    key = input("Enter your secret key : ")
    blowfish.decrypt(filename, key)

else:
    print('Invalid choice')

print("input the steg image filename")
steg_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
reveal_image(steg_filename)

""" UP-SCALING """
print("UP-SCALING")
print("input the low res image filename")
low_res_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
upscale_image(low_res_filename)




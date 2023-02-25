"""
    Embed the binary representation of a message into the least significant bits
    of the pixel values of an image.

    Parameters:
        image_pixels(list): A list of tuples representing the pixel values of the image.
        message_binary(str): The binary representation of the message to be embedded.

    Returns:
        list: A list of tuples representing the modified pixel values of the image.
"""


def embed_message(image_pixels, message_binary):
    # Copy the original pixel values to avoid modifying the original list
    new_pixels = list(image_pixels)

    # Convert the message binary string to a list of bits
    bits = [int(bit) for bit in message_binary.replace(' ', ' ')]

    # Embed the bits into the least significant bits of the pixel values
    for i in range(len(bits)):
        pixel = list(new_pixels[i])
        pixel[-1] = bits[i]
        new_pixels[i] = tuple(pixel)

    return new_pixels

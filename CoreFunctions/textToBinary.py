"""Convert the input text into binary format

Parameters :
    text(str): The text to be converted
Returns :
    str: The binary representation of the input text
"""


def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

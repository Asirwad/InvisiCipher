import requests
import io
import json
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"


def generate(text_prompt):
	with open("C:/Users/asirw/PycharmProjects/InvisiCipher/app/models/StableDiffusionAPI/Key.json") as file:
		key = json.load(file)[0]
	response = requests.post(API_URL, headers={"Authorization": key}, json={"inputs": text_prompt})
	return Image.open(io.BytesIO(response.content))


"""
text = input("Your sentence here:")
image = generate(text)
image.show()
"""
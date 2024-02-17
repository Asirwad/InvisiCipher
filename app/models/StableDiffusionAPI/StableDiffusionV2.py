import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}


def generate(text_prompt):
	response = requests.post(API_URL, headers=headers, json={"inputs": text_prompt})
	return Image.open(io.BytesIO(response.content))


"""
text = input("Your sentence here:")
image = generate(text)
image.show()"""
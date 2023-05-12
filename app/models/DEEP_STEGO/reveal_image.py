import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import imageio
from tkinter import filedialog
from app.models.DEEP_STEGO.Utils.preprocessing import normalize_batch, denormalize_batch


def reveal_image(stego_image_filepath):
    model = load_model("./models/reveal.h5", compile=False)

    stego_image = Image.open(stego_image_filepath).convert('RGB')

    # Resize the image to 224px*224px
    if stego_image.size != (224, 224):
        stego_image = stego_image.resize((224, 224))
        print("stego_image was resized to 224px * 224px")

    stego_image = np.array(stego_image).reshape(1, 224, 224, 3) / 255.0

    secret_image_out = model.predict([normalize_batch(stego_image)])

    secret_image_out = denormalize_batch(secret_image_out)
    secret_image_out = np.squeeze(secret_image_out) * 255.0
    secret_image_out = np.uint8(secret_image_out)

    imageio.imsave("test/secret_out.png", secret_image_out)
    print("Saved revealed image to secret_out.png")

    return



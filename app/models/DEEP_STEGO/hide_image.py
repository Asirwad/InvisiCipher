import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import imageio
from tkinter import filedialog
from app.models.DEEP_STEGO.Utils.preprocessing import normalize_batch, denormalize_batch


def hide_image(cover_image_filepath, secret_image_filepath):
    model = load_model("./models/hide.h5")

    secret_image_in = Image.open(secret_image_filepath).convert('RGB')
    cover_image_in = Image.open(cover_image_filepath).convert('RGB')

    # Resize if image to 224px*224px
    if secret_image_in.size != (224, 224):
        secret_image_in = secret_image_in.resize((224, 224))
        print("secret_image was resized to 224px * 224px")
    if cover_image_in.size != (224, 224):
        cover_image_in = cover_image_in.resize((224, 224))
        print("cover_image was resized to 224px * 224px")

    secret_image_in = np.array(secret_image_in).reshape(1, 224, 224, 3) / 255.0
    cover_image_in = np.array(cover_image_in).reshape(1, 224, 224, 3) / 255.0

    steg_image_out = model.predict([normalize_batch(secret_image_in), normalize_batch(cover_image_in)])

    steg_image_out = denormalize_batch(steg_image_out)
    steg_image_out = np.squeeze(steg_image_out) * 255.0
    steg_image_out = np.uint8(steg_image_out)

    imageio.imsave('test/steg_image.png', steg_image_out)
    print("Saved steg image to steg_image.png")

    return

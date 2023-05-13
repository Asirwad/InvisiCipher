import math
import sys
import numpy as np
import cv2
from tkinter import filedialog
from tensorflow.keras.models import load_model
from app.models.DEEP_STEGO.Utils.preprocessing import normalize_batch, denormalize_batch


def update_progress(current_frame, total_frames):
    progress = math.ceil((current_frame/total_frames)*100)
    sys.stdout.write('\rProgress: [{0}] {1}%'.format('>'*math.ceil(progress/10), progress))


def hide_video(cover_vid_filepath, secret_vid_filepath):
    model = load_model('./models/hide.h5')

    vid_cap_cover = cv2.VideoCapture(cover_vid_filepath)
    vid_cap_secret = cv2.VideoCapture(secret_vid_filepath)

    print("\nEncoding video.....")

    num_frames = int(vid_cap_cover.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Total number of frames in the video : ", num_frames)

    steg_out_vid = cv2.VideoWriter('results/steg_vid.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, (224, 224))

    secret_batch = []
    cover_batch = []
    frame = 0

    while True:
        (success1, secret) = vid_cap_secret.read()
        (success2, cover) = vid_cap_cover.read()

        if not (success1 and success2):
            break

        secret = cv2.resize(cv2.cvtColor(secret, cv2.COLOR_BGR2RGB), (224, 224), interpolation=cv2.INTER_AREA)
        cover = cv2.resize(cv2.cvtColor(cover, cv2.COLOR_BGR2RGB), (224, 224), interpolation=cv2.INTER_AREA)

        secret_batch.append(secret)
        cover_batch.append(cover)

        frame = frame + 1
        if frame % 4 == 0:
            secret_batch = np.float32(secret_batch)/255.0
            cover_batch = np.float32(cover_batch)/255.0

            steg_out = model.predict([normalize_batch(secret_batch), normalize_batch(cover_batch)])

            steg_out = denormalize_batch(steg_out)
            steg_out = np.squeeze(steg_out)*255.0
            steg_out = np.uint8(steg_out)

            for i in range(0, 4):
                steg_out_vid.write(steg_out[i][..., ::-1])

            secret_batch = []
            cover_batch = []

            update_progress(frame, num_frames)

    # to make progress bar to 100%
    update_progress(num_frames, num_frames)
    print("\nSuccessfully encoded the video")

    vid_cap_cover.release()
    vid_cap_secret.release()
    cv2.destroyAllWindows()


print("input the cover video filename")
cover_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
print("You selected :", cover_filename)
print("input the secret video filename")
secret_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
print("You selected :", secret_filename)
hide_video(cover_filename, secret_filename)
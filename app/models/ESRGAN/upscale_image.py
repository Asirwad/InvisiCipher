from tkinter import filedialog
import cv2
import numpy as np
import torch
import os
from app.models.ESRGAN import RRDBNet_arch as arch


def upscale_image(image_filepath):
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:400"
    model_path = 'models/RRDB_ESRGAN_x4.pth'
    device = torch.device('cuda')

    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device)

    print('Model path {:s}. \nUp-scaling...'.format(model_path))

    image = cv2.imread(image_filepath, cv2.IMREAD_COLOR)
    image = image * 1.0 / 255
    image = torch.from_numpy(np.transpose(image[:, :, [2, 1, 0]], (2, 0, 1))).float()
    image_low_res = image.unsqueeze(0)
    image_low_res = image_low_res.to(device)

    with torch.no_grad():
        image_high_res = model(image_low_res).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    image_high_res = np.transpose(image_high_res[[2, 1, 0], :, :], (1, 2, 0))
    image_high_res = (image_high_res * 255.0).round()
    cv2.imwrite('upscaled.png', image_high_res)
    print("image saved as upscaled.png")

    return


print("input the low res image filename")
low_res_filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")))
upscale_image(low_res_filename)

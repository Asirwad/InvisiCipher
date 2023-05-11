import numpy as np


# Preprocessing functions
def normalize_batch(images):
    """Performs channel-wise z-score normalization"""

    return (images - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])


def denormalize_batch(images, should_clip=True):
    """Denormalize the images for prediction"""

    images = (images * np.array([0.229, 0.224, 0.225])) + np.array([0.485, 0.456, 0.406])

    if should_clip:
        images = np.clip(images, 0, 1)
    return images

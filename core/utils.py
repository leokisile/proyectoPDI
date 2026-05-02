import numpy as np


def normalizar(img):
    return (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
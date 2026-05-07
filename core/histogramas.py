import cv2
import numpy as np


# ============================
# HISTOGRAMA ESCALA DE GRISES
# ============================

def histograma_grises(img):

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([img], [0], None, [256], [0, 256]).flatten()

    return hist


# ============================
# HISTOGRAMA RGB
# ============================

def histograma_rgb(img):

    if img is None:
        print("La imagen no existe")
        return None, None, None

    if len(img.shape) == 2:
        print("La imagen está en grises")
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    b, g, r = cv2.split(img)
    print(b,g,r)

    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256]).flatten()
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256]).flatten()
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256]).flatten()

    return hist_b, hist_g, hist_r
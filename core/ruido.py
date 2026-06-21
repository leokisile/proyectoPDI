# ruido.py

import numpy as np
import cv2


def ruido_sal_pimienta(img, prob=0.05):

    resultado = img.copy()

    h, w = img.shape[:2]

    mascara = np.random.rand(h, w)

    resultado[mascara < prob/2] = 0

    resultado[
        (mascara >= prob/2) &
        (mascara < prob)
    ] = 255

    return resultado

def ruido_gaussiano(
    img,
    media=0,
    sigma=25
):

    ruido = np.random.normal(
        media,
        sigma,
        img.shape
    )

    resultado = img.astype(np.float32) + ruido

    return np.clip(
        resultado,
        0,
        255
    ).astype(np.uint8)

def ruido_multiplicativo(
    img,
    sigma=0.2
):

    ruido = np.random.normal(
        0,
        sigma,
        img.shape
    )

    resultado = img.astype(np.float32)

    resultado = resultado + resultado * ruido

    return np.clip(
        resultado,
        0,
        255
    ).astype(np.uint8)
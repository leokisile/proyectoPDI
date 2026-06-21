# binarizacion.py

import cv2
import numpy as np
from scipy.signal import find_peaks


def _to_gray(img):
    """
    Convierte a escala de grises si la imagen tiene 3 canales.
    """
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def otsu(img):
    """
    Binarización mediante Otsu.
    """
    gray = _to_gray(img)

    _, resultado = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return resultado


def entropia_kapur(img):
    """
    Binarización mediante el método de Kapur.
    """
    gray = _to_gray(img)

    histograma = cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    ).flatten()

    total_pixeles = gray.size

    max_entropia = -np.inf
    umbral_optimo = 0

    for t in range(1, 255):

        clase1 = histograma[:t]
        clase2 = histograma[t:]

        p1 = np.sum(clase1) / total_pixeles
        p2 = np.sum(clase2) / total_pixeles

        if p1 <= 0 or p2 <= 0:
            continue

        n1 = clase1 / (np.sum(clase1) + 1e-10)
        n2 = clase2 / (np.sum(clase2) + 1e-10)

        entropia1 = -np.sum(n1 * np.log(n1 + 1e-10))
        entropia2 = -np.sum(n2 * np.log(n2 + 1e-10))

        entropia_total = p1 * entropia1 + p2 * entropia2

        if entropia_total > max_entropia:
            max_entropia = entropia_total
            umbral_optimo = t

    resultado = np.where(
        gray >= umbral_optimo,
        255,
        0
    ).astype(np.uint8)

    return resultado


def minimo_histograma(img):
    """
    Método del mínimo del histograma.
    Busca dos picos principales y utiliza
    el valle entre ellos como umbral.
    """
    gray = _to_gray(img)

    histograma = cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    ).flatten()

    picos, _ = find_peaks(
        histograma,
        distance=20
    )

    if len(picos) < 2:
        return otsu(gray)

    pico1 = picos[0]
    pico2 = picos[1]

    umbral = (
        np.argmin(histograma[pico1:pico2])
        + pico1
    )

    resultado = np.where(
        gray > umbral,
        255,
        0
    ).astype(np.uint8)

    return resultado


def umbral_media(img):
    """
    Binarización usando la media
    de las intensidades.
    """
    gray = _to_gray(img)

    umbral = np.mean(gray)

    resultado = np.where(
        gray >= umbral,
        255,
        0
    ).astype(np.uint8)

    return resultado


def multiples_umbrales(img, t1=80, t2=150):
    """
    Segmentación multinivel.
    Devuelve tres regiones:
    0, 127 y 255.
    """
    gray = _to_gray(img)

    resultado = np.zeros_like(gray)

    resultado[gray < t1] = 0
    resultado[(gray >= t1) & (gray < t2)] = 127
    resultado[gray >= t2] = 255

    return resultado.astype(np.uint8)


def umbral_banda(img, t1=80, t2=150):
    """
    Conserva únicamente los píxeles
    comprendidos entre t1 y t2.
    """
    gray = _to_gray(img)

    resultado = np.zeros_like(gray)

    resultado[
        (gray >= t1) &
        (gray <= t2)
    ] = 255

    return resultado.astype(np.uint8)
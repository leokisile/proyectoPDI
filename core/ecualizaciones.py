# ecualizaciones.py

import cv2
import numpy as np


def _to_gray(img):
    """
    Convierte a escala de grises si la imagen tiene 3 canales.
    """
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def ecualizacion_histograma(img):
    """
    Ecualización clásica del histograma.
    """
    gray = _to_gray(img)
    return cv2.equalizeHist(gray)


def ecualizacion_uniforme(img):
    """
    Ecualización uniforme.
    """
    gray = _to_gray(img)
    return cv2.equalizeHist(gray)


def ecualizacion_exponencial(img):
    """
    Transformación exponencial.
    """
    gray = _to_gray(img)

    resultado = 255 * (1 - np.exp(-gray.astype(np.float32) / 255.0))

    return np.uint8(np.clip(resultado, 0, 255))


def ecualizacion_rayleigh(img):
    """
    Transformación basada en distribución de Rayleigh.
    """
    gray = _to_gray(img)

    resultado = 255 * np.sqrt(gray.astype(np.float32) / 255.0)

    return np.uint8(np.clip(resultado, 0, 255))


def ecualizacion_hipercubica(img):
    """
    Transformación hipercúbica.
    """
    gray = _to_gray(img)

    resultado = 255 * (gray.astype(np.float32) / 255.0) ** 4

    return np.uint8(np.clip(resultado, 0, 255))


def ecualizacion_logaritmica_hiperbolica(img):
    """
    Transformación logarítmica hiperbólica.
    """
    gray = _to_gray(img)

    resultado = (
        255
        * np.log1p(gray.astype(np.float32))
        / np.log1p(255)
    )

    return np.uint8(np.clip(resultado, 0, 255))


def funcion_potencia(img, potencia=2.0):
    """
    Transformación de potencia.
    """
    gray = _to_gray(img)

    resultado = 255 * (gray.astype(np.float32) / 255.0) ** potencia

    return np.uint8(np.clip(resultado, 0, 255))


def correccion_gamma(img, gamma=1.5):
    """
    Corrección Gamma.
    gamma > 1 oscurece.
    gamma < 1 aclara.
    """
    gray = _to_gray(img)

    resultado = np.power(
        gray.astype(np.float32) / 255.0,
        gamma
    ) * 255

    return np.uint8(np.clip(resultado, 0, 255))
import cv2
import numpy as np


# ============================
# UTILIDAD INTERNA
# ============================

def preparar_imagenes(img1, img2):
    """
    Ajusta tamaño y canales para operaciones lógicas.
    """

    # Ajustar tamaño
    if img1.shape[:2] != img2.shape[:2]:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Ajustar canales
    if len(img1.shape) != len(img2.shape):

        # img1 gris y img2 color
        if len(img1.shape) == 2:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # img1 color y img2 gris
        else:
            img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    return img1, img2


# ============================
# OPERACIONES LÓGICAS
# ============================

def and_logico(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    return cv2.bitwise_and(img1, img2)


def or_logico(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    return cv2.bitwise_or(img1, img2)


def xor_logico(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    return cv2.bitwise_xor(img1, img2)


def not_logico(img):

    return cv2.bitwise_not(img)


# ============================
# OPERACIONES ARITMÉTICAS
# ============================

def suma(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    return cv2.add(img1, img2)


def resta(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    return cv2.subtract(img1, img2)


def multiplicacion(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    resultado = cv2.multiply(img1, img2)

    return np.clip(resultado, 0, 255).astype(np.uint8)


def division(img1, img2):

    img1, img2 = preparar_imagenes(img1, img2)

    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    img2[img2 == 0] = 1

    resultado = cv2.divide(img1, img2)

    return np.clip(resultado, 0, 255).astype(np.uint8)
import cv2
import numpy as np

def cargar_imagen(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if img is None:
        return None

    # =========================
    # CASO 1: Imagen en color
    # =========================
    if len(img.shape) == 3:
        return img  # BGR 그대로

    # =========================
    # CASO 2: Imagen en escala de grises
    # =========================
    if len(img.shape) == 2:
        # Detectar si es binaria
        unique_vals = np.unique(img)

        if len(unique_vals) <= 2:
            # Es binaria → devolver como está (0 y 255)
            return img

        # Es gris normal
        return img

    return img
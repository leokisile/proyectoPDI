import numpy as np


# =========================
# NORMALIZACIÓN
# =========================
def normalizar(img):
    img = img.astype(np.float32)
    min_val = np.min(img)
    max_val = np.max(img)

    if max_val - min_val == 0:
        return np.zeros_like(img, dtype=np.uint8)

    return ((img - min_val) / (max_val - min_val) * 255).astype(np.uint8)


# =========================
# ESCALA DE GRISES
# =========================
def rgb_a_grises(img):
    """
    Convierte imagen RGB a escala de grises.
    """
    if len(img.shape) == 2:
        return img

    return np.dot(img[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)


# =========================
# EXPANSIÓN DE HISTOGRAMA
# =========================
def expansion_histograma(img, r_min, r_max, new_min=0, new_max=255):
    """
    Expande el rango [r_min, r_max] a [new_min, new_max]
    """
    img = img.astype(np.float32)

    new_min, new_max = min(new_min, new_max), max(new_max, new_min)

    if r_max - r_min == 0:
        return np.zeros_like(img, dtype=np.uint8)

    img_exp = (img - r_min) / (r_max - r_min)
    img_exp = img_exp * (new_max - new_min) + new_min

    return np.clip(img_exp, 0, 255).astype(np.uint8)


# =========================
# CONTRACCIÓN DE HISTOGRAMA
# =========================
def contraccion_histograma(img, r_min, r_max, new_min, new_max):
    """
    Comprime el rango [r_min, r_max] a un rango más pequeño [new_min, new_max]
    """
    img = img.astype(np.float32)

    new_min, new_max = min(new_min, new_max), max(new_max, new_min)

    if r_max - r_min == 0:
        return np.zeros_like(img, dtype=np.uint8)

    img_comp = (img - r_min) / (r_max - r_min)
    img_comp = img_comp * (new_max - new_min) + new_min

    return np.clip(img_comp, 0, 255).astype(np.uint8)


# =========================
# NEGATIVO DE IMAGEN
# =========================
def negativo(img):
    return (255 - img).astype(np.uint8)


# =========================
# BINARIZACIÓN SIMPLE
# =========================
def umbral(img, t=128):
    img_gray = rgb_a_grises(img) if len(img.shape) == 3 else img
    return ((img_gray > t) * 255).astype(np.uint8)
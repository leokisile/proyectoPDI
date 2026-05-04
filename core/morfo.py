import cv2
import numpy as np

# =======================
# Operaciones báscias
# =======================

def erosion(image, kernel, iterations=1):
    return cv2.erode(image, kernel, iterations=iterations)


def dilatacion(image, kernel, iterations=1):
    return cv2.dilate(image, kernel, iterations=iterations)


def apertura(image, kernel):
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def cierre(image, kernel):
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# =========================
# Morfologia Binaria
# =========================
def frontera(binaria, kernel):
    erosion = cv2.erode(binaria, kernel)
    borde = cv2.subtract(binaria, erosion)
    return borde

def adelgazamiento(binaria):
    thinning = cv2.ximgproc.thinning(binaria)
    return thinning

def hit_or_miss(binaria, kernel):
    result = cv2.morphologyEx(binaria, cv2.MORPH_HITMISS, kernel)
    return result

def esqueleto_eje_medio(img_binaria, umbral_poda=1):

    # Asegurar copia
    img = img_binaria.copy()

    # 1. Transformada de distancia
    dist = cv2.distanceTransform(img, cv2.DIST_L2, 5)

    # 2. Eje medio (aproximacion por maximos locales)
    kernel = np.ones((3,3), np.uint8)
    dilatada = cv2.dilate(dist, kernel)

    eje_medio = (dist == dilatada) & (dist > 0)

    skel = (eje_medio.astype(np.uint8)) * 255

    # 3. Poda de ramas pequeñas
    skel_podado = np.zeros_like(skel)

    for y in range(dist.shape[0]):
        for x in range(dist.shape[1]):
            if skel[y, x] == 255 and dist[y, x] >= umbral_poda:
                skel_podado[y, x] = 255

    return skel_podado

# ================================
# Morfologia en Laticces
# ===============================
def gradiente_morfologico(img, kernel):
    return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

def gradiente_dilatacion(img, kernel):
    dil = cv2.dilate(img, kernel)
    return cv2.subtract(dil, img)

def gradiente_erosion(img, kernel):
    ero = cv2.erode(img, kernel)
    return cv2.subtract(img, ero)

def top_hat(img, kernel):
    return cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

def black_hat(img, kernel):
    return cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)


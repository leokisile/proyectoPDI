import cv2


def cargar_imagen(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)
import cv2


def filtro_gaussiano(image, ksize=5):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def filtro_promedio(image, ksize=5):
    return cv2.blur(image, (ksize, ksize))
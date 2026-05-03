import cv2


def filtro_gaussiano(image, ksize=5, sigma=0):
    return cv2.GaussianBlur(image, (ksize, ksize), sigma)


def filtro_promedio(image, ksize=5):
    return cv2.blur(image, (ksize, ksize))


def erosion(image, kernel):
    return cv2.erode(image, kernel, iterations=1)


def dilatacion(image, kernel):
    return cv2.dilate(image, kernel, iterations=1)
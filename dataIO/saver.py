import cv2


def guardar_imagen(path, image):
    cv2.imwrite(path, image)
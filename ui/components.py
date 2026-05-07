import cv2
import numpy as np
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(self, title):
        super().__init__(title)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        self.setMinimumSize(250, 250)

    def set_image(self, img_array):

        if img_array is None:
            return

        # =========================
        # CASO 1: ESCALA DE GRISES
        # =========================
        if len(img_array.shape) == 2:
            h, w = img_array.shape
            bytes_per_line = w

            qimg = QImage(
                img_array.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_Grayscale8
            )

        # =========================
        # CASO 2: COLOR (BGR -> RGB)
        # =========================
        elif len(img_array.shape) == 3:

            # OpenCV usa BGR → Qt usa RGB
            rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

            h, w, ch = rgb.shape
            bytes_per_line = ch * w

            qimg = QImage(
                rgb.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_RGB888
            )

        else:
            return

        pix = QPixmap.fromImage(qimg)
        self.setPixmap(pix.scaled(self.size(), Qt.KeepAspectRatio))
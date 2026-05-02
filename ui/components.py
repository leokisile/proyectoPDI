from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np


class ImageLabel(QLabel):
    def __init__(self, title):
        super().__init__(title)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        self.setMinimumSize(250, 250)

    def set_image(self, img_array):
        if img_array is None:
            return

        height, width = img_array.shape
        bytes_per_line = width
        q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio))

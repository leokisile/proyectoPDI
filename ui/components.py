from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
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
        h, w = img_array.shape
        qimg = QImage(img_array.data, w, h, w, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(qimg)
        self.setPixmap(pix.scaled(self.size(), Qt.KeepAspectRatio))
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
)

from ui.components import ImageLabel
from ui import events


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Procesamiento de Imágenes")
        self.resize(800, 500)

        self.original_img = None
        self.result_img = None

        layout = QVBoxLayout()

        # Botones
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Cargar Imagen")
        self.gauss_btn = QPushButton("Filtro Gaussiano")
        self.mean_btn = QPushButton("Filtro Promedio")

        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.gauss_btn)
        btn_layout.addWidget(self.mean_btn)

        # Imágenes
        img_layout = QHBoxLayout()
        self.original_label = ImageLabel("Original")
        self.result_label = ImageLabel("Resultado")

        img_layout.addWidget(self.original_label)
        img_layout.addWidget(self.result_label)

        layout.addLayout(btn_layout)
        layout.addLayout(img_layout)
        self.setLayout(layout)

        # Conexión de eventos
        self.load_btn.clicked.connect(lambda: events.cargar_imagen_event(self))
        self.gauss_btn.clicked.connect(lambda: events.aplicar_gaussiano_event(self))
        self.mean_btn.clicked.connect(lambda: events.aplicar_promedio_event(self))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
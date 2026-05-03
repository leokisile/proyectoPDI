import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QLabel, QSlider, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

from ui.components import ImageLabel
from ui import events
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Procesamiento de Imágenes")
        self.resize(1100, 600)

        self.original_img = None
        self.result_img = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # =====================
        # MENU
        # =====================
        top = QHBoxLayout()
        self.combo_operaciones = QComboBox()
        self.combo_operaciones.addItems([
            "Seleccionar operación",
            "Filtro Gaussiano",
            "Filtro Promedio",
            "Erosión",
            "Dilatación"
        ])
        self.apply_btn = QPushButton("Aplicar")
        self.load_btn = QPushButton("Cargar")
        self.save_btn = QPushButton("Guardar")

        top.addWidget(self.combo_operaciones)
        top.addWidget(self.apply_btn)
        top.addWidget(self.load_btn)
        top.addWidget(self.save_btn)

        # =====================
        # CONTENIDO
        # =====================
        main = QHBoxLayout()

        # Panel lateral dinámico
        self.panel = QVBoxLayout()

        self.slider_kernel = QSlider(Qt.Horizontal)
        self.slider_kernel.setMinimum(1)
        self.slider_kernel.setMaximum(15)
        self.slider_kernel.setValue(5)

        self.slider_sigma = QSlider(Qt.Horizontal)
        self.slider_sigma.setMinimum(0)
        self.slider_sigma.setMaximum(10)

        self.panel.addWidget(QLabel("Kernel"))
        self.panel.addWidget(self.slider_kernel)
        self.panel.addWidget(QLabel("Sigma"))
        self.panel.addWidget(self.slider_sigma)

        # Matriz morfológica
        self.kernel_table = QTableWidget(5, 5)
        for i in range(5):
            for j in range(5):
                self.kernel_table.setItem(i, j, QTableWidgetItem("1"))

        self.panel.addWidget(QLabel("Elemento estructurante"))
        self.panel.addWidget(self.kernel_table)

        # Imágenes
        imgs = QHBoxLayout()
        self.original_label = ImageLabel("Original")
        self.result_label = ImageLabel("Resultado")
        imgs.addWidget(self.original_label)
        imgs.addWidget(self.result_label)

        main.addLayout(self.panel)
        main.addLayout(imgs)

        layout.addLayout(top)
        layout.addLayout(main)
        central.setLayout(layout)

        # =====================
        # EVENTOS
        # =====================
        self.load_btn.clicked.connect(lambda: events.cargar_imagen_event(self))
        self.save_btn.clicked.connect(lambda: events.guardar_imagen_event(self))
        self.apply_btn.clicked.connect(lambda: events.aplicar_segun_opcion(self))
        self.combo_operaciones.currentTextChanged.connect(self.update_panel)

        self.update_panel()

    def update_panel(self):
        op = self.combo_operaciones.currentText()

        # sliders visibles solo para filtros
        sliders_visible = op in ["Filtro Gaussiano", "Filtro Promedio"]
        self.slider_kernel.setVisible(sliders_visible)
        self.slider_sigma.setVisible(op == "Filtro Gaussiano")

        # kernel visible solo en morfología
        kernel_visible = op in ["Erosión", "Dilatación"]
        self.kernel_table.setVisible(kernel_visible)

    def get_kernel(self):
        rows = self.kernel_table.rowCount()
        cols = self.kernel_table.columnCount()
        mat = []
        for i in range(rows):
            row = []
            for j in range(cols):
                val = int(self.kernel_table.item(i, j).text())
                row.append(val)
            mat.append(row)
        return np.array(mat, dtype='uint8')

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
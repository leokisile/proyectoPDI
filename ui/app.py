# =========================
# ui/app.py (FIX CRASH + MENU UNIFICADO)
# =========================
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import Qt

from ui.components import ImageLabel
from ui import events
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDI Plataforma")
        self.resize(1200, 600)

        self.original_img = None
        self.result_img = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # =====================
        # ÁRBOL UNIFICADO
        # =====================
        top = QHBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Operaciones")

        # ===== FILTROS =====
        filtros = QTreeWidgetItem(["Filtros"])

        paso_altas = QTreeWidgetItem(["Paso Altas"])
        paso_altas.addChildren([
            QTreeWidgetItem(["Sobel"]),
            QTreeWidgetItem(["Prewitt"]),
            QTreeWidgetItem(["Roberts"]),
            QTreeWidgetItem(["Canny"]),
            QTreeWidgetItem(["Kirsch"]),
            QTreeWidgetItem(["Laplaciano"])
        ])

        paso_bajas = QTreeWidgetItem(["Paso Bajas"])
        paso_bajas.addChildren([
            QTreeWidgetItem(["Gaussiano"]),
            QTreeWidgetItem(["Promedio"]),
            QTreeWidgetItem(["Promedio Pesado"])
        ])

        no_lineales = QTreeWidgetItem(["No Lineales"])
        no_lineales.addChildren([
            QTreeWidgetItem(["Mediano"]),
            QTreeWidgetItem(["Moda"]),
            QTreeWidgetItem(["Minimo"]),
            QTreeWidgetItem(["Maximo"]),
            QTreeWidgetItem(["Bilateral"])
        ])

        filtros.addChildren([paso_altas, paso_bajas, no_lineales])

        # ===== MORFOLOGÍA =====
        morfo = QTreeWidgetItem(["Morfología"])
        morfo.addChildren([
            QTreeWidgetItem(["Erosión"]),
            QTreeWidgetItem(["Dilatación"]),
            QTreeWidgetItem(["Apertura"]),
            QTreeWidgetItem(["Cierre"]),
            QTreeWidgetItem(["Gradiente"])
        ])

        self.tree.addTopLevelItems([filtros, morfo])

        self.label_operacion = QLabel("Operación: Ninguna")

        self.apply_btn = QPushButton("Aplicar")
        self.load_btn = QPushButton("Cargar")
        self.save_btn = QPushButton("Guardar")

        top.addWidget(self.tree)
        top.addWidget(self.label_operacion)
        top.addWidget(self.apply_btn)
        top.addWidget(self.load_btn)
        top.addWidget(self.save_btn)

        # =====================
        # LAYOUT 1/3
        # =====================
        main = QHBoxLayout()

        # Panel
        self.panel = QVBoxLayout()

        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setRange(1, 15)

        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(0, 255)

        self.slider3 = QSlider(Qt.Horizontal)
        self.slider3.setRange(0, 255)

        self.panel.addWidget(QLabel("Parámetro 1 (1-15)"))
        self.panel.addWidget(self.slider1)
        self.panel.addWidget(QLabel("Parámetro 2 (0-255)"))
        self.panel.addWidget(self.slider2)
        self.panel.addWidget(QLabel("Parámetro 3 (0-255)"))
        self.panel.addWidget(self.slider3)

        self.kernel_table = QTableWidget(5, 5)
        for i in range(5):
            for j in range(5):
                self.kernel_table.setItem(i, j, QTableWidgetItem("1"))

        self.panel.addWidget(QLabel("Kernel"))
        self.panel.addWidget(self.kernel_table)

        panel_widget = QWidget()
        panel_widget.setLayout(self.panel)

        # Imágenes
        self.original_label = ImageLabel("Original")
        self.result_label = ImageLabel("Resultado")

        main.addWidget(panel_widget, 1)
        main.addWidget(self.original_label, 1)
        main.addWidget(self.result_label, 1)

        layout.addLayout(top)
        layout.addLayout(main)
        central.setLayout(layout)

        # =====================
        # EVENTOS
        # =====================
        self.load_btn.clicked.connect(lambda: events.cargar_imagen_event(self))
        self.save_btn.clicked.connect(lambda: events.guardar_imagen_event(self))
        self.apply_btn.clicked.connect(lambda: events.dispatch(self))

        self.tree.itemClicked.connect(self.update_ui)

    def get_selected_operation(self):
        item = self.tree.currentItem()
        if item and item.childCount() == 0:
            return item.text(0)
        return None

    def update_ui(self):
        op = self.get_selected_operation()

        if not op:
            return

        self.label_operacion.setText(f"Operación: {op}")

        # Mostrar sliders o kernel
        # Slider del ksize
        if op in ["Sobel", "Gaussiano", "Mediano", "Moda", "Maximo", "Minimo"]:
            self.slider1.setVisible(True)
        else:
            self.slider1.setVisible(False)

        # Sliders con valores 0 - 255
        if op in ["Gaussiano", "Canny"]:
            self.slider2.setVisible(True)
        else:
            self.slider2.setVisible(False)

        if op in ["Canny"]:
            self.slider3.setVisible(True)
        else:
            self.slider3.setVisible(False)

        self.kernel_table.setVisible(op in [
            "Erosión", "Dilatación", "Apertura", "Cierre", "Gradiente"
        ])

    def get_kernel(self):
        rows = self.kernel_table.rowCount()
        cols = self.kernel_table.columnCount()
        mat = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(int(self.kernel_table.item(i, j).text()))
            mat.append(row)
        return np.array(mat, dtype='uint8')


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

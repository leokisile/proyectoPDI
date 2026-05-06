# =========================
# ui/app.py (FIX CRASH + MENU UNIFICADO)
# =========================
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QSlider, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt

from ui.components import ImageLabel
from ui import events
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDI Plataforma")
        self.resize(1400, 800)

        #Inicializar imagenes
        self.original_img = None
        self.img2 = None
        self.result_img = None

        # Inicializar historial
        self.history = []
        self.history_index = -1

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()

        # =====================
        # ÁRBOL UNIFICADO
        # =====================
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Operaciones")
        self.tree.setMaximumWidth(250)

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

        ope_basicas = QTreeWidgetItem(["Operaciones basicas"])
        ope_basicas.addChildren([
            QTreeWidgetItem(["Erosion"]),
            QTreeWidgetItem(["Dilatacion"]),
            QTreeWidgetItem(["Apertura"]),
            QTreeWidgetItem(["Cierre"])
        ])

        binarias = QTreeWidgetItem(["Morfologia Binaria"])
        binarias.addChildren([
            QTreeWidgetItem(["Frontera"]),
            QTreeWidgetItem(["Adelgazamiento"]),
            QTreeWidgetItem(["Hit-or-Miss"]),
            QTreeWidgetItem(["Esqueleto"])
        ])

        laticces = QTreeWidgetItem(["Morfologia en Laticces"])
        laticces.addChildren([
            QTreeWidgetItem(["Gradiente simetrico"]),
            QTreeWidgetItem(["Gradiente por erosion"]),
            QTreeWidgetItem(["Gradiente por dilatacion"]),
            QTreeWidgetItem(["Top Hat"]),
            QTreeWidgetItem(["Black Hat"])
        ])

        morfo.addChildren([ope_basicas, binarias, laticces])

        logicas = QTreeWidgetItem(["Operaciones Lógicas"])
        logicas.addChildren([
            QTreeWidgetItem(["AND"]),
            QTreeWidgetItem(["OR"]),
            QTreeWidgetItem(["XOR"]),
            QTreeWidgetItem(["NOT"]),
            QTreeWidgetItem(["Suma"]),
            QTreeWidgetItem(["Resta"]),
            QTreeWidgetItem(["Multiplicacion"]),
            QTreeWidgetItem(["Division"])
        ])

        self.tree.addTopLevelItems([filtros, morfo, logicas])

        # =====================
        # PANEL IZQUIERDO
        # =====================
        left_layout = QVBoxLayout()

        #Elegir imagen
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Imagen original", "Resultado"])

        # Sliders
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setRange(1, 15)

        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(0, 255)

        self.slider3 = QSlider(Qt.Horizontal)
        self.slider3.setRange(0, 255)

        self.slider1.valueChanged.connect(self.update_label_params)
        self.slider2.valueChanged.connect(self.update_label_params)
        self.slider3.valueChanged.connect(self.update_label_params)

        # Kernel
        self.kernel_table = QTableWidget(5, 5)
        for i in range(5):
            for j in range(5):
                self.kernel_table.setItem(i, j, QTableWidgetItem("1"))

        left_layout.addWidget(self.tree)

        left_layout.addWidget(QLabel("Aplicar sobre:"))
        left_layout.addWidget(self.source_combo)

        left_layout.addWidget(QLabel("Parámetro 1"))
        left_layout.addWidget(self.slider1)
        left_layout.addWidget(QLabel("Parámetro 2"))
        left_layout.addWidget(self.slider2)
        left_layout.addWidget(QLabel("Parámetro 3"))
        left_layout.addWidget(self.slider3)

        left_layout.addWidget(QLabel("Kernel"))
        left_layout.addWidget(self.kernel_table)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # =====================
        # CENTRO
        # =====================
        center_layout = QVBoxLayout()

        self.load_btn_1 = QPushButton("Cargar Imagen 1")
        self.img1_label = ImageLabel("Imagen 1")

        self.load_btn_2 = QPushButton("Cargar Imagen 2")
        self.img2_label = ImageLabel("Imagen 2")

        self.load_btn_2.setVisible(False)
        self.img2_label.setVisible(False)

        self.label_operacion = QLabel("Operación: Ninguna")

        self.apply_btn = QPushButton("Aplicar")
        self.save_btn = QPushButton("Guardar")

        center_layout.addWidget(self.load_btn_1)
        center_layout.addWidget(self.img1_label)
        center_layout.addWidget(self.load_btn_2)
        center_layout.addWidget(self.img2_label)
        center_layout.addWidget(self.label_operacion)
        center_layout.addWidget(self.apply_btn)
        center_layout.addWidget(self.save_btn)

        center_widget = QWidget()
        center_widget.setLayout(center_layout)

        # =====================
        # DERECHA
        # =====================
        right_layout = QVBoxLayout()

        self.original_label = ImageLabel("Original")
        self.result_label = ImageLabel("Resultado")

        self.undo_btn = QPushButton("← Undo")
        self.redo_btn = QPushButton("Redo →")

        right_layout.addWidget(self.original_label)
        right_layout.addWidget(self.result_label)

        right_layout.addWidget(self.undo_btn)
        right_layout.addWidget(self.redo_btn)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # =====================
        # GRID
        # =====================
        grid = QGridLayout()
        grid.addWidget(left_widget, 0, 0)
        grid.addWidget(center_widget, 0, 1)
        grid.addWidget(right_widget, 0, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        main_layout.addLayout(grid)
        central.setLayout(main_layout)

        # =====================
        # EVENTOS
        # =====================
        self.load_btn_1.clicked.connect(lambda: events.cargar_imagen_event(self))
        self.load_btn_2.clicked.connect(lambda: events.cargar_imagen2_event(self))
        self.apply_btn.clicked.connect(lambda: events.dispatch(self))
        self.save_btn.clicked.connect(lambda: events.guardar_imagen_event(self))
        self.undo_btn.clicked.connect(lambda: events.undo(self))
        self.redo_btn.clicked.connect(lambda: events.redo(self))

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

        # Imagen 2 solo para operaciones lógicas
        ops_2_imgs = [
            "AND", "OR", "XOR",
            "Suma", "Resta",
            "Multiplicacion", "Division"
        ]
        if op in ops_2_imgs:
            self.load_btn_2.setVisible(True)
            self.img2_label.setVisible(True)
        else:
            self.load_btn_2.setVisible(False)
            self.img2_label.setVisible(False)

        # Mostrar sliders o kernel
        # Slider del ksize, iteraciones, umbral de poda
        if op in ["Sobel", "Gaussiano", "Mediano", "Moda", "Maximo", "Minimo", "Erosion", "Dilatacion", "Esqueleto"]:
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
            "Erosion", "Dilatacion", "Apertura", "Cierre", "Gradiente", "Frontera", "Hit-or-Miss", "Top Hat", "Black Hat", "Gradiente simetrico", "Gradiente por erosion", "Gradiente por dilatacion"
        ])

        self.update_label_params()

    def get_kernel(self):
        rows = self.kernel_table.rowCount()
        cols = self.kernel_table.columnCount()
        mat = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(int(self.kernel_table.item(i, j).text()))
            mat.append(row)
        return np.array(mat, dtype='int8')

    def update_label_params(self):
        op = self.get_selected_operation()

        if not op:
            self.label_operacion.setText("Operación: Ninguna")
            return

        texto = f"Operación: {op}"

        # Mostrar valores según visibilidad
        if self.slider1.isVisible():
            texto += f" | Ksize: {self.slider1.value()}"

        if self.slider2.isVisible():
            texto += f" | P1: {self.slider2.value()}"

        if self.slider3.isVisible():
            texto += f" | P2: {self.slider3.value()}"

        self.label_operacion.setText(texto)



def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QFileDialog
from dataIO.loader import cargar_imagen
from dataIO.saver import guardar_imagen
from core.filtros import filtro_gaussiano, filtro_promedio, erosion, dilatacion
import numpy as np


def cargar_imagen_event(ui):
    path, _ = QFileDialog.getOpenFileName(None, "Seleccionar imagen")
    if path:
        img = cargar_imagen(path)
        ui.original_img = img
        ui.original_label.set_image(img)


def guardar_imagen_event(ui):
    if ui.result_img is None:
        return
    path, _ = QFileDialog.getSaveFileName(None, "Guardar imagen", filter="PNG (*.png);;JPG (*.jpg)")
    if path:
        guardar_imagen(path, ui.result_img)


def aplicar_segun_opcion(ui):
    if ui.original_img is None:
        return

    op = ui.combo_operaciones.currentText()

    if op == "Filtro Gaussiano":
        k = ui.slider_kernel.value() | 1  # asegurar impar
        s = ui.slider_sigma.value()
        res = filtro_gaussiano(ui.original_img, k, s)

    elif op == "Filtro Promedio":
        k = ui.slider_kernel.value() | 1
        res = filtro_promedio(ui.original_img, k)

    elif op == "Erosión":
        kernel = ui.get_kernel()
        res = erosion(ui.original_img, kernel)

    elif op == "Dilatación":
        kernel = ui.get_kernel()
        res = dilatacion(ui.original_img, kernel)

    else:
        return

    ui.result_img = res
    ui.result_label.set_image(res)
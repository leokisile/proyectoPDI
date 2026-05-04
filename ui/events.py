from PyQt5.QtWidgets import QFileDialog
from dataIO.loader import cargar_imagen
from dataIO.saver import guardar_imagen
from core import filtros, morfo
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


# =========================
# ui/events.py (FIX CRASH)
# =========================
from core import filtros, morfo


def dispatch(ui):
    if ui.original_img is None:
        return

    op = ui.get_selected_operation()
    if not op:
        return

    img = ui.original_img

    try:
        if op == "Sobel":
            res = filtros.filtro_sobel(img, ui.slider1.value())

        elif op == "Gaussiano":
            res = filtros.filtro_gaussian(img, ui.slider1.value(), 1)

        elif op == "Mediano":
            res = filtros.filtro_mediano(img, ui.slider1.value())

        elif op == "Erosión":
            res = morfo.erosion(img, ui.get_kernel())

        elif op == "Dilatación":
            res = morfo.dilatacion(img, ui.get_kernel())

        elif op == "Apertura":
            res = morfo.apertura(img, ui.get_kernel())

        elif op == "Cierre":
            res = morfo.cierre(img, ui.get_kernel())

        elif op == "Gradiente":
            res = morfo.gradiente_morfologico(img, ui.get_kernel())

        else:
            return

        ui.result_img = res
        ui.result_label.set_image(res)

    except Exception as e:
        print("Error en operación:", e)
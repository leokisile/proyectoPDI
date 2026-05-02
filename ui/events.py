from PyQt5.QtWidgets import QFileDialog
from dataIO.loader import cargar_imagen
from core.filtros import filtro_gaussiano, filtro_promedio


def cargar_imagen_event(ui):
    path, _ = QFileDialog.getOpenFileName(None, "Seleccionar imagen")
    if path:
        img = cargar_imagen(path)
        ui.original_img = img
        ui.original_label.set_image(img)


def aplicar_gaussiano_event(ui):
    if ui.original_img is None:
        return
    result = filtro_gaussiano(ui.original_img)
    ui.result_img = result
    ui.result_label.set_image(result)


def aplicar_promedio_event(ui):
    if ui.original_img is None:
        return
    result = filtro_promedio(ui.original_img)
    ui.result_img = result
    ui.result_label.set_image(result)
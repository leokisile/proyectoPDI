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

        elif op == "Prewitt":
            res = filtros.filtro_prewitt(img)

        elif op == "Roberts":
            res = filtros.filtro_roberts(img)

        elif op == "Canny":
            res = filtros.filtro_canny(img, ui.slider2.value(), ui.slider3.value())

        elif op == "Kirsch":
            res = filtros.filtro_kirsch(img)

        elif op == "Laplaciano":
            res = filtros.filtro_laplaciano(img)

        elif op == "Promedio":
            res = filtros.filtro_promedio(img)

        elif op == "Promedio Pesado":
            res = filtros.filtro_promediador_pesado(img)

        elif op == "Gaussiano":
            res = filtros.filtro_gaussian(img, ui.slider1.value(), ui.slider2.value())

        elif op == "Mediano":
            res = filtros.filtro_mediano(img, ui.slider1.value())

        elif op == "Moda":
            res = filtros.filtro_moda(img, ui.slider1.value())

        elif op == "Minimo":
            res = filtros.filtro_minimo(img, ui.slider1.value())

        elif op == "Maximo":
            res = filtros.filtro_maximo(img, ui.slider1.value())

        elif op == "Bilateral":
            res = filtros.filtro_bilateral(img)

        elif op == "Erosion":
            res = morfo.erosion(img, ui.get_kernel(), ui.slider1.value())

        elif op == "Dilatacion":
            res = morfo.dilatacion(img, ui.get_kernel(), ui.slider1.value())

        elif op == "Apertura":
            res = morfo.apertura(img, ui.get_kernel())

        elif op == "Cierre":
            res = morfo.cierre(img, ui.get_kernel())

        elif op == "Frontera":
            res = morfo.frontera(img, ui.get_kernel())

        elif op == "Adelgazamiento":
            res = morfo.adelgazamiento(img)

        elif op == "Hit-or-Miss":
            res = morfo.hit_or_miss(img, ui.get_kernel())

        elif op == "Esqueleto":
            res = morfo.esqueleto_eje_medio(img, ui.slider1.value())

        elif op == "Gradiente simetrico":
            res = morfo.gradiente_morfologico(img, ui.get_kernel())

        elif op == "Gradiente por erosion":
            res = morfo.gradiente_erosion(img, ui.get_kernel())

        elif op == "Gradiente por dilatacion":
            res = morfo.gradiente_dilatacion(img, ui.get_kernel())

        elif op == "Top Hat":
            res = morfo.top_hat(img, ui.get_kernel())

        elif op == "Black Hat":
            res = morfo.black_hat(img, ui.get_kernel())

        else:
            return

        ui.result_img = res
        ui.result_label.set_image(res)

    except Exception as e:
        print("Error en operación:", e)
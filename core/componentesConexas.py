# componentes_conexas.py

import cv2
import numpy as np


def _to_binary(img):
    """
    Convierte a binaria si es necesario.
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_bin = cv2.threshold(
        img,
        127,
        255,
        cv2.THRESH_BINARY
    )

    return img_bin


def vecindad_4(img):
    """
    Etiquetado usando conectividad 4.
    """
    img_bin = _to_binary(img)

    num_labels, labels = cv2.connectedComponents(
        img_bin,
        connectivity=4
    )

    return labels.astype(np.uint8)


def vecindad_8(img):
    """
    Etiquetado usando conectividad 8.
    """
    img_bin = _to_binary(img)

    num_labels, labels = cv2.connectedComponents(
        img_bin,
        connectivity=8
    )

    return labels.astype(np.uint8)

def conteo_objetos(img):
    """
    Cuenta objetos, etiqueta cada componente conexa,
    muestra el número del objeto y su área en píxeles.
    """

    img_bin = _to_binary(img)

    num_labels, labels, stats, centroids = \
        cv2.connectedComponentsWithStats(
            img_bin,
            connectivity=8
        )

    # Imagen RGB donde se dibujarán los componentes
    salida = np.zeros(
        (labels.shape[0], labels.shape[1], 3),
        dtype=np.uint8
    )

    # Colores aleatorios para los objetos
    colores = np.random.randint(
        0,
        255,
        size=(num_labels, 3),
        dtype=np.uint8
    )

    contador = 0

    for i in range(1, num_labels):

        contador += 1

        # Área del componente
        area = stats[i, cv2.CC_STAT_AREA]

        # Pintar componente
        salida[labels == i] = colores[i]

        # Coordenadas del centroide
        x, y = centroids[i]

        x = int(x)
        y = int(y)

        # Texto a mostrar
        texto = f"{contador}: {area}px"

        # Dibujar etiqueta
        cv2.putText(
            salida,
            texto,
            (x - 20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    print(f"Objetos encontrados: {contador}")

    return salida
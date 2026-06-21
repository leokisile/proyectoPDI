# araña_roja/preprocesamiento.py

import cv2
import numpy as np


def redimensionar_estandar(img, base=500):

    h, w = img.shape[:2]

    escala = base / max(h, w)

    nueva_dim = (
        int(w * escala),
        int(h * escala)
    )

    return cv2.resize(
        img,
        nueva_dim,
        interpolation=cv2.INTER_AREA
    )


def extraer_rojo_verde(img):
    """
    Extrae diferencia entre canal rojo y verde.
    Arañas rojas resaltan por mayor componente R.
    """

    b, g, r = cv2.split(img)

    return np.maximum(
        0,
        r.astype(np.int16) -
        g.astype(np.int16)
    ).astype(np.uint8)



def expandir_contraste(img):

    minimo = np.min(img)
    maximo = np.max(img)

    return np.uint8(
        ((img-minimo) /
        (maximo-minimo+1e-10))*255
    )



def suavizar_mediana(img, kernel=3):

    return cv2.medianBlur(
        img,
        kernel
    )

# araña_roja/segmentacion.py

import cv2
import numpy as np



def umbral_araña_roja(
        img,
        umbral=20):

    _, binaria = cv2.threshold(
        img,
        umbral,
        255,
        cv2.THRESH_BINARY
    )

    return binaria



def filtrar_componentes(
        binaria,
        intensidad_ref,
        area_min=300,
        intensidad_min=80):


    n, labels, stats, _ = \
        cv2.connectedComponentsWithStats(
            binaria,
            connectivity=8
        )


    resultado = np.zeros_like(binaria)


    for i in range(1,n):

        mascara = labels == i

        area = stats[
            i,
            cv2.CC_STAT_AREA
        ]

        pico = np.max(
            intensidad_ref[mascara]
        )


        if (
            area > area_min and
            pico > intensidad_min
        ):

            resultado[mascara]=255


    return resultado

# araña_roja/componentes.py

import cv2
import numpy as np


def analizar_componentes(img):

    n, labels, stats, centroides = \
        cv2.connectedComponentsWithStats(
            img,
            connectivity=8
        )


    datos=[]


    for i in range(1,n):

        area = stats[
            i,
            cv2.CC_STAT_AREA
        ]

        x,y,w,h = stats[
            i,
            cv2.CC_STAT_LEFT:
            cv2.CC_STAT_HEIGHT+1
        ]


        datos.append({
            "objeto":i,
            "area":area,
            "bbox":(x,y,w,h)
        })


    print(
        f"Objetos detectados: {n-1}"
    )


    return datos

# araña_roja/visualizacion.py

import cv2
import numpy as np



def resaltar_segmentacion(
    img,
    mascara,
    alpha=0.5
):

    resultado = img.copy()


    overlay = np.zeros_like(img)

    overlay[:]=(0,255,255)


    resultado[mascara>0]=cv2.addWeighted(
        img[mascara>0],
        1-alpha,
        overlay[mascara>0],
        alpha,
        0
    )


    n,labels,stats,centroides = \
        cv2.connectedComponentsWithStats(
            mascara,
            8
        )


    for i in range(1,n):

        x = stats[i,cv2.CC_STAT_LEFT]
        y = stats[i,cv2.CC_STAT_TOP]

        w = stats[i,cv2.CC_STAT_WIDTH]
        h = stats[i,cv2.CC_STAT_HEIGHT]


        area = stats[
            i,
            cv2.CC_STAT_AREA
        ]


        cv2.rectangle(
            resultado,
            (x,y),
            (x+w,y+h),
            (255,0,0),
            2
        )


        cv2.putText(
            resultado,
            f"{i}: {area}px",
            (x,y-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,0,255),
            2
        )


    return resultado

def procesar_arana_roja(
        img,
        area_min=300,
        intensidad_min=80,
        umbral=20
):
    """
    Pipeline automático completo
    de segmentación de araña roja.

    Entrada:
        img -> imagen BGR original

    Retorna:
        resultado final resaltado
        y todas las etapas intermedias
    """


    # 1. Normalizar tamaño
    original = redimensionar_estandar(img)


    # 2. Extraer diferencia rojo-verde
    rg = extraer_rojo_verde(original)


    # 3. Expandir contraste
    expansion = expandir_contraste(rg)


    # 4. Suavizado mediana
    suavizada = suavizar_mediana(
        expansion,
        kernel=3
    )


    # 5. Umbralización
    binaria = umbral_araña_roja(
        suavizada,
        umbral
    )


    # 6. Filtrado por componentes
    mascara_final = filtrar_componentes(
        binaria,
        expansion,
        area_min,
        intensidad_min
    )


    # 7. Visualización sobre imagen original
    resultado = resaltar_segmentacion(
        original,
        mascara_final
    )


    return {
        "original": original,
        "rojo_verde": rg,
        "expansion": expansion,
        "suavizada": suavizada,
        "binaria": binaria,
        "mascara_final": mascara_final,
        "resultado": resultado
    }
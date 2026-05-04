import cv2
import numpy as np

# ============================
# Filtros lineales paso altas
# ============================
def filtro_sobel(imagen, ksize=3):
    sobel_x = cv2.Sobel(imagen, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(imagen, cv2.CV_64F, 0, 1, ksize=ksize)
    return cv2.magnitude(sobel_x, sobel_y)

def filtro_prewitt(imagen):
    kernel_prewitt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
    kernel_prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

    prewitt_x = cv2.filter2D(imagen, -1, kernel_prewitt_x)
    prewitt_y = cv2.filter2D(imagen, -1, kernel_prewitt_y)
    bordes_Prewitt = cv2.addWeighted(prewitt_x, 0.5, prewitt_y, 0.5, 0)
    return bordes_Prewitt

def filtro_roberts(imagen):
    kernel_roberts_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_roberts_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)

    roberts_x = cv2.filter2D(imagen, -1, kernel_roberts_x)
    roberts_y = cv2.filter2D(imagen, -1, kernel_roberts_y)

    bordes_Roberts = cv2.addWeighted(roberts_x, 0.5, roberts_y, 0.5, 0)
    return bordes_Roberts

def filtro_canny(imagen, t1=100, t2=200):
    return cv2.Canny(imagen, t1, t2)

def filtro_kirsch(imagen):
    kernel_kirsch = [
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]),
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]),
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),
        np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),
        np.array([[-3, 5, -3], [-3, 0, -3], [-3, 5, -3]])
  ]

    bordes_kirsch = np.max([cv2.filter2D(imagen, -1, kernel) for kernel in kernel_kirsch], axis=0)
    return bordes_kirsch

def filtro_laplaciano(imagen):
    kernel_laplaciano = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
    laplaciano = cv2.filter2D(imagen, -1, kernel_laplaciano)
    return laplaciano

# ============================
# Filtros lineales paso bajas
# ============================
def filtro_promedio(imagen):
    return cv2.blur(imagen, (5, 5))

def filtro_promediador_pesado(imagen):
    kernel_promediador_pesado = np.array([[1,1,1], [1,5,1], [1,1,1]]) / 13
    promediador_pesado = cv2.filter2D(imagen, -1, kernel_promediador_pesado)
    return promediador_pesado

def filtro_gaussian(imagen, ksize=3, sigma=1):
    ksize = ksize if ksize % 2 == 1 else ksize + 1
    return cv2.GaussianBlur(imagen, (ksize, ksize), sigma)

# =========================
# Filtros no lineales
# =========================
def filtro_mediano(imagen, ksize=5):
    return cv2.medianBlur(imagen, ksize)

def filtro_moda(imagen, kernel_size=3):
    import numpy as np

    salida = np.copy(imagen)
    h, w = imagen.shape
    pad = kernel_size // 2

    imagen_padded = np.pad(imagen, pad, mode='reflect')

    for i in range(h):
        for j in range(w):
            window = imagen_padded[i:i+kernel_size, j:j+kernel_size].ravel()

            vals, counts = np.unique(window, return_counts=True)
            salida[i, j] = vals[np.argmax(counts)]

    return salida

def filtro_maximo(imagen, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    imagen_max = cv2.dilate(imagen, kernel, iterations=1)
    return imagen_max

def filtro_minimo(imagen, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    imagen_min = cv2.erode(imagen, kernel, iterations=1)
    return imagen_min

def filtro_bilateral(imagen):
    return cv2.bilateralFilter(imagen, 9, 75, 75)
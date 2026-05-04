import cv2
import numpy as np

def apply_blur(image : np.ndarray, ksize : int) -> np.ndarray:
    ksize = max(1, ksize)
    if ksize % 2 == 0:
        ksize += 1

    if ksize == 1:
        return image.copy()

    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def apply_sharpness(image : np.ndarray, alpha : float) -> np.ndarray:
    if alpha == 0:
        return image.copy()

    blurred = cv2.GaussianBlur(image, (0,0), sigmaX=3)
    sharpened = cv2.addWeighted(image, 1 + alpha, blurred, -alpha, 0)
    return sharpened

def apply_brightness(image : np.ndarray , beta : int) -> np.ndarray:
    if beta == 0:
        return image.copy()
    return cv2.convertScaleAbs(image, alpha = 1.0, beta = beta)

def apply_contrast(image : np.ndarray, alpha : float) -> np.ndarray:
    if alpha == 1.0:
        return image.copy()

    return cv2.convertScaleAbs(image, alpha = alpha, beta = 0)

def apply_edge_detection(image : np.ndarray, thresh1 : int, thresh2 : int) -> np.ndarray:
    if image.ndim == 2:
        gray = image.copy()
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray, thresh1, thresh2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_grayscale(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
    return image

def apply_all_filters(
        image : np.ndarray,
        blur_ksize : int = 1,
        sharpness_alpha : float = 0,
        brightness_beta : int = 0,
        contrast_alpha : float = 1.0,
        edge_detection : bool = False,
        edge_thresh1 : int = 100,
        edge_thresh2 : int = 200,
        gray_scale : bool = False,
) -> np.ndarray:

    result = image.copy()

    if gray_scale:
        result = apply_grayscale(result)

    result = apply_brightness(result, brightness_beta)
    result = apply_contrast(result, contrast_alpha)
    result = apply_blur(result, blur_ksize)
    result = apply_sharpness(result, sharpness_alpha)
    if edge_detection:
        result = apply_edge_detection(result, edge_thresh1, edge_thresh2)

    if gray_scale:
        result = apply_grayscale(result)    

    return result   
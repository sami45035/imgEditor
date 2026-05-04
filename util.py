import io
import numpy as np 
from PIL import Image


def pil_to_numpy_bgr(pil_image: Image.Image) -> np.ndarray:

    rgb_image = pil_image.convert("RGB")
    rgb_array = np.array(rgb_image, dtype=np.uint8)

    
    bgr_array = rgb_array[:, :, ::-1].copy()
    return bgr_array


def numpy_bgr_to_pil(bgr_array):
    if bgr_array.ndim == 2:
        # Grayscale → PIL directly
        return Image.fromarray(bgr_array.astype(np.uint8), mode='L')
    
    elif bgr_array.ndim == 3:
        if bgr_array.shape[2] == 4:
            # BGRA → RGBA
            rgb_array = bgr_array[:, :, [2, 1, 0, 3]].copy()
            return Image.fromarray(rgb_array.astype(np.uint8), mode='RGBA')
        else:
            # BGR → RGB
            rgb_array = bgr_array[:, :, ::-1].copy()
            return Image.fromarray(rgb_array.astype(np.uint8), mode='RGB')
    else:
        raise ValueError(f"Unexpected array shape: {bgr_array.shape}")

def numpy_bgr_to_rgb(bgr_array):
    # If grayscale (2D), convert to RGB by stacking 3 channels
    if bgr_array.ndim == 2:
        return np.stack([bgr_array] * 3, axis=-1).copy()
    
    # If already 3D (H, W, C), reverse BGR → RGB
    return bgr_array[:, :, ::-1].copy()

def numpy_bgr_to_png_bytes(bgr_array):
    pil_image = numpy_bgr_to_pil(bgr_array)
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()


def uploaded_file_to_pil(uploaded_file) -> Image.Image:
    
    image_bytes = uploaded_file.read()
    pil_image = Image.open(io.BytesIO(image_bytes))
    return pil_image.convert("RGB")
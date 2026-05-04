import streamlit as st

from filters import apply_all_filters
from util import (
    pil_to_numpy_bgr,
    numpy_bgr_to_rgb,
    numpy_bgr_to_png_bytes,
    uploaded_file_to_pil,
)


st.set_page_config(
    page_title="Image Editor",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)


DEFAULTS = {
    "blur_ksize": 1,
    "sharpness_alpha": 0.0,
    "brightness_beta": 0,
    "contrast_alpha": 1.0,
    "edge_detect": False,
    "edge_thresh1": 100,
    "edge_thresh2": 200,
    "grayscale": False,
}


def reset_filters():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value



for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


with st.sidebar:
    st.title("🎛️ Filter Controls")
    st.markdown("---")

    
    st.subheader("🌫️ Blur")
    blur_ksize = st.slider(
        "Kernel size (1 = off)",
        min_value=1,
        max_value=51,
        step=2,           # keep odd values only
        key="blur_ksize",
        help="Gaussian blur kernel size. Must be an odd number; 1 means no blur.",
    )

    st.markdown("---")

   
    st.subheader("✨ Sharpness")
    sharpness_alpha = st.slider(
        "Strength (0 = off)",
        min_value=0.0,
        max_value=3.0,
        step=0.1,
        key="sharpness_alpha",
        help="Unsharp-mask alpha. 0 = no sharpening; 3 = maximum sharpening.",
    )

    st.markdown("---")

    
    st.subheader("☀️ Brightness")
    brightness_beta = st.slider(
        "Offset (0 = off)",
        min_value=-100,
        max_value=100,
        step=1,
        key="brightness_beta",
        help="Pixel intensity shift. Negative = darker; positive = brighter.",
    )

    st.markdown("---")

    
    st.subheader("🔆 Contrast")
    contrast_alpha = st.slider(
        "Scale factor (1.0 = off)",
        min_value=0.5,
        max_value=3.0,
        step=0.1,
        key="contrast_alpha",
        help="Pixel value scale. < 1 reduces contrast; > 1 increases it.",
    )

    st.markdown("---")

    
    st.subheader("🔍 Edge Detection")
    edge_detect = st.checkbox(
        "Enable Canny Edge Detection",
        key="edge_detect",
        help="Highlights contours in the image using the Canny algorithm.",
    )
    if edge_detect:
        edge_thresh1 = st.slider(
            "Lower threshold",
            min_value=0,
            max_value=500,
            step=5,
            key="edge_thresh1",
        )
        edge_thresh2 = st.slider(
            "Upper threshold",
            min_value=0,
            max_value=500,
            step=5,
            key="edge_thresh2",
        )
    else:
        edge_thresh1 = st.session_state["edge_thresh1"]
        edge_thresh2 = st.session_state["edge_thresh2"]

    st.markdown("---")

    
    st.subheader("⬛ Grayscale")
    grayscale = st.checkbox(
        "Convert to Grayscale",
        key="grayscale",
        help="Converts the image to single-channel luminance.",
    )

    st.markdown("---")

    
    if st.button("🔄 Reset All Filters", use_container_width=True, on_click=reset_filters):
        pass  # reset_filters() handles state; Streamlit re-runs automatically


st.title("🖼️ Image Editor")
st.caption("Upload an image, tweak filters on the left, and download the result.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    pil_image = uploaded_file_to_pil(uploaded_file)
    original_bgr = pil_to_numpy_bgr(pil_image)

    
    processed_bgr = apply_all_filters(
        image=original_bgr,
        blur_ksize=st.session_state["blur_ksize"],
        sharpness_alpha=st.session_state["sharpness_alpha"],
        brightness_beta=st.session_state["brightness_beta"],
        contrast_alpha=st.session_state["contrast_alpha"],
        edge_detection=st.session_state["edge_detect"],
        edge_thresh1=st.session_state["edge_thresh1"],
        edge_thresh2=st.session_state["edge_thresh2"],
        gray_scale=st.session_state["grayscale"],
    )

    
    col_orig, col_proc = st.columns(2)

    with col_orig:
        st.subheader("Original")
        st.image(numpy_bgr_to_rgb(original_bgr), use_container_width=True)

    with col_proc:
        st.subheader("Processed")
        st.image(numpy_bgr_to_rgb(processed_bgr), use_container_width=True)

    
    st.markdown("---")
    png_bytes = numpy_bgr_to_png_bytes(processed_bgr)
    original_name = uploaded_file.name.rsplit(".", 1)[0]

    st.download_button(
        label="⬇️ Download Processed Image (PNG)",
        data=png_bytes,
        file_name=f"{original_name}_edited.png",
        mime="image/png",
        use_container_width=True,
    )

else:
    
    st.info("👆 Upload a JPG or PNG image to get started.")
    st.markdown(
        """
        **Supported filters:**
        | Filter | Control |
        |--------|---------|
        | 🌫️ Blur | Kernel size slider |
        | ✨ Sharpness | Alpha slider |
        | ☀️ Brightness | Offset slider |
        | 🔆 Contrast | Scale slider |
        | 🔍 Edge Detection | Toggle + thresholds |
        | ⬛ Grayscale | Toggle |
        
        Filters are **stackable** — each one is applied in sequence on top of the previous result.
        """
    )

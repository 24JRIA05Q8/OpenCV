
import streamlit as st
import cv2
import numpy as np
from PIL import Image


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="OpenCV Image Filters",
    page_icon="🎨",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎨 OpenCV Image Filters")

st.write(
    "Upload an image and use the buttons below "
    "to apply different OpenCV filters."
)


# --------------------------------------------------
# UPLOAD IMAGE
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📁 Upload an Image",
    type=["jpg", "jpeg", "png", "webp"]
)


# --------------------------------------------------
# IMAGE PROCESSING
# --------------------------------------------------

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file).convert("RGB")

    # Convert PIL image to NumPy
    original = np.array(image)

    # Convert RGB → BGR for OpenCV
    original_bgr = cv2.cvtColor(
        original,
        cv2.COLOR_RGB2BGR
    )


    # --------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------

    if "selected_filter" not in st.session_state:
        st.session_state.selected_filter = "Original"


    # --------------------------------------------------
    # FILTER FUNCTIONS
    # --------------------------------------------------

    def grayscale(img):
        return cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )


    def blur(img):
        return cv2.GaussianBlur(
            img,
            (15, 15),
            0
        )


    def edge_detection(img):
        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        return cv2.Canny(
            gray,
            100,
            200
        )


    def sharpen(img):
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

        return cv2.filter2D(
            img,
            -1,
            kernel
        )


    def sepia(img):
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])

        result = cv2.transform(
            img,
            kernel
        )

        return np.clip(
            result,
            0,
            255
        ).astype(np.uint8)


    def invert(img):
        return cv2.bitwise_not(img)


    def threshold(img):
        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        _, result = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

        return result


    # --------------------------------------------------
    # BUTTONS
    # --------------------------------------------------

    st.subheader("🎛️ Choose a Filter")

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        if st.button(
            "Original",
            use_container_width=True
        ):
            st.session_state.selected_filter = "Original"


    with col2:

        if st.button(
            "Grayscale",
            use_container_width=True
        ):
            st.session_state.selected_filter = "Grayscale"


    with col3:

        if st.button(
            "Blur",
            use_container_width=True
        ):
            st.session_state.selected_filter = "Blur"


    with col4:

        if st.button(
            "Edges",
            use_container_width=True
        ):
            st.session_state.selected_filter = "Edges"


    with col5:

        if st.button(
            "More Filters",
            use_container_width=True
        ):
            st.session_state.selected_filter = "More"


    # --------------------------------------------------
    # SELECT FILTER
    # --------------------------------------------------

    selected = st.session_state.selected_filter


    # The fifth button opens the remaining filters

    if selected == "More":

        st.subheader("✨ Additional Filters")

        filter_option = st.selectbox(
            "Choose another filter",
            [
                "Sharpen",
                "Sepia",
                "Invert",
                "Threshold"
            ]
        )

        selected = filter_option


    # --------------------------------------------------
    # APPLY FILTER
    # --------------------------------------------------

    if selected == "Original":

        result = original_bgr


    elif selected == "Grayscale":

        result = grayscale(
            original_bgr
        )


    elif selected == "Blur":

        result = blur(
            original_bgr
        )


    elif selected == "Edges":

        result = edge_detection(
            original_bgr
        )


    elif selected == "Sharpen":

        result = sharpen(
            original_bgr
        )


    elif selected == "Sepia":

        result = sepia(
            original_bgr
        )


    elif selected == "Invert":

        result = invert(
            original_bgr
        )


    elif selected == "Threshold":

        result = threshold(
            original_bgr
        )


    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------

    st.divider()

    st.subheader(
        f"🖼️ Selected Filter: {selected}"
    )


    # Convert OpenCV BGR → RGB
    # for Streamlit display

    if len(result.shape) == 2:

        display_result = result

    else:

        display_result = cv2.cvtColor(
            result,
            cv2.COLOR_BGR2RGB
        )


    st.image(
        display_result,
        caption=f"{selected} Result",
        use_container_width=True
    )


else:

    st.info(
        "👆 Please upload an image to get started."
    )

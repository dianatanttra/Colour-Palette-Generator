import streamlit as st
import cv2
import numpy as np

from modules.palette import extract_palette_with_metadata
from modules.theme import classify_theme_from_clusters
from modules.mood import detect_mood
from modules.recolor import recolor_with_palette

st.set_page_config(page_title="ColorSense", layout="wide")

st.title("🎨 ColorSense – Image Palette & Recolour Tool")

uploaded = st.file_uploader("Upload an image", type=["jpg","png","jpeg"])

if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    st.image(img_rgb, caption="Input Image", use_column_width=True)

    mode = st.sidebar.radio(
        "Choose Function",
        ["Extract Palette", "Generate Theme", "Recolour Image"]
    )

    # -------- PALETTE --------
    if mode == "Extract Palette":
        clusters = extract_palette_with_metadata(img_bgr, k=5)
        palette = np.array([c["rgb"] for c in clusters])

        st.subheader("Extracted Colour Palette")
        st.image([palette], width=500)

    # -------- THEME --------
    if mode == "Generate Theme":
        clusters = extract_palette_with_metadata(img_bgr, k=5)
        theme = classify_theme_from_clusters(clusters)
        mood = detect_mood(img_rgb)

        st.subheader(f"Detected Mood: {mood}")

        cols = st.columns(4)
        for col, (role, color) in zip(cols, theme.items()):
            block = np.ones((100,100,3), dtype=np.uint8)
            block[:] = color
            col.image(block, caption=role)

    # -------- RECOLOUR --------
    if mode == "Recolour Image":
        target = st.file_uploader("Upload target image", type=["jpg","png"])

        if target:
            t_bytes = np.asarray(bytearray(target.read()), dtype=np.uint8)
            tgt_bgr = cv2.imdecode(t_bytes, 1)
            tgt_rgb = cv2.cvtColor(tgt_bgr, cv2.COLOR_BGR2RGB)

            clusters = extract_palette_with_metadata(img_bgr, k=5)
            palette = np.array([c["rgb"] for c in clusters])

            recolored = recolor_with_palette(tgt_rgb, palette)

            col1, col2 = st.columns(2)
            col1.image(tgt_rgb, caption="Original")
            col2.image(recolored, caption="Recoloured")

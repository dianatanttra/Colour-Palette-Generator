import numpy as np
from sklearn.cluster import KMeans

def recolor_with_palette(target_img_rgb, palette_rgb):
    pixels = target_img_rgb.reshape(-1, 3)

    k = len(palette_rgb)
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(pixels)

    palette_sorted = sorted(palette_rgb.tolist(), key=lambda c: sum(c))
    centers = kmeans.cluster_centers_
    center_order = np.argsort(np.sum(centers, axis=1))

    recolored_pixels = np.zeros_like(pixels, dtype=np.uint8)

    for i, idx in enumerate(center_order):
        recolored_pixels[labels == idx] = palette_sorted[i]

    return recolored_pixels.reshape(target_img_rgb.shape)

import cv2
import numpy as np
from sklearn.cluster import KMeans

def extract_palette_with_metadata(image_bgr, k=5):
    h, w = image_bgr.shape[:2]
    img_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    flat = img_rgb.reshape(-1,3).astype(np.float32)

    edges = cv2.Canny(image_bgr, 80, 180).reshape(-1,1) / 255.0

    xs, ys = np.meshgrid(np.arange(w), np.arange(h))
    xs = (xs / w).reshape(-1,1)
    ys = (ys / h).reshape(-1,1)

    features = np.hstack([flat/255.0, xs, ys, edges])

    kmeans = KMeans(n_clusters=k, random_state=42).fit(features)
    labels = kmeans.labels_

    clusters = []

    for i in range(k):
        mask = labels == i
        if mask.sum() == 0:
            continue

        clusters.append({
            "rgb": flat[mask].mean(axis=0).astype(np.uint8),
            "edge": float(edges[mask].mean()),
            "size": float(mask.mean())
        })

    return clusters

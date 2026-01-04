import colorsys

def classify_theme_from_clusters(clusters):
    for c in clusters:
        r, g, b = c["rgb"] / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        c.update({"h":h, "s":s, "v":v})

    background = max(
        clusters,
        key=lambda c: 0.6*c["size"] + 0.3*(1-c["s"]) + 0.1*(1-c["edge"])
    )

    remaining = [c for c in clusters if c is not background]

    primary = max(remaining, key=lambda c: c["s"]*0.6 + c["size"]*0.4)
    remaining.remove(primary)

    secondary = max(remaining, key=lambda c: c["size"])
    remaining.remove(secondary)

    accent = max(remaining, key=lambda c: c["s"]*0.5 + c["edge"]*0.5)

    return {
        "Primary": primary["rgb"].tolist(),
        "Secondary": secondary["rgb"].tolist(),
        "Accent": accent["rgb"].tolist(),
        "Background": background["rgb"].tolist()
    }

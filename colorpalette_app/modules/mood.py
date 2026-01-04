import cv2
import numpy as np

def detect_mood(img_rgb):
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    avg_h, avg_s, avg_v = np.mean(h), np.mean(s), np.mean(v)

    if avg_v < 60:
        return "Dark"
    if avg_s < 40 and avg_v > 180:
        return "Pastel"
    if avg_s > 150:
        return "Vibrant"
    if 0 <= avg_h <= 20 or 160 <= avg_h <= 180:
        return "Warm"
    if 80 <= avg_h <= 140:
        return "Cool"

    return "Neutral"

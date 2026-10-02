"""Color-space helpers. All inputs are float32 sRGB-encoded RGB in [0, 1]."""
from __future__ import annotations

import cv2
import numpy as np


def rgb_to_lab(img: np.ndarray) -> np.ndarray:
    """sRGB -> CIELAB (D65). L in [0,100], a/b roughly [-128,127]."""
    return cv2.cvtColor(np.clip(img, 0, 1).astype(np.float32), cv2.COLOR_RGB2Lab)


def lab_to_rgb(lab: np.ndarray) -> np.ndarray:
    return np.clip(cv2.cvtColor(lab.astype(np.float32), cv2.COLOR_Lab2RGB), 0, 1)


def rgb_to_hsv(img: np.ndarray) -> np.ndarray:
    """H in degrees [0,360), S and V in [0,1]."""
    return cv2.cvtColor(np.clip(img, 0, 1).astype(np.float32), cv2.COLOR_RGB2HSV)


def hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    return np.clip(cv2.cvtColor(hsv.astype(np.float32), cv2.COLOR_HSV2RGB), 0, 1)


def luminance(img: np.ndarray) -> np.ndarray:
    """Lab L scaled to [0,1] -- the 'luminosity' a check layer shows."""
    return rgb_to_lab(img)[..., 0] / 100.0


def replace_luminance(img: np.ndarray, new_l01: np.ndarray) -> np.ndarray:
    """Luminosity blend: keep a*/b*, swap in a new L (0..1)."""
    lab = rgb_to_lab(img)
    lab[..., 0] = np.clip(new_l01 * 100.0, 0, 100)
    return lab_to_rgb(lab)


def gaussian(x: np.ndarray, sigma: float) -> np.ndarray:
    if sigma <= 0:
        return x.copy()
    k = int(max(3, round(sigma * 6)) | 1)
    return cv2.GaussianBlur(x, (k, k), sigma, borderType=cv2.BORDER_REFLECT)


def hue_distance(h: np.ndarray, center: float) -> np.ndarray:
    d = np.abs(h - center) % 360.0
    return np.minimum(d, 360.0 - d)


def smoothstep(e0: float, e1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - e0) / (e1 - e0 + 1e-12), 0, 1)
    return t * t * (3 - 2 * t)


def delta_e2000(lab1: np.ndarray, lab2: np.ndarray) -> np.ndarray:
    from skimage.color import deltaE_ciede2000

    return deltaE_ciede2000(lab1, lab2)

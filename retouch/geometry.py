"""Crop, rotate/straighten, perspective. Coordinates are normalized (0..1) unless noted."""
from __future__ import annotations

import math

import cv2
import numpy as np

RATIOS = {"1:1": 1.0, "4:5": 4 / 5, "5:4": 5 / 4, "3:4": 3 / 4, "4:3": 4 / 3,
          "2:3": 2 / 3, "3:2": 3 / 2, "9:16": 9 / 16, "16:9": 16 / 9}


def largest_rotated_rect(w: float, h: float, angle_rad: float) -> tuple[float, float]:
    """Largest axis-aligned rectangle inside a w x h rectangle rotated by angle."""
    if w <= 0 or h <= 0:
        return 0.0, 0.0
    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)
    sin_a, cos_a = abs(math.sin(angle_rad)), abs(math.cos(angle_rad))
    if side_short <= 2.0 * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:
        x = 0.5 * side_short
        wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a
    return wr, hr


def rotate(img: np.ndarray, degrees: float, crop: bool = True, keep_aspect: bool = True) -> np.ndarray:
    """Rotate counter-clockwise by `degrees` (positive = CCW). Crops away the blank corners."""
    if abs(degrees) < 1e-4:
        return img
    h, w = img.shape[:2]
    m = cv2.getRotationMatrix2D((w / 2, h / 2), degrees, 1.0)
    if not crop:
        cos, sin = abs(m[0, 0]), abs(m[0, 1])
        nw, nh = int(h * sin + w * cos), int(h * cos + w * sin)
        m[0, 2] += nw / 2 - w / 2
        m[1, 2] += nh / 2 - h / 2
        return cv2.warpAffine(img, m, (nw, nh), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    out = cv2.warpAffine(img, m, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    wr, hr = largest_rotated_rect(w, h, math.radians(degrees))
    if keep_aspect:
        s = min(wr / w, hr / h)
        wr, hr = w * s, h * s
    x0, y0 = int(math.ceil((w - wr) / 2)), int(math.ceil((h - hr) / 2))
    return np.ascontiguousarray(out[y0:h - y0, x0:w - x0])


def crop_box(img: np.ndarray, box: list[float]) -> np.ndarray:
    """box = [x0, y0, x1, y1] normalized."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = box
    xs = sorted((int(round(x0 * w)), int(round(x1 * w))))
    ys = sorted((int(round(y0 * h)), int(round(y1 * h))))
    xs = [max(0, min(w, v)) for v in xs]
    ys = [max(0, min(h, v)) for v in ys]
    return np.ascontiguousarray(img[ys[0]:ys[1], xs[0]:xs[1]])


def crop_ratio(img: np.ndarray, ratio: str | float, center: tuple[float, float] = (0.5, 0.5),
               scale: float = 1.0) -> np.ndarray:
    """Largest crop of `ratio` (w/h) times `scale`, centered as close to `center` as fits."""
    r = RATIOS[ratio] if isinstance(ratio, str) else float(ratio)
    h, w = img.shape[:2]
    cw, ch = (w, w / r) if w / h < r else (h * r, h)
    cw, ch = cw * scale, ch * scale
    cx = min(max(center[0] * w, cw / 2), w - cw / 2)
    cy = min(max(center[1] * h, ch / 2), h - ch / 2)
    return crop_box(img, [(cx - cw / 2) / w, (cy - ch / 2) / h, (cx + cw / 2) / w, (cy + ch / 2) / h])


def perspective(img: np.ndarray, src: list[list[float]], dst: list[list[float]] | None = None) -> np.ndarray:
    """Map 4 normalized points (TL, TR, BR, BL) to dst (default: the full frame)."""
    h, w = img.shape[:2]
    s = np.float32([[x * w, y * h] for x, y in src])
    d = np.float32([[x * w, y * h] for x, y in (dst or [[0, 0], [1, 0], [1, 1], [0, 1]])])
    m = cv2.getPerspectiveTransform(s, d)
    return cv2.warpPerspective(img, m, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)


def keystone(img: np.ndarray, vertical: float = 0.0, horizontal: float = 0.0, aspect: float = 1.0) -> np.ndarray:
    """Lightroom-like keystone sliders. vertical>0 widens the top (fixes converging verticals
    when shooting up). Values are fractions of width (e.g. 0.05). aspect stretches height."""
    # Source quad (TL, TR, BR, BL) that gets stretched to the full frame.
    tl, tr, br, bl = [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]
    v, hz = vertical / 2, horizontal / 2
    if v > 0:   # top is too narrow in the photo: pull its corners inward in the source
        tl[0] += v; tr[0] -= v
    elif v < 0:
        bl[0] -= v; br[0] += v
    if hz > 0:  # left edge too short
        tl[1] += hz; bl[1] -= hz
    elif hz < 0:
        tr[1] -= hz; br[1] += hz
    out = perspective(img, [tl, tr, br, bl])
    if abs(aspect - 1.0) > 1e-3:
        h, w = out.shape[:2]
        out = cv2.resize(out, (w, int(round(h * aspect))), interpolation=cv2.INTER_LANCZOS4)
        out = crop_ratio(out, w / h)
    return out


def detect_tilt(img: np.ndarray, max_angle: float = 12.0) -> dict:
    """Estimate camera roll from near-horizontal/near-vertical line segments.
    Returns suggested CCW rotation in degrees and the evidence behind it."""
    h, w = img.shape[:2]
    s = 1200 / max(h, w)
    small = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA) if s < 1 else img
    gray = cv2.cvtColor((np.clip(small, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    min_len = int(max(gray.shape) * 0.08)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 720, threshold=80, minLineLength=min_len, maxLineGap=6)
    if lines is None:
        return {"rotate": 0.0, "confidence": 0.0, "segments": 0}
    angs, weights = [], []
    for x1, y1, x2, y2 in np.asarray(lines).reshape(-1, 4):
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        a = math.degrees(math.atan2(dy, dx))  # image coords, y down
        a = (a + 90) % 180 - 90
        if abs(a) <= max_angle:            # near horizontal
            dev = a
        elif abs(abs(a) - 90) <= max_angle:  # near vertical
            dev = a - 90 if a > 0 else a + 90
        else:
            continue
        angs.append(dev)
        weights.append(length)
    if not angs:
        return {"rotate": 0.0, "confidence": 0.0, "segments": 0}
    angs, weights = np.array(angs), np.array(weights)
    order = np.argsort(angs)
    cum = np.cumsum(weights[order])
    median = float(angs[order][np.searchsorted(cum, cum[-1] / 2)])
    near = np.abs(angs - median) < 1.0
    conf = float(weights[near].sum() / weights.sum())
    # A line tilted by +dev (clockwise on screen, y down) is fixed by rotating CCW by +dev.
    return {"rotate": round(median, 2), "confidence": round(conf, 2), "segments": int(len(angs))}

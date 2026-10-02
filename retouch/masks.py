"""Masks: skin, luminosity, hue range, shapes, and a declarative spec builder.

A mask is float32 HxW in [0,1] (white = effect applies). Shape coordinates are
normalized to the current image (0..1), radii are fractions of image width.
"""
from __future__ import annotations

import cv2
import numpy as np

from . import color as C


# ---- luminosity masks (Kuyper/Marsh definitions: Ln = L^n, Dn = (1-L)^n) -------------
def lights(img: np.ndarray, n: int = 1) -> np.ndarray:
    return C.luminance(img) ** n


def darks(img: np.ndarray, n: int = 1) -> np.ndarray:
    return (1.0 - C.luminance(img)) ** n


def midtones(img: np.ndarray, n: int = 1) -> np.ndarray:
    """Midtones = All minus Lights_n minus Darks_n, with selection subtraction done the way
    Photoshop does it (A * (1 - B)), so M1 = L(1-L) is not zero; normalized to peak 1.
    (Plain arithmetic 1 - L - (1-L) is identically 0 for n = 1.)"""
    l = C.luminance(img)
    m = (1.0 - l ** n) * (1.0 - (1.0 - l) ** n)
    return np.clip(m / max(float(m.max()), 1e-6), 0, 1)


def zone(img: np.ndarray, center: float, width: float = 0.25) -> np.ndarray:
    """Smooth band around a luminance value (0..1)."""
    l = C.luminance(img)
    return np.clip(1.0 - np.abs(l - center) / width, 0, 1) ** 2


# ---- color masks ----------------------------------------------------------------------
def hue_range(img: np.ndarray, center: float, width: float = 30.0, soft: float = 15.0,
              sat_min: float = 0.05) -> np.ndarray:
    """Like Hue/Sat 'range': full inside +-width/2, linear falloff over `soft` degrees."""
    hsv = C.rgb_to_hsv(img)
    d = C.hue_distance(hsv[..., 0], center)
    m = np.clip(1.0 - (d - width / 2) / max(soft, 1e-6), 0, 1)
    return m * C.smoothstep(sat_min * 0.5, sat_min * 1.5 + 1e-6, hsv[..., 1])


def skin(img: np.ndarray, loose: bool = False) -> np.ndarray:
    """Skin probability from Lab hue angle/chroma (measured skin: hue ~45-70 deg, C* ~8-40).
    Combined with a YCrCb box. Soft, cleaned with morphology."""
    lab = C.rgb_to_lab(img)
    a, b = lab[..., 1], lab[..., 2]
    hue = np.degrees(np.arctan2(b, a))
    chroma = np.hypot(a, b)
    lo, hi = (25, 85) if loose else (35, 75)
    m_h = np.clip(1 - np.maximum(lo - hue, hue - hi) / 12.0, 0, 1)
    m_c = C.smoothstep(4, 9, chroma) * (1 - C.smoothstep(45 if loose else 40, 60, chroma))
    m_l = C.smoothstep(12, 25, lab[..., 0]) * (1 - C.smoothstep(96, 99.5, lab[..., 0]))
    u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    ycc = cv2.cvtColor(u8, cv2.COLOR_RGB2YCrCb).astype(np.float32)
    cr, cb = ycc[..., 1], ycc[..., 2]
    m_y = ((cr > 133 - (10 if loose else 0)) & (cr < 180) & (cb > 70) & (cb < 135)).astype(np.float32)
    m = m_h * m_c * m_l * (0.35 + 0.65 * m_y)
    h, w = m.shape
    k = max(3, int(min(h, w) * 0.004) | 1)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k * 3, k * 3)))
    return np.clip(C.gaussian(m, k), 0, 1)


# ---- shapes ---------------------------------------------------------------------------
def ellipse(shape: tuple[int, int], cx: float, cy: float, rx: float, ry: float | None = None,
            angle: float = 0.0, feather: float = 0.3) -> np.ndarray:
    """Soft ellipse. rx/ry are fractions of image width; feather is a fraction of the radius."""
    h, w = shape
    ry = rx if ry is None else ry
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x, y = xx - cx * w, yy - cy * h
    t = np.radians(angle)
    xr, yr = x * np.cos(t) + y * np.sin(t), -x * np.sin(t) + y * np.cos(t)
    r = np.sqrt((xr / (rx * w + 1e-6)) ** 2 + (yr / (ry * w + 1e-6)) ** 2)
    return (1.0 - C.smoothstep(1.0 - feather, 1.0, r)).astype(np.float32)


def polygon(shape: tuple[int, int], pts: list[list[float]], feather_px: float = 2.0) -> np.ndarray:
    h, w = shape
    m = np.zeros((h, w), np.float32)
    cv2.fillPoly(m, [np.int32([[x * w, y * h] for x, y in pts])], 1.0, lineType=cv2.LINE_AA)
    return np.clip(C.gaussian(m, feather_px), 0, 1)


def linear_gradient(shape: tuple[int, int], p0: list[float], p1: list[float]) -> np.ndarray:
    """1 at p0 fading to 0 at p1."""
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ax, ay = p0[0] * w, p0[1] * h
    dx, dy = p1[0] * w - ax, p1[1] * h - ay
    t = ((xx - ax) * dx + (yy - ay) * dy) / (dx * dx + dy * dy + 1e-6)
    return 1.0 - C.smoothstep(0.0, 1.0, t)


# ---- refinement -----------------------------------------------------------------------
def feather(m: np.ndarray, px: float) -> np.ndarray:
    return np.clip(C.gaussian(m.astype(np.float32), px), 0, 1)


def choke(m: np.ndarray, px: int) -> np.ndarray:
    """Positive px erodes (shrinks), negative dilates."""
    if px == 0:
        return m
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * abs(px) + 1, 2 * abs(px) + 1))
    return cv2.erode(m, k) if px > 0 else cv2.dilate(m, k)


def guided_refine(m: np.ndarray, img: np.ndarray, radius: int = 8, eps: float = 1e-3) -> np.ndarray:
    """Edge-aware mask refinement (He et al. guided filter), guide = luminance."""
    I = C.luminance(img).astype(np.float32)
    p = m.astype(np.float32)
    box = lambda x: cv2.boxFilter(x, -1, (2 * radius + 1, 2 * radius + 1), borderType=cv2.BORDER_REFLECT)
    mI, mp = box(I), box(p)
    a = (box(I * p) - mI * mp) / (box(I * I) - mI * mI + eps)
    b = mp - a * mI
    return np.clip(box(a) * I + box(b), 0, 1)


def grabcut(img: np.ndarray, rect: list[float], fg: list[list[float]] | None = None,
            bg: list[list[float]] | None = None, iters: int = 6, work_px: int = 1400,
            refine_radius: int = 6) -> np.ndarray:
    """Subject selection like Quick Selection / Select Subject, but classical: GrabCut graph cut
    seeded with a rectangle plus definite-foreground/background dabs ([x, y, r] normalized, r as a
    fraction of width), run on a downscaled copy, then upsampled and edge-refined against the
    full-resolution luminance with a guided filter so the edge follows the real contour."""
    h, w = img.shape[:2]
    s = min(1.0, work_px / max(h, w))
    small = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA) if s < 1 else img
    sh, sw = small.shape[:2]
    u8 = cv2.cvtColor((np.clip(small, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    mask = np.full((sh, sw), cv2.GC_BGD, np.uint8)
    x0, y0, x1, y1 = rect
    mask[int(y0 * sh):int(y1 * sh), int(x0 * sw):int(x1 * sw)] = cv2.GC_PR_FGD
    for pts, val in ((bg or [], cv2.GC_BGD), (fg or [], cv2.GC_FGD)):
        for x, y, r in pts:
            cv2.circle(mask, (int(x * sw), int(y * sh)), max(1, int(r * sw)), int(val), -1)
    bgm, fgm = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(u8, mask, None, bgm, fgm, iters, cv2.GC_INIT_WITH_MASK)
    m = np.isin(mask, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.float32)
    # keep the component(s) touching definite foreground only
    n, lab = cv2.connectedComponents((m > 0).astype(np.uint8))
    keep = set()
    for x, y, r in fg or []:
        v = lab[min(sh - 1, int(y * sh)), min(sw - 1, int(x * sw))]
        if v > 0:
            keep.add(int(v))
    if keep:
        m = np.isin(lab, list(keep)).astype(np.float32)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)
    return guided_refine(m, img, radius=refine_radius, eps=2e-4)


# ---- declarative spec -----------------------------------------------------------------
def build(img: np.ndarray, spec: dict | None, ctx: dict | None = None) -> np.ndarray | None:
    """Build a mask from a dict, e.g.
    {"skin": true, "include": [{"ellipse": [cx,cy,rx,ry,angle]}],
     "exclude": [{"ellipse": [...]}, {"polygon": [[x,y],...]}],
     "lum": "lights2" | "darks1" | "mid2" | {"zone": [c, w]},
     "hue": [center, width], "feather": px, "choke": px, "invert": false, "opacity": 1.0}
    Face-parsing parts (needs ctx with a "prob" array or a "parse" callable):
     "parts": ["face_skin", "neck"], "exclude_parts": ["eyes", "brows", "lips"]
    Groups: face_skin, skin_all, eyes, brows, lips, teeth, ears, hair, neck, cloth, nose, skin.
    Components multiply (intersection); include shapes union together first.
    """
    if not spec:
        return None
    h, w = img.shape[:2]
    m = np.ones((h, w), np.float32)

    def shape_mask(s: dict) -> np.ndarray:
        if "ellipse" in s:
            e = s["ellipse"]
            cx, cy, rx = e[0], e[1], e[2]
            ry = e[3] if len(e) > 3 else rx
            ang = e[4] if len(e) > 4 else 0.0
            return ellipse((h, w), cx, cy, rx, ry, ang, s.get("feather", 0.3))
        if "polygon" in s:
            return polygon((h, w), s["polygon"], s.get("feather_px", 2.0))
        if "gradient" in s:
            return linear_gradient((h, w), *s["gradient"])
        if "rect" in s:
            x0, y0, x1, y1 = s["rect"]
            return polygon((h, w), [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], s.get("feather_px", 2.0))
        raise ValueError(f"unknown shape {s}")

    if spec.get("parts") or spec.get("exclude_parts"):
        from . import faces as F
        if ctx is None or ctx.get("prob") is None or ctx["prob"].shape[1:] != (h, w):
            if ctx is None:
                ctx = {}
            ctx["prob"] = F.parse(img)
        prob = ctx["prob"]
        if spec.get("parts"):
            m *= F.part_mask(prob, spec["parts"], spec.get("parts_soften", 1.5))
        if spec.get("exclude_parts"):
            ex = F.part_mask(prob, spec["exclude_parts"], 0)
            ex = choke(ex, -int(spec.get("exclude_grow", 2)))
            m *= 1.0 - feather(ex, spec.get("exclude_feather", 2.0))
    if spec.get("grabcut"):
        g = dict(spec["grabcut"])
        key = "grabcut:" + repr(sorted(g.items()))
        if ctx is not None and key in ctx:
            gm = ctx[key]
        else:
            gm = grabcut(img, **g)
            if ctx is not None:
                ctx[key] = gm
        if spec.get("grabcut_union"):
            for s2 in spec["grabcut_union"]:
                gm = np.maximum(gm, shape_mask(s2))
        m *= gm
    if spec.get("minus"):                 # mask math: subtract another mask spec
        m *= 1.0 - build(img, spec["minus"], ctx)
    if spec.get("skin"):
        m *= skin(img, loose=spec.get("skin") == "loose")
    if spec.get("include"):
        inc = np.zeros((h, w), np.float32)
        for s in spec["include"]:
            inc = np.maximum(inc, shape_mask(s))
        m *= inc
    lum = spec.get("lum")
    if isinstance(lum, str):
        kind, n = lum.rstrip("0123456789"), int(lum[len(lum.rstrip("0123456789")):] or 1)
        m *= {"lights": lights, "darks": darks, "mid": midtones}[kind](img, n)
    elif isinstance(lum, dict) and "zone" in lum:
        m *= zone(img, *lum["zone"])
    if spec.get("hue"):
        m *= hue_range(img, *spec["hue"])
    for s in spec.get("exclude", []):
        m *= 1.0 - shape_mask(s)
    if spec.get("choke"):
        m = choke(m, int(spec["choke"]))
    if spec.get("feather"):
        m = feather(m, float(spec["feather"]))
    if spec.get("invert"):
        m = 1.0 - m
    return np.clip(m * float(spec.get("opacity", 1.0)), 0, 1)

"""Non-destructive retouching operations, modelled on how high-end retouchers work.

Every op takes float32 sRGB RGB [0,1] and returns a new image of the same size.
The pipeline blends op output through a mask (out = img + mask * (op(img) - img)),
which is the code equivalent of an adjustment layer with a layer mask.
Pixel sizes (sigma, radius) are in pixels of the current image.
"""
from __future__ import annotations

import math

import cv2
import numpy as np
from scipy.interpolate import PchipInterpolator

from . import color as C


# ---- tone ------------------------------------------------------------------------------
def _curve_lut(points: list[list[float]], n: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    pts = sorted((float(x) / 255.0, float(y) / 255.0) for x, y in points)
    if pts[0][0] > 0:
        pts.insert(0, (0.0, pts[0][1] if len(pts) == 1 else 0.0))
    if pts[-1][0] < 1:
        pts.append((1.0, 1.0))
    xs, ys = zip(*pts)
    x = np.linspace(0, 1, n)
    return x, np.clip(PchipInterpolator(xs, ys)(x), 0, 1)


def apply_curve(x: np.ndarray, points: list[list[float]]) -> np.ndarray:
    lx, ly = _curve_lut(points)
    return np.interp(np.clip(x, 0, 1), lx, ly).astype(np.float32)


def curves(img: np.ndarray, points: list[list[float]], channel: str = "rgb") -> np.ndarray:
    """Photoshop-style curve, points as [[in, out], ...] in 0..255.
    channel: rgb | r | g | b | lum (luminosity blend: tone only, no saturation shift)."""
    if channel == "lum":
        return C.replace_luminance(img, apply_curve(C.luminance(img), points))
    out = img.copy()
    idx = {"rgb": [0, 1, 2], "r": [0], "g": [1], "b": [2]}[channel]
    for i in idx:
        out[..., i] = apply_curve(img[..., i], points)
    return out


def levels(img: np.ndarray, black: float = 0, white: float = 255, gamma: float = 1.0,
           out_black: float = 0, out_white: float = 255) -> np.ndarray:
    x = np.clip((img * 255 - black) / max(white - black, 1e-6), 0, 1) ** (1 / gamma)
    return (out_black + x * (out_white - out_black)) / 255.0


def _to_linear(x: np.ndarray) -> np.ndarray:
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def _to_srgb(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0, None)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def exposure(img: np.ndarray, ev: float = 0.0, highlight_rolloff: bool = True) -> np.ndarray:
    lin = _to_linear(img) * (2.0 ** ev)
    if highlight_rolloff and ev > 0:
        lin = np.where(lin > 0.8, 0.8 + (1 - np.exp(-(lin - 0.8) / 0.2)) * 0.2, lin)
    return np.clip(_to_srgb(lin), 0, 1).astype(np.float32)


def shadows_highlights(img: np.ndarray, shadows: float = 0.0, highlights: float = 0.0,
                       sigma: float = 30.0) -> np.ndarray:
    """Local tone recovery on L. shadows>0 lifts, highlights>0 pulls down. Range ~0..1."""
    L = C.luminance(img)
    base = C.gaussian(L, sigma)
    lift = shadows * 0.35 * (1 - C.smoothstep(0.0, 0.5, base))
    pull = highlights * 0.35 * C.smoothstep(0.5, 1.0, base)
    newL = L + lift * (1 - L) - pull * L
    return C.replace_luminance(img, newL)


def local_contrast(img: np.ndarray, amount: float = 0.2, sigma: float = 40.0,
                   support: np.ndarray | None = None) -> np.ndarray:
    """Clarity-like midtone contrast on L (keep small for portraits).
    With `support` (a mask), the local average is taken only inside the mask, so a dark sky
    next to bright land cannot push a bright rim (halo) onto the land edge, and vice versa."""
    L = C.luminance(img)
    if support is None:
        detail = L - C.gaussian(L, sigma)
    else:
        wgt = (support > 0.5).astype(np.float32)
        base = C.gaussian(L * wgt, sigma) / np.maximum(C.gaussian(wgt, sigma), 1e-4)
        detail = (L - base) * wgt
    mid = 1 - np.abs(L - 0.5) * 2
    return C.replace_luminance(img, L + amount * detail * (0.4 + 0.6 * mid))


# ---- color -----------------------------------------------------------------------------
def white_balance(img: np.ndarray, temp: float = 0.0, tint: float = 0.0) -> np.ndarray:
    """temp>0 warmer, tint>0 more magenta. Units ~ -1..1, applied in linear light."""
    lin = _to_linear(img)
    gains = np.array([1 + 0.25 * temp, 1 - 0.2 * tint, 1 - 0.25 * temp], np.float32)
    lin = lin * gains
    return np.clip(_to_srgb(lin), 0, 1).astype(np.float32)


def neutralize(img: np.ndarray, x: float, y: float, r: float = 0.01, strength: float = 1.0) -> np.ndarray:
    """Make the sampled patch neutral grey (gray-point eyedropper), in linear light."""
    h, w = img.shape[:2]
    rr = max(2, int(r * w))
    cx, cy = int(x * w), int(y * h)
    patch = _to_linear(img[max(0, cy - rr):cy + rr, max(0, cx - rr):cx + rr]).reshape(-1, 3).mean(0)
    target = patch.mean()
    gains = 1 + strength * (target / np.maximum(patch, 1e-6) - 1)
    return np.clip(_to_srgb(_to_linear(img) * gains), 0, 1).astype(np.float32)


def saturation(img: np.ndarray, amount: float = 0.0) -> np.ndarray:
    lab = C.rgb_to_lab(img)
    lab[..., 1:] *= 1 + amount
    return C.lab_to_rgb(lab)


def vibrance(img: np.ndarray, amount: float = 0.0, protect_skin: bool = True) -> np.ndarray:
    lab = C.rgb_to_lab(img)
    chroma = np.hypot(lab[..., 1], lab[..., 2])
    w = 1 - C.smoothstep(10, 60, chroma)
    if protect_skin:
        hue = np.degrees(np.arctan2(lab[..., 2], lab[..., 1]))
        w *= 1 - 0.7 * np.clip(1 - np.abs(hue - 55) / 25, 0, 1)
    lab[..., 1:] *= (1 + amount * w)[..., None]
    return C.lab_to_rgb(lab)


def hue_sat(img: np.ndarray, center: float, width: float = 30.0, soft: float = 20.0,
            hue: float = 0.0, sat: float = 0.0, light: float = 0.0) -> np.ndarray:
    """Targeted Hue/Saturation like Photoshop's Reds/Yellows range.
    hue in degrees, sat and light in -1..1."""
    hsv = C.rgb_to_hsv(img)
    d = C.hue_distance(hsv[..., 0], center)
    w = np.clip(1.0 - (d - width / 2) / max(soft, 1e-6), 0, 1) * C.smoothstep(0.02, 0.08, hsv[..., 1])
    L0 = C.luminance(img)
    hsv[..., 0] = (hsv[..., 0] + hue * w) % 360
    hsv[..., 1] = np.clip(hsv[..., 1] * (1 + sat * w), 0, 1)
    # Desaturating at constant HSV value brightens (and saturating darkens) the pixel. Keep the
    # original luminance so hue/sat moves color only; tone changes go through `light`.
    out = C.replace_luminance(C.hsv_to_rgb(hsv), L0)
    if light:
        L = C.luminance(out)
        L = L + light * w * (1 - L if light > 0 else L)
        out = C.replace_luminance(out, L)
    return out


def mono(img: np.ndarray, r: float = 0.4, g: float = 0.4, b: float = 0.2, tone: list | None = None,
         tone_amount: float = 0.0) -> np.ndarray:
    """Channel Mixer black & white (weights like colour filters on film: red filter = high r,
    darkens greens and blue water). Optional split tone colour (rgb 0..255) for a toned print."""
    wsum = r + g + b
    lin = _to_linear(img)
    y = (lin[..., 0] * r + lin[..., 1] * g + lin[..., 2] * b) / max(wsum, 1e-6)
    out = np.repeat(_to_srgb(np.clip(y, 0, 1))[..., None], 3, -1).astype(np.float32)
    if tone and tone_amount:
        t = np.array(tone, np.float32) / 255.0
        L = C.luminance(out)
        out = C.replace_luminance(out + tone_amount * (t - out.mean(-1, keepdims=True)) * 1.0, L)
    return np.clip(out, 0, 1)


def lab_shift(img: np.ndarray, da: float = 0.0, db: float = 0.0, dl: float = 0.0) -> np.ndarray:
    lab = C.rgb_to_lab(img)
    lab[..., 0] += dl
    lab[..., 1] += da
    lab[..., 2] += db
    return C.lab_to_rgb(lab)


def match_skin(img: np.ndarray, mask: np.ndarray, hue: float = 58.0, chroma: float | None = None,
               strength: float = 0.5) -> np.ndarray:
    """Nudge the masked region's mean Lab hue (and optionally chroma) toward a target.
    Measured skin hue angles cluster ~53-62 deg (b* >= a*)."""
    lab = C.rgb_to_lab(img)
    wsum = mask.sum() + 1e-6
    a = float((lab[..., 1] * mask).sum() / wsum)
    b = float((lab[..., 2] * mask).sum() / wsum)
    cur_c = math.hypot(a, b)
    tgt_c = cur_c if chroma is None else chroma
    ta, tb = tgt_c * math.cos(math.radians(hue)), tgt_c * math.sin(math.radians(hue))
    lab[..., 1] += strength * (ta - a)
    lab[..., 2] += strength * (tb - b)
    return C.lab_to_rgb(lab)


def color_balance(img: np.ndarray, shadows=(0, 0, 0), midtones=(0, 0, 0), highlights=(0, 0, 0)) -> np.ndarray:
    """Each tuple = (cyan-red, magenta-green, yellow-blue) in -1..1 (≈ PS slider/100)."""
    L = C.luminance(img)[..., None]
    ws = (1 - C.smoothstep(0.0, 0.5, L))
    wh = C.smoothstep(0.5, 1.0, L)
    wm = 1 - ws - wh
    shift = (np.array(shadows, np.float32) * ws + np.array(midtones, np.float32) * wm
             + np.array(highlights, np.float32) * wh) * 0.15
    out = np.clip(img + shift, 0, 1)
    return C.replace_luminance(out, L[..., 0])


def split_tone(img: np.ndarray, shadow_hue: float = 200, shadow_sat: float = 0.0,
               highlight_hue: float = 40, highlight_sat: float = 0.0, balance: float = 0.0) -> np.ndarray:
    """Color-grade wheels: tint shadows/highlights by hue (deg) and amount (0..1), keep L."""
    lab = C.rgb_to_lab(img)
    L = lab[..., 0] / 100
    pivot = 0.5 + balance * 0.25
    ws = 1 - C.smoothstep(0.0, pivot, L)
    wh = C.smoothstep(pivot, 1.0, L)
    for hue, sat, wgt in ((shadow_hue, shadow_sat, ws), (highlight_hue, highlight_sat, wh)):
        if sat:
            lab[..., 1] += 20 * sat * math.cos(math.radians(hue)) * wgt
            lab[..., 2] += 20 * sat * math.sin(math.radians(hue)) * wgt
    return C.lab_to_rgb(lab)


def gradient_map(img: np.ndarray, stops: list[list], opacity: float = 0.15,
                 preserve_luminosity: bool = True) -> np.ndarray:
    """stops = [[pos 0..1, [r,g,b] 0..255], ...]; blended at low opacity as pros do."""
    L = C.luminance(img)
    pos = np.array([s[0] for s in stops], np.float32)
    cols = np.array([s[1] for s in stops], np.float32) / 255
    mapped = np.stack([np.interp(L, pos, cols[:, i]) for i in range(3)], -1).astype(np.float32)
    if preserve_luminosity:
        mapped = C.replace_luminance(mapped, L)
    return img + opacity * (mapped - img)


def lut3d(img: np.ndarray, lut: np.ndarray, opacity: float = 1.0) -> np.ndarray:
    """Apply an NxNxNx3 LUT (indexed [r,g,b]) with trilinear interpolation."""
    from scipy.ndimage import map_coordinates

    n = lut.shape[0]
    coords = np.clip(img, 0, 1).reshape(-1, 3).T * (n - 1)
    out = np.stack([map_coordinates(lut[..., c], coords, order=1) for c in range(3)], -1)
    out = out.reshape(img.shape).astype(np.float32)
    return img + opacity * (out - img)


# ---- skin: frequency-band dodge & burn ------------------------------------------------
def band(x: np.ndarray, s_lo: float, s_hi: float, support: np.ndarray | None = None) -> np.ndarray:
    """Difference of Gaussians: detail between s_lo and s_hi (pores below s_lo stay out).
    With `support`, blurs are normalized convolutions over the support only, so hair, eyes or
    background next to the skin cannot bias the skin's local average (no dark/bright rims)."""
    if support is None:
        return C.gaussian(x, s_lo) - C.gaussian(x, s_hi)
    w = support.astype(np.float32)
    nb = lambda s: C.gaussian(x * w, s) / np.maximum(C.gaussian(w, s), 1e-4)
    return (nb(s_lo) - nb(s_hi)) * (w > 0)


def micro_db(img: np.ndarray, mask: np.ndarray, s_lo: float = 2.0, s_hi: float = 14.0,
             strength: float = 0.6, cap: float = 5.0) -> np.ndarray:
    """Automatic micro dodge & burn: even mid-frequency luminance blotches inside the mask.

    Pores and fine texture (< s_lo) and facial volume (> s_hi) are untouched, which is what
    hand D&B achieves. Deviations much larger than `cap` (L units) fade out of the correction:
    they are usually features (lash line, nostril, wrinkle) and belong to healing or manual work.
    """
    lab = C.rgb_to_lab(img)
    L = lab[..., 0]
    m = mask.astype(np.float32)
    d = band(L, s_lo, s_hi, support=(m > 0.3))
    keep = np.exp(-0.5 * (d / max(cap, 1e-6)) ** 2)
    lab[..., 0] = L - strength * d * keep * m
    return C.lab_to_rgb(lab)


def color_even(img: np.ndarray, mask: np.ndarray, s_lo: float = 3.0, s_hi: float = 25.0,
               strength: float = 0.6, cap: float = 4.0) -> np.ndarray:
    """Even blotchy redness/yellowness (a*/b* mid-band) inside the mask; keeps L untouched."""
    lab = C.rgb_to_lab(img)
    for ch in (1, 2):
        d = band(lab[..., ch], s_lo, s_hi, support=(mask > 0.3))
        keep = np.exp(-0.5 * (d / max(cap, 1e-6)) ** 2)
        lab[..., ch] -= strength * d * keep * mask
    return C.lab_to_rgb(lab)


def dodge_burn(img: np.ndarray, strokes: list[dict]) -> np.ndarray:
    """Manual (macro) D&B. Each stroke: {"ellipse": [cx,cy,rx,ry,angle], "amount": +/-L units,
    "feather": 0..1}. Applied to luminosity only (no saturation shift)."""
    from . import masks as M

    h, w = img.shape[:2]
    L = C.luminance(img)
    delta = np.zeros((h, w), np.float32)
    for s in strokes:
        e = s["ellipse"]
        m = M.ellipse((h, w), e[0], e[1], e[2], e[3] if len(e) > 3 else None,
                      e[4] if len(e) > 4 else 0.0, s.get("feather", 0.8))
        delta += m * s["amount"] / 100.0
    return C.replace_luminance(img, L + delta)


def color_fix(img: np.ndarray, mask: np.ndarray, sample: list[float] | None = None,
              rgb: list[float] | None = None, mode: str = "color", opacity: float = 0.3) -> np.ndarray:
    """Pratik Naik's 'Color Fix': paint a sampled good skin tone at low opacity on a layer in
    Color mode (hue + chroma replaced, luminance kept) or Hue mode (hue only, chroma kept).
    sample = [x, y, r] normalized (5x5-average eyedropper equivalent), or rgb 0..255."""
    lab = C.rgb_to_lab(img)
    if sample is not None:
        h, w = img.shape[:2]
        rr = max(2, int(sample[2] * w))
        cx, cy = int(sample[0] * w), int(sample[1] * h)
        ta, tb = lab[max(0, cy - rr):cy + rr, max(0, cx - rr):cx + rr, 1:].reshape(-1, 2).mean(0)
    else:
        ta, tb = C.rgb_to_lab(np.array([[rgb]], np.float32) / 255.0)[0, 0, 1:]
    a, b = lab[..., 1], lab[..., 2]
    if mode == "hue":
        c = np.hypot(a, b)
        t = math.atan2(tb, ta)
        na, nb = c * math.cos(t), c * math.sin(t)
    else:
        na, nb = np.full_like(a, ta), np.full_like(b, tb)
    k = mask * opacity
    lab[..., 1] = a + k * (na - a)
    lab[..., 2] = b + k * (nb - b)
    return C.lab_to_rgb(lab)


def shine_reduce(img: np.ndarray, mask: np.ndarray, threshold: float = 0.80, amount: float = 0.5,
                 sigma: float = 6.0) -> np.ndarray:
    """Pull specular hot spots on skin down toward their surroundings without killing them."""
    lab = C.rgb_to_lab(img)
    L = lab[..., 0] / 100
    hot = C.smoothstep(threshold, min(1.0, threshold + 0.12), C.gaussian(L, sigma / 3)) * mask
    surround = C.gaussian(L, sigma * 3)
    # lower only the low-frequency excess, so pores and texture inside the highlight survive
    low = C.gaussian(L, sigma / 2)
    target = L - amount * hot * np.maximum(low - surround, 0)
    lab[..., 0] = target * 100
    # Specular spots are desaturated; give back a little of the surrounding skin color.
    for ch in (1, 2):
        lab[..., ch] += amount * 0.5 * hot * (C.gaussian(lab[..., ch], sigma * 3) - lab[..., ch])
    return C.lab_to_rgb(lab)


# ---- healing ---------------------------------------------------------------------------
def fill_from_surround(x: np.ndarray, hole: np.ndarray, sigma: float = 4.0, levels: int = 5) -> np.ndarray:
    """Fill `hole` (bool/0-1, HxW) from surrounding pixels by multi-scale normalized convolution.
    Smooth, exact outside the hole, works on float data of any channel count (cv2.inpaint is
    unreliable on float32 in OpenCV 5)."""
    known = (hole < 0.5).astype(np.float32)
    x = x.astype(np.float32)
    xs = x if x.ndim == 3 else x[..., None]
    out = xs.copy()
    filled = known.copy()
    for i in range(levels):
        sg = sigma * (2 ** i)
        wsum = C.gaussian(known, sg)
        est = np.stack([C.gaussian(xs[..., c] * known, sg) for c in range(xs.shape[2])], -1) / np.maximum(wsum, 1e-6)[..., None]
        take = (filled < 0.5) & (wsum > 1e-3)
        out[take] = est[take]
        filled = np.maximum(filled, take.astype(np.float32))
        if filled.min() >= 0.5:
            break
    # one smoothing pass inside the hole so the fill has no level seams
    sm = np.stack([C.gaussian(out[..., c], sigma) for c in range(out.shape[2])], -1)
    h = (hole >= 0.5)[..., None]
    out = np.where(h, sm, xs)
    return out if x.ndim == 3 else out[..., 0]

def _disk(h: int, w: int, cx: float, cy: float, r: float, feather: float = 0.35) -> np.ndarray:
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy) / max(r, 1e-6)
    return 1 - C.smoothstep(1 - feather, 1.0, d)


def heal(img: np.ndarray, spots: list[dict], search: float = 3.0) -> np.ndarray:
    """Texture-preserving healing brush.

    For each spot {"x","y","r"} (normalized; r = fraction of width) the tone underneath is
    rebuilt from the surroundings (inpainted low frequencies), and fresh texture (high
    frequencies) is borrowed from the best nearby source patch -- the same split the Healing
    Brush does. Optional "src": [x, y] forces the source like Alt-clicking.
    """
    out = img.copy()
    H, W = img.shape[:2]
    for sp in spots:
        r = max(2.0, sp["r"] * W)
        cx, cy = sp["x"] * W, sp["y"] * H
        pad = int(r * (search + 2.5))
        x0, y0 = max(0, int(cx - pad)), max(0, int(cy - pad))
        x1, y1 = min(W, int(cx + pad)), min(H, int(cy + pad))
        reg = out[y0:y1, x0:x1].copy()
        h, w = reg.shape[:2]
        lcx, lcy = cx - x0, cy - y0
        disk = _disk(h, w, lcx, lcy, r)
        hard = (disk > 0.02).astype(np.uint8)
        sig = max(0.8, r / 3.0)
        low = np.stack([C.gaussian(reg[..., c], sig) for c in range(3)], -1)
        high = reg - low
        filled = fill_from_surround(low, hard, sigma=max(1.5, r / 2))
        filled = np.stack([C.gaussian(filled[..., c], sig * 0.5) for c in range(3)], -1)

        # choose texture source
        best, best_off = None, (0, 0)
        if "src" in sp:
            cands = [(sp["src"][0] * W - cx, sp["src"][1] * H - cy)]
        else:
            cands = [(math.cos(t) * r * k, math.sin(t) * r * k)
                     for k in (2.2, 3.0) for t in np.linspace(0, 2 * math.pi, 16, endpoint=False)]
        ring = (disk < 0.02) & (_disk(h, w, lcx, lcy, r * 2.0) > 0.5)
        ring_std = float(high[ring].std()) if ring.any() else float(high.std())
        for dx, dy in cands:
            sx, sy = lcx + dx, lcy + dy
            if not (r <= sx < w - r and r <= sy < h - r):
                continue
            m = cv2.getRotationMatrix2D((0, 0), 0, 1.0)
            m[:, 2] = (dx, dy)
            shifted_high = cv2.warpAffine(high, m, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                                          borderMode=cv2.BORDER_REFLECT)
            shifted_low = cv2.warpAffine(low, m, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                                         borderMode=cv2.BORDER_REFLECT)
            sel = disk > 0.5
            tone = float(np.abs(shifted_low[sel] - filled[sel]).mean())
            tex = abs(float(shifted_high[sel].std()) - ring_std) / (ring_std + 1e-4)
            score = tone * 10 + tex
            if best is None or score < best:
                best, best_off, best_high = score, (dx, dy), shifted_high
        if best is None:
            best_high = np.zeros_like(high)
        patched = filled + best_high
        out[y0:y1, x0:x1] = reg + disk[..., None] * (patched - reg)
    return np.clip(out, 0, 1)


def remove_lines(img: np.ndarray, mask: np.ndarray, width_px: float = 3.0, threshold: float = 2.5,
                 dark: bool = True) -> np.ndarray:
    """Remove thin straight wires over smooth areas (sky) -- spot healing along a path.
    Wires are found as straight segments (Hough) in a morphological black-hat (top-hat for light
    wires) inside `mask`, drawn as a thin band, kept strictly inside the mask, and filled from the
    surrounding sky by normalized convolution (no generative fill)."""
    L = (C.luminance(img) * 255).astype(np.float32)
    k = int(max(3, round(width_px * 3)) | 1)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    resp = cv2.morphologyEx(L, cv2.MORPH_BLACKHAT if dark else cv2.MORPH_TOPHAT, se)
    # the region the wires cross: the mask with the wires themselves closed over, kept a few px
    # away from anything that is not sky (ridge lines, roofs)
    sel = mask > 0.5
    region = cv2.morphologyEx(sel.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1)))
    region = cv2.erode(region, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
    sel = region
    noise = float(np.median(resp[sel])) * 1.4826 + 0.5 if sel.any() else 1.0
    binary = ((resp > threshold * noise + 1.0) & sel).astype(np.uint8) * 255
    h, w = L.shape
    segs = cv2.HoughLinesP(binary, 1, np.pi / 720, threshold=30, minLineLength=int(max(h, w) * 0.04), maxLineGap=12)
    band = np.zeros((h, w), np.uint8)
    sky = mask > 0.5
    # local texture: wires are only removed over smooth areas (sky); over foliage or ridges a
    # fill would smear real detail, which is a clone-stamp job instead
    wire_px = cv2.dilate(binary, np.ones((5, 5), np.uint8))
    mu = cv2.blur(L, (7, 7))
    lstd = np.sqrt(np.maximum(cv2.blur(L * L, (7, 7)) - mu * mu, 0))
    off = width_px + 4
    thick = int(round(width_px * 2 + 3))
    for x1, y1, x2, y2 in (np.asarray(segs).reshape(-1, 4) if segs is not None else []):
        length = math.hypot(x2 - x1, y2 - y1)
        if length < 1:
            continue
        nx, ny = -(y2 - y1) / length, (x2 - x1) / length
        n = int(length // 2) + 1
        for t in np.linspace(0, 1, n):
            px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
            pts = []
            for sgn in (1, -1):  # step past neighbouring parallel wires to reach clean sky
                q = None
                for mult in (1, 2, 3, 4):
                    qx, qy = px + sgn * nx * off * mult, py + sgn * ny * off * mult
                    if not (0 <= int(qy) < h and 0 <= int(qx) < w):
                        break
                    q = (qx, qy)
                    if wire_px[int(qy), int(qx)] == 0:
                        break
                pts.append(q if q is not None else (-1, -1))
            # a wire has sky on both sides; a ridge or roof edge does not
            # at the frame border only one side exists; judge by that side alone
            pts = [q for q in pts if 0 <= int(q[1]) < h and 0 <= int(q[0]) < w] or pts
            inside = all(0 <= int(qy) < h and 0 <= int(qx) < w and sky[int(qy), int(qx)] for qx, qy in pts)
            if inside and abs(L[int(pts[0][1]), int(pts[0][0])] - L[int(pts[-1][1]), int(pts[-1][0])]) < 14 \
                    and max(lstd[int(qy), int(qx)] for qx, qy in pts) < 4.0:
                cv2.circle(band, (int(round(px)), int(round(py))), thick // 2 + 1, 1, -1)
    band &= sel.astype(np.uint8)
    if not band.any():
        return img
    out = fill_from_surround(img, band, sigma=max(2.0, width_px))
    out = _match_grain(img, out, band)
    soft = C.gaussian(band.astype(np.float32), 0.8)[..., None]
    return np.clip(img + soft * (out - img), 0, 1)


def _match_grain(img: np.ndarray, out: np.ndarray, hole: np.ndarray, seed: int = 11) -> np.ndarray:
    """Give a smooth fill the fine luminance grain measured just outside it."""
    Lh = C.luminance(img)
    hf = Lh - C.gaussian(Lh, 1.0)
    ring = (cv2.dilate(hole.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0) & (hole == 0)
    g = float(hf[ring].std()) * 0.5 if ring.any() else 0.0
    if g <= 0:
        return out
    n = np.random.default_rng(seed).standard_normal(hole.shape).astype(np.float32)
    n = C.gaussian(n, 0.9)
    n *= g / (float(n.std()) + 1e-6)
    return C.replace_luminance(out, C.luminance(out) + n * (hole > 0))


def clone(img: np.ndarray, dst: list[float], src: list[float], r: float, feather: float = 0.5) -> np.ndarray:
    """Clone Stamp: copy a soft disk from src to dst (normalized coords, r = fraction of width)."""
    H, W = img.shape[:2]
    dx, dy = (src[0] - dst[0]) * W, (src[1] - dst[1]) * H
    m = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted = cv2.warpAffine(img, m, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                             borderMode=cv2.BORDER_REFLECT)
    disk = _disk(H, W, dst[0] * W, dst[1] * H, r * W, feather)
    return img + disk[..., None] * (shifted - img)


def deghost(img: np.ndarray, cx: float, cy: float, r: float, sectors: int = 12,
            ref: tuple[float, float] = (1.06, 1.45), feather: float = 0.1, nq: int = 96,
            fade_toward: tuple[float, float] | None = None, fade: float = 0.0) -> np.ndarray:
    """Remove a lens-flare ghost (the coloured disc a bright source throws across the frame).
    Phone pipelines tone-map the ghost, so it is neither purely additive nor a plain tint. Like a
    retoucher matching a patch to its surroundings, each angular sector of the disc is matched to
    the ring of untouched scene just outside it at the same angle: lightness by full quantile
    mapping, a*/b* by mean/spread transfer (per-channel rank mapping speckles). Sectors blend
    smoothly, and because each matches its own neighbourhood, real light (the sun's glow on one
    side) is kept. cx, cy are fractions of width/height; r is a fraction of width.
    `fade_toward` = [x, y] of the light source: the correction eases off on the side of the disc
    facing it by `fade` (0..1), where ghost and real glare overlap and real glare should win."""
    h, w = img.shape[:2]
    cx, cy, r = cx * w, cy * h, r * w
    R = r * ref[1]
    x0, x1 = int(max(0, cx - R)), int(min(w, cx + R + 1))
    y0, y1 = int(max(0, cy - R)), int(min(h, cy + R + 1))
    sub = img[y0:y1, x0:x1]
    lab = C.rgb_to_lab(sub)
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy) / r
    th = np.arctan2(yy - cy, xx - cx)
    inside, ring = d < 1.0, (d > ref[0]) & (d < ref[1])
    qs = np.linspace(0, 100, nq)
    acc = np.zeros_like(lab)
    wsum = np.zeros(sub.shape[:2], np.float32)
    sw = 2 * np.pi / sectors
    for k in range(sectors):
        ad = np.abs(np.angle(np.exp(1j * (th - (-np.pi + (k + 0.5) * sw)))))
        sel_in, sel_rf = inside & (ad < sw * 0.75), ring & (ad < sw * 0.75)
        if sel_in.sum() < 500 or sel_rf.sum() < 500:
            continue
        mk = np.empty_like(lab)
        qi = np.maximum.accumulate(np.percentile(lab[..., 0][sel_in], qs) + np.arange(nq) * 1e-6)
        mk[..., 0] = np.interp(lab[..., 0], qi, np.percentile(lab[..., 0][sel_rf], qs))
        for c in (1, 2):
            mi, si = lab[..., c][sel_in].mean(), lab[..., c][sel_in].std() + 1e-3
            mr, sr = lab[..., c][sel_rf].mean(), lab[..., c][sel_rf].std() + 1e-3
            mk[..., c] = mr + (lab[..., c] - mi) * min(sr / si, 1.2)
        wk = np.exp(-0.5 * (ad / (sw * 0.6)) ** 2).astype(np.float32)
        acc += wk[..., None] * mk
        wsum += wk
    mapped = C.lab_to_rgb(acc / np.maximum(wsum, 1e-6)[..., None])
    m = (1 - C.smoothstep(1 - feather, 1 + feather * 0.3, d)).astype(np.float32)
    if fade_toward is not None and fade > 0:
        ux, uy = fade_toward[0] * w - cx, fade_toward[1] * h - cy
        n = math.hypot(ux, uy) + 1e-6
        proj = ((xx - cx) * ux + (yy - cy) * uy) / (n * r)      # -1 (far side) .. 1 (toward source)
        m *= 1 - fade * C.smoothstep(0.2, 0.95, proj)
    out = img.copy()
    out[y0:y1, x0:x1] = sub + m[..., None] * (mapped - sub)
    return np.clip(out, 0, 1).astype(np.float32)


def shadow_fix(img: np.ndarray, mask: np.ndarray, sigma: float = 6.0) -> np.ndarray:
    """Lift an unwanted cast shadow (a blurred dark blob on a lit surface) without touching texture:
    the surface's own brightness under the shadow is interpolated from around the mask, and the
    pixels are multiplied (in linear light) by expected/actual low-pass luminance."""
    lin = _to_linear(img)
    Y = lin @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lp = C.gaussian(Y, sigma)
    hole = (mask > 0.02).astype(np.float32)
    exp_lp = fill_from_surround(lp, hole, sigma=sigma * 2, levels=7)
    gain = np.clip(exp_lp / np.maximum(lp, 1e-5), 1.0, 8.0)
    gain = 1 + (gain - 1) * mask
    return np.clip(_to_srgb(lin * gain[..., None]), 0, 1).astype(np.float32)


def denoise(img: np.ndarray, luma: float = 0.3, chroma: float = 0.8, luma_sigma: float = 3.0,
            chroma_px: float = 6.0) -> np.ndarray:
    """Edge-aware noise reduction for night shots: strong on colour noise (blotchy a*/b*), light on
    luminance so texture survives. Bilateral filtering in Lab, mixed back by `luma`/`chroma`."""
    lab = C.rgb_to_lab(img)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    Lf = cv2.bilateralFilter(L, 0, luma_sigma, 1.5)
    af = cv2.bilateralFilter(a, 0, 4.0, chroma_px)
    bf = cv2.bilateralFilter(b, 0, 4.0, chroma_px)
    out = np.stack([L + luma * (Lf - L), a + chroma * (af - a), b + chroma * (bf - b)], -1)
    return C.lab_to_rgb(out).astype(np.float32)


# ---- finishing -------------------------------------------------------------------------
def sharpen(img: np.ndarray, radius: float = 1.0, amount: float = 0.6, threshold: float = 0.01) -> np.ndarray:
    """Unsharp mask on luminosity only (no color fringes)."""
    L = C.luminance(img)
    d = L - C.gaussian(L, radius)
    d = np.where(np.abs(d) < threshold, 0, d)
    return C.replace_luminance(img, L + amount * d)


def grain(img: np.ndarray, amount: float = 0.015, size: float = 0.8, seed: int = 7) -> np.ndarray:
    """Monochrome film-like grain, strongest in midtones; unifies retouched and untouched texture."""
    rng = np.random.default_rng(seed)
    h, w = img.shape[:2]
    n = rng.standard_normal((h, w)).astype(np.float32)
    if size > 0:
        n = C.gaussian(n, size)
        n /= n.std() + 1e-6
    L = C.luminance(img)
    mid = 0.35 + 0.65 * (1 - np.abs(L - 0.5) * 2)
    return C.replace_luminance(img, L + amount * n * mid)


def fs_split(img: np.ndarray, radius: float) -> tuple[np.ndarray, np.ndarray]:
    """Frequency separation (16-bit 'Add/Invert/Scale 2' equivalent): img = low + high."""
    low = np.stack([C.gaussian(img[..., c], radius) for c in range(3)], -1)
    return low, img - low

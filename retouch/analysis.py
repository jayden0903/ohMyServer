"""Inspection tools: check layers, multi-scale tiles, face/skin stats, blemish candidates, metrics.

These are the evaluator's eyes. Check layers exaggerate exactly the defects a retoucher hunts
for (blotches, seams, banding), which makes them visible even on a downscaled view.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import cv2
import numpy as np

from . import color as C
from . import io as IO
from . import masks as M
from . import ops as O

SOLARIZE = [[0, 0], [64, 255], [128, 0], [192, 255], [255, 0]]
CONTRAST = [[0, 0], [90, 20], [128, 128], [166, 235], [255, 255]]
MIDPEAK = [[0, 0], [128, 255], [255, 0]]


# ---- check layers ----------------------------------------------------------------------
def check_layers(img: np.ndarray) -> dict[str, np.ndarray]:
    """Scott Valentine / Retouching Academy helper views, as RGB images."""
    L = C.luminance(img)
    gray = lambda x: np.repeat(np.clip(x, 0, 1)[..., None], 3, -1)
    hsv = C.rgb_to_hsv(img)
    hsv[..., 1] = np.clip(hsv[..., 1] * 3.0, 0, 1)
    return {
        "luminosity": gray(L),
        "contrast": gray(O.apply_curve(L, CONTRAST)),
        "solarize": gray(O.apply_curve(L, SOLARIZE)),
        "midpeak": gray(O.apply_curve(L, MIDPEAK)),
        "color_check": C.hsv_to_rgb(hsv),
    }


# ---- tiles -----------------------------------------------------------------------------
def tiles(img: np.ndarray, out_dir: str | Path, prefix: str = "t", grid: int = 3,
          overlap: float = 0.15, max_side: int = 1100) -> list[dict]:
    """Full view + grid x grid overlapping tiles (each saved <= max_side px)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    h, w = img.shape[:2]
    res = [{"path": str(IO.save_preview(img, out / f"{prefix}_full.jpg", 1600)), "box": [0, 0, 1, 1]}]
    th, tw = h / grid, w / grid
    for gy in range(grid):
        for gx in range(grid):
            x0 = max(0, int(gx * tw - overlap * tw)); x1 = min(w, int((gx + 1) * tw + overlap * tw))
            y0 = max(0, int(gy * th - overlap * th)); y1 = min(h, int((gy + 1) * th + overlap * th))
            p = IO.save_preview(img[y0:y1, x0:x1], out / f"{prefix}_{gy}{gx}.jpg", max_side)
            res.append({"path": str(p), "box": [x0 / w, y0 / h, x1 / w, y1 / h]})
    return res


def crop_view(img: np.ndarray, box: list[float], path: str | Path, max_side: int = 1200,
              upscale_to: int | None = None) -> Path:
    """Save a normalized crop; optionally upscale (nearest) to inspect at >100%."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = box
    c = img[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    if upscale_to and max(c.shape[:2]) < upscale_to:
        s = upscale_to / max(c.shape[:2])
        c = cv2.resize(c, (int(c.shape[1] * s), int(c.shape[0] * s)), interpolation=cv2.INTER_NEAREST)
    return IO.save_preview(c, path, max_side)


def side_by_side(a: np.ndarray, b: np.ndarray, path: str | Path, max_side: int = 2000) -> Path:
    if a.shape != b.shape:
        b = cv2.resize(b, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_AREA)
    gap = np.ones((a.shape[0], max(4, a.shape[1] // 100), 3), np.float32)
    return IO.save_preview(np.concatenate([a, gap, b], 1), path, max_side)


def grid_overlay(img: np.ndarray, kind: str = "thirds") -> np.ndarray:
    """Draw composition guides (thirds or phi) for crop decisions."""
    out = img.copy()
    h, w = out.shape[:2]
    fr = {"thirds": [1 / 3, 2 / 3], "phi": [0.382, 0.618]}[kind]
    t = max(1, w // 600)
    for f in fr:
        cv2.line(out, (int(f * w), 0), (int(f * w), h), (1, 0.2, 0.2), t, cv2.LINE_AA)
        cv2.line(out, (0, int(f * h)), (w, int(f * h)), (1, 0.2, 0.2), t, cv2.LINE_AA)
    return out


# ---- faces -----------------------------------------------------------------------------
def detect_faces(img: np.ndarray) -> list[dict]:
    from . import faces as F

    return F.detect(img)


def scale_params(face_width_px: int | None, img_width_px: int) -> dict:
    """Suggested band limits from face size (heuristic: pores ~ face_w/500, blotches ~ face_w/25)."""
    fw = face_width_px or img_width_px * 0.3
    return {"pore_px": round(fw / 500, 2), "micro_db": {"s_lo": round(max(1.0, fw / 300), 2),
                                                        "s_hi": round(max(6.0, fw / 35), 2)},
            "color_even": {"s_lo": round(max(1.5, fw / 200), 2), "s_hi": round(max(10.0, fw / 20), 2)},
            "blemish_r": [round(fw / 250 / img_width_px, 5), round(fw / 40 / img_width_px, 5)],
            "fs_radius": round(max(2.0, fw / 120), 2)}


# ---- skin & blemishes ------------------------------------------------------------------
def skin_stats(img: np.ndarray, mask: np.ndarray | None = None) -> dict:
    mask = M.skin(img) if mask is None else mask
    w = mask > 0.5
    if w.sum() < 50:
        return {"skin_pixels": int(w.sum())}
    lab = C.rgb_to_lab(img)
    L, a, b = lab[..., 0][w], lab[..., 1][w], lab[..., 2][w]
    hue = np.degrees(np.arctan2(b, a))
    hsv = C.rgb_to_hsv(img)
    rgb = img[w]
    return {
        "skin_pixels": int(w.sum()),
        "L_mean": round(float(L.mean()), 1),
        "a_mean": round(float(a.mean()), 1), "b_mean": round(float(b.mean()), 1),
        "b_over_a": round(float(b.mean() / max(a.mean(), 1e-3)), 2),
        "chroma_mean": round(float(np.hypot(a, b).mean()), 1),
        "lab_hue_mean": round(float(hue.mean()), 1), "lab_hue_std": round(float(hue.std()), 1),
        "hsv_hue_mean": round(float(hsv[..., 0][w].mean()), 1),
        "rgb_ratio_G/R": round(float(rgb[:, 1].mean() / max(rgb[:, 0].mean(), 1e-3)), 2),
        "rgb_ratio_B/R": round(float(rgb[:, 2].mean() / max(rgb[:, 0].mean(), 1e-3)), 2),
        "targets": "b*>=a*, a*/b* midtones ~15-20 (>30 oversaturated), Lab hue ~53-62, G/R .74-.81, B/R .60-.69",
    }


def blemish_candidates(img: np.ndarray, mask: np.ndarray, r_min: float, r_max: float,
                       thresh: float = 2.2, max_n: int = 300) -> list[dict]:
    """Small dark/red spots on skin, found as DoG blobs on L (dark) and a* (red).
    r_min/r_max are fractions of width. Returns spots ready for ops.heal (to be reviewed)."""
    h, w = img.shape[:2]
    lab = C.rgb_to_lab(img)
    L, a = lab[..., 0], lab[..., 1]
    found = []
    rmin_px, rmax_px = max(1.5, r_min * w), max(3.0, r_max * w)
    sigmas = np.geomspace(rmin_px / 1.414, rmax_px / 1.414, 6)
    hard = mask > 0.6
    for sgm in sigmas:
        dl = C.gaussian(L, sgm) - C.gaussian(L, sgm * 2.5)     # negative = darker than surround
        da = C.gaussian(a, sgm) - C.gaussian(a, sgm * 2.5)     # positive = redder
        noise_l = float(np.median(np.abs(dl[hard]))) * 1.4826 + 1e-3 if hard.any() else 1.0
        noise_a = float(np.median(np.abs(da[hard]))) * 1.4826 + 1e-3 if hard.any() else 1.0
        score = np.maximum(-dl / noise_l, 0.7 * da / noise_a) * hard
        # Reject parts of larger structures (nostrils, lash line, lip corners): a real blemish
        # fades at 3x its scale, a feature does not.
        big = C.gaussian(L, sgm * 3) - C.gaussian(L, sgm * 7.5)
        score *= (big > -0.6 * np.abs(dl)).astype(np.float32)
        k = int(sgm * 2) | 1
        peaks = (score == cv2.dilate(score, np.ones((k, k), np.float32))) & (score > thresh)
        for y, x in zip(*np.nonzero(peaks)):
            found.append((float(score[y, x]), x, y, sgm * 1.414))
    found.sort(reverse=True)
    spots: list[dict] = []
    for sc, x, y, r in found:
        if any(math.hypot(x - s["_x"], y - s["_y"]) < max(r, s["_r"]) * 1.2 for s in spots):
            continue
        spots.append({"x": round(x / w, 5), "y": round(y / h, 5), "r": round(r * 1.3 / w, 5),
                      "score": round(sc, 2), "_x": x, "_y": y, "_r": r})
        if len(spots) >= max_n:
            break
    for s in spots:
        del s["_x"], s["_y"], s["_r"]
    return spots


def blemish_search_mask(img: np.ndarray, prob: np.ndarray, face_w_px: int) -> np.ndarray:
    """Where automatic blemish search is allowed: face skin + neck, minus a generous zone around
    eyes/brows/lips and minus very dark holes (nostrils)."""
    from . import faces as F

    grow = max(3, int(face_w_px * 0.035))
    feats = M.choke((F.part_mask(prob, ["eyes", "brows", "lips", "teeth"], 0) > 0.3).astype(np.float32), -grow)
    m = F.part_mask(prob, ["face_skin", "neck"], 1.5) * (1 - M.feather(feats, grow / 3))
    L = C.luminance(img) * 100
    sel = m > 0.6
    if sel.any():
        med = float(np.median(L[sel])); mad = float(np.median(np.abs(L[sel] - med))) * 1.4826 + 1e-3
        holes = (C.gaussian(L, max(2, face_w_px / 120)) < med - 3.0 * mad).astype(np.float32)
        holes = M.choke(holes, -max(2, int(face_w_px * 0.015)))
        m *= 1 - M.feather(holes, max(2, face_w_px / 150))
    return m


def draw_spots(img: np.ndarray, spots: list[dict]) -> np.ndarray:
    out = img.copy()
    h, w = out.shape[:2]
    t = max(1, w // 800)
    for i, s in enumerate(spots):
        c = (int(s["x"] * w), int(s["y"] * h))
        cv2.circle(out, c, max(2, int(s["r"] * w)), (0, 1, 0.3), t, cv2.LINE_AA)
    return out


# ---- metrics ---------------------------------------------------------------------------
def metrics(orig: np.ndarray, edit: np.ndarray, skin_mask: np.ndarray | None = None,
            pore_px: float = 1.5, blotch: tuple[float, float] = (3.0, 20.0)) -> dict:
    """Deterministic gates. Orig and edit must be the same size (compare after geometry)."""
    if orig.shape != edit.shape:
        orig = cv2.resize(orig, (edit.shape[1], edit.shape[0]), interpolation=cv2.INTER_AREA)
    m = M.skin(orig) if skin_mask is None else skin_mask
    sel = m > 0.6
    Lo, Le = C.luminance(orig) * 100, C.luminance(edit) * 100
    hf = lambda L: L - C.gaussian(L, pore_px * 1.5)
    # Texture retention = projection of the edited fine detail onto the ORIGINAL fine detail.
    # Plain std ratios can be gamed: added grain restores std while the real pores are gone.
    ho, he = hf(Lo)[sel], hf(Le)[sel]
    tex_o = float((ho * ho).sum()) if sel.any() else 0.0
    tex_e = float((ho * he).sum()) if sel.any() else 0.0
    # pore-structure band (what reads as 'skin' at normal viewing), same projection measure
    pb = lambda L: C.gaussian(L, pore_px * 1.0) - C.gaussian(L, pore_px * 4.0)
    po, pe = pb(Lo)[sel], pb(Le)[sel]
    tex2 = float((po * pe).sum() / ((po * po).sum() + 1e-9)) if sel.any() else 0.0
    noise_added = float(np.sqrt(max(((he - ho * (tex_e / (tex_o + 1e-9))) ** 2).mean(), 0))) if sel.any() else 0.0
    bl = lambda L: O.band(L, *blotch, support=sel)
    bo, be = float(bl(Lo)[sel].std()) if sel.any() else 0, float(bl(Le)[sel].std()) if sel.any() else 0
    s = 800 / max(orig.shape[:2])
    small = lambda x: cv2.resize(x, (int(x.shape[1] * s), int(x.shape[0] * s)), interpolation=cv2.INTER_AREA)
    de = C.delta_e2000(C.rgb_to_lab(small(orig)), C.rgb_to_lab(small(edit)))
    clip_hi = float((edit.max(-1) >= 0.998).mean())
    clip_lo = float((edit.min(-1) <= 0.002).mean())
    res = {
        "texture_retention": round(min(tex_e / (tex_o + 1e-6), tex2), 3),
        "texture_fine": round(tex_e / (tex_o + 1e-6), 3), "texture_pore_band": round(tex2, 3),
        "texture_foreign_rms": round(noise_added, 3),
        "blotch_reduction": round(1 - be / (bo + 1e-6), 3),
        "deltaE_mean": round(float(de.mean()), 2), "deltaE_p95": round(float(np.percentile(de, 95)), 2),
        "clip_high_pct": round(clip_hi * 100, 3), "clip_low_pct": round(clip_lo * 100, 3),
        "skin_after": skin_stats(edit, m),
    }
    gates = []
    if res["texture_retention"] < 0.85:
        gates.append("FAIL texture_retention<0.85: skin texture is being erased (plastic skin)")
    if res["texture_retention"] > 1.25:
        gates.append("WARN texture_retention>1.25: over-sharpened / crunchy skin")
    if res["deltaE_p95"] > 12:
        gates.append("WARN deltaE_p95>12: large color departure from original; confirm intent")
    if clip_hi > 0.005 and clip_hi > float((orig.max(-1) >= 0.998).mean()) * 1.5:
        gates.append("WARN highlight clipping increased")
    sk = res["skin_after"]
    if "b_over_a" in sk and sk["b_over_a"] < 0.85:
        gates.append("WARN skin b*/a* < 0.85: skin reads red/magenta")
    if "chroma_mean" in sk and sk["chroma_mean"] > 32:
        gates.append("WARN skin chroma > 32: oversaturated ('Cheetos orange')")
    res["gates"] = gates or ["PASS"]
    return res


def save_json(obj, path: str | Path) -> None:
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False,
                                     default=lambda o: o.item() if hasattr(o, "item") else str(o)))

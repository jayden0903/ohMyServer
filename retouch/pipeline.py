"""Recipe runner: a recipe is the layer stack, so every edit stays reproducible and adjustable.

{
  "input": "photo.jpg", "output_dir": "out/job1",
  "steps": [
    {"op": "rotate", "degrees": 0.8},
    {"op": "crop_ratio", "ratio": "4:5", "center": [0.5, 0.42]},
    {"op": "heal", "name": "Cleanup", "spots": [{"x": .41, "y": .37, "r": .004}]},
    {"op": "micro_db", "name": "Micro D&B", "mask": {"skin": true, "exclude": [...]}, "s_lo": 2, "s_hi": 14},
    {"op": "curves", "channel": "lum", "points": [[0,8],[128,132],[255,250]], "mask": {...}, "opacity": .6}
  ],
  "export": {"jpeg_quality": 95, "tiff": true}
}
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from . import analysis as A
from . import geometry as G
from . import io as IO
from . import masks as M
from . import ops as O

GEOMETRY = {
    "rotate": lambda img, s: G.rotate(img, s["degrees"], s.get("crop", True)),
    "crop_box": lambda img, s: G.crop_box(img, s["box"]),
    "crop_ratio": lambda img, s: G.crop_ratio(img, s["ratio"], tuple(s.get("center", (0.5, 0.5))),
                                              s.get("scale", 1.0)),
    "keystone": lambda img, s: G.keystone(img, s.get("vertical", 0), s.get("horizontal", 0),
                                          s.get("aspect", 1.0)),
    "perspective": lambda img, s: G.perspective(img, s["src"], s.get("dst")),
}

# ops whose function takes the mask itself (the mask selects *where to measure/correct*)
MASK_AWARE = {"shadow_fix", "remove_lines", "micro_db", "color_even", "shine_reduce", "match_skin", "color_fix"}

ADJUST = {
    "curves": lambda img, s, m: O.curves(img, s["points"], s.get("channel", "rgb")),
    "levels": lambda img, s, m: O.levels(img, s.get("black", 0), s.get("white", 255), s.get("gamma", 1.0),
                                         s.get("out_black", 0), s.get("out_white", 255)),
    "exposure": lambda img, s, m: O.exposure(img, s.get("ev", 0.0)),
    "shadows_highlights": lambda img, s, m: O.shadows_highlights(img, s.get("shadows", 0), s.get("highlights", 0),
                                                                 s.get("sigma", 30)),
    "local_contrast": lambda img, s, m: O.local_contrast(img, s.get("amount", 0.2), s.get("sigma", 40),
                                                         support=m if s.get("mask") else None),
    "white_balance": lambda img, s, m: O.white_balance(img, s.get("temp", 0), s.get("tint", 0)),
    "neutralize": lambda img, s, m: O.neutralize(img, s["x"], s["y"], s.get("r", 0.01), s.get("strength", 1)),
    "saturation": lambda img, s, m: O.saturation(img, s.get("amount", 0)),
    "vibrance": lambda img, s, m: O.vibrance(img, s.get("amount", 0), s.get("protect_skin", True)),
    "hue_sat": lambda img, s, m: O.hue_sat(img, s["center"], s.get("width", 30), s.get("soft", 20),
                                           s.get("hue", 0), s.get("sat", 0), s.get("light", 0)),
    "mono": lambda img, s, m: O.mono(img, s.get("r", 0.4), s.get("g", 0.4), s.get("b", 0.2), s.get("tone"),
                                     s.get("tone_amount", 0.0)),
    "lab_shift": lambda img, s, m: O.lab_shift(img, s.get("da", 0), s.get("db", 0), s.get("dl", 0)),
    "match_skin": lambda img, s, m: O.match_skin(img, m, s.get("hue", 58), s.get("chroma"), s.get("strength", 0.5)),
    "color_fix": lambda img, s, m: O.color_fix(img, m, s.get("sample"), s.get("rgb"), s.get("mode", "color"),
                                               s.get("opacity", 0.3)),
    "color_balance": lambda img, s, m: O.color_balance(img, s.get("shadows", (0, 0, 0)), s.get("midtones", (0, 0, 0)),
                                                       s.get("highlights", (0, 0, 0))),
    "split_tone": lambda img, s, m: O.split_tone(img, s.get("shadow_hue", 200), s.get("shadow_sat", 0),
                                                 s.get("highlight_hue", 40), s.get("highlight_sat", 0),
                                                 s.get("balance", 0)),
    "gradient_map": lambda img, s, m: O.gradient_map(img, s["stops"], s.get("opacity_map", 0.15),
                                                     s.get("preserve_luminosity", True)),
    "micro_db": lambda img, s, m: O.micro_db(img, m, s.get("s_lo", 2), s.get("s_hi", 14), s.get("strength", 0.6),
                                             s.get("cap", 5)),
    "color_even": lambda img, s, m: O.color_even(img, m, s.get("s_lo", 3), s.get("s_hi", 25),
                                                 s.get("strength", 0.6), s.get("cap", 4)),
    "dodge_burn": lambda img, s, m: O.dodge_burn(img, s["strokes"]),
    "shine_reduce": lambda img, s, m: O.shine_reduce(img, m, s.get("threshold", 0.8), s.get("amount", 0.5),
                                                     s.get("sigma", 6)),
    "remove_lines": lambda img, s, m: O.remove_lines(img, m, s.get("width_px", 3.0), s.get("threshold", 2.5),
                                                     s.get("dark", True)),
    "heal": lambda img, s, m: O.heal(img, s["spots"], s.get("search", 3.0)),
    "clone": lambda img, s, m: _clone_all(img, s["strokes"]),
    "deghost": lambda img, s, m: O.deghost(img, s["cx"], s["cy"], s["r"], s.get("sectors", 12),
                                           tuple(s.get("ref", (1.06, 1.45))), s.get("feather", 0.1),
                                           fade_toward=s.get("fade_toward"), fade=s.get("fade", 0.0)),
    "shadow_fix": lambda img, s, m: O.shadow_fix(img, m, s.get("sigma", 6.0)),
    "denoise": lambda img, s, m: O.denoise(img, s.get("luma", 0.3), s.get("chroma", 0.8), s.get("luma_sigma", 3.0),
                                           s.get("chroma_px", 6.0)),
    "sharpen": lambda img, s, m: O.sharpen(img, s.get("radius", 1.0), s.get("amount", 0.6), s.get("threshold", 0.01)),
    "grain": lambda img, s, m: O.grain(img, s.get("amount", 0.015), s.get("size", 0.8), s.get("seed", 7)),
}


def _clone_all(img, strokes):
    for st in strokes:
        img = O.clone(img, st["dst"], st["src"], st["r"], st.get("feather", 0.5))
    return img


def _delta_view(before: np.ndarray, after: np.ndarray, gain: float = 6.0) -> np.ndarray:
    return np.clip(0.5 + gain * (after - before), 0, 1)


def run(recipe: dict | str | Path, verbose: bool = True) -> dict:
    if not isinstance(recipe, dict):
        recipe = json.loads(Path(recipe).read_text())
    out = Path(recipe["output_dir"])
    (out / "layers").mkdir(parents=True, exist_ok=True)
    img, meta = IO.load(recipe["input"])
    original = img
    base = img
    log = []
    ctx: dict = {"prob": None}
    t0 = time.time()
    for i, step in enumerate(recipe["steps"]):
        if step.get("enabled") is False:
            continue
        op = step["op"]
        name = step.get("name", op)
        t = time.time()
        if op in GEOMETRY:
            # geometry applies to the 'original' reference too, so a crop late in the stack (a final
            # composition crop after the masks were placed) still compares like with like
            same = base is img
            img = GEOMETRY[op](img, step)
            base = img if same else GEOMETRY[op](base, step)
            ctx["prob"] = None
        elif op in ADJUST:
            mask = M.build(img, step.get("mask"), ctx)
            if op in MASK_AWARE:
                m_in = mask if mask is not None else np.ones(img.shape[:2], np.float32)
                res = ADJUST[op](img, step, m_in)
                blend = None
            else:
                res = ADJUST[op](img, step, mask)
                blend = mask
            opacity = float(step.get("opacity", 1.0))
            if blend is None:
                new = img + opacity * (res - img)
            else:
                new = img + opacity * blend[..., None] * (res - img)
            new = np.clip(new, 0, 1).astype(np.float32)
            tag = f"{i:02d}_{name.replace(' ', '_').replace('/', '-')}"
            IO.save_preview(_delta_view(img, new), out / "layers" / f"{tag}_delta.jpg", 1400)
            if mask is not None:
                IO.save_preview(np.repeat(mask[..., None], 3, -1), out / "layers" / f"{tag}_mask.jpg", 1000)
            img = new
        else:
            raise ValueError(f"unknown op: {op}")
        log.append({"step": i, "op": op, "name": name, "seconds": round(time.time() - t, 2),
                    "size": [img.shape[1], img.shape[0]]})
        if verbose:
            print(f"[{i:02d}] {name:<24} {time.time() - t:6.2f}s  {img.shape[1]}x{img.shape[0]}")

    exp = recipe.get("export", {})
    final = img
    if exp.get("max_side"):
        import cv2
        h, w = final.shape[:2]
        s = exp["max_side"] / max(h, w)
        if s < 1:
            final = cv2.resize(final, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
    IO.save(final, out / "final.jpg", meta, exp.get("jpeg_quality", 95))
    if exp.get("tiff"):
        IO.save(final, out / "final_16bit.tif", meta)
    A.side_by_side(base, img, out / "before_after.jpg")
    IO.save_preview(base, out / "base.jpg", 1600)
    IO.save_preview(base, out / "before_web.jpg", 2400, quality=90)   # for the before/after slider
    IO.save_preview(img, out / "final_preview.jpg", 1600)
    skin_m = None
    if ctx.get("prob") is not None and ctx["prob"].shape[1:] == base.shape[:2]:
        from . import faces as F
        skin_m = F.part_mask(ctx["prob"], ["face_skin", "neck"], 1.5) * (
            1 - F.part_mask(ctx["prob"], ["eyes", "brows", "lips", "teeth"], 3))
    met = A.metrics(base, img, skin_mask=skin_m, pore_px=recipe.get("pore_px", 1.5),
                    blotch=tuple(recipe.get("blotch_band", (3.0, 20.0))))
    summary = {"input_size": list(original.shape[1::-1]), "output_size": list(final.shape[1::-1]),
               "seconds": round(time.time() - t0, 1), "steps": log, "metrics": met}
    A.save_json(summary, out / "summary.json")
    (out / "recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False))
    return summary

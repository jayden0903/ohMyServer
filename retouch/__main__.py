"""CLI.

  python -m retouch analyze  IMG OUT_DIR            # faces, tilt, skin stats, check layers, tiles, blemish candidates
  python -m retouch run      RECIPE.json            # apply a recipe (layer stack) and export
  python -m retouch inspect  IMG OUT.jpg x0 y0 x1 y1 [--check solarize|contrast|luminosity|midpeak|color_check]
  python -m retouch compare  BEFORE AFTER OUT_DIR   # metrics + side by side + check-layer tiles
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from . import analysis as A
from . import geometry as G
from . import io as IO
from . import masks as M
from . import pipeline as P


def cmd_analyze(a):
    img, meta = IO.load(a.image)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    h, w = img.shape[:2]
    faces = A.detect_faces(img)
    fw = faces[0]["width_px"] if faces else None
    sp = A.scale_params(fw, w)
    from . import faces as F
    if faces:
        prob = F.parse(img, faces)
        skin = F.part_mask(prob, ["face_skin", "neck"], 1.5) * (1 - F.part_mask(prob, ["eyes", "brows", "lips"], 2))
        IO.save_preview(F.overlay(img, prob), out / "face_parsing.jpg", 1600)
    else:
        skin = M.skin(img)
    report = {"size": [w, h], "bit_depth": meta["bit_depth"], "icc": bool(meta.get("icc_profile")),
              "faces": faces, "tilt": G.detect_tilt(img), "scale_params": sp,
              "skin": A.skin_stats(img, skin)}
    search = A.blemish_search_mask(img, prob, fw) if faces else skin
    spots = A.blemish_candidates(img, search, *sp["blemish_r"], thresh=3.5, max_n=150)
    report["blemish_candidates"] = len(spots)
    A.save_json(spots, out / "blemish_candidates.json")
    IO.save_preview(A.draw_spots(img, spots), out / "blemish_overlay.jpg", 2000)
    IO.save_preview(np.repeat(skin[..., None], 3, -1), out / "skin_mask.jpg", 1200)
    IO.save_preview(A.grid_overlay(img, "thirds"), out / "grid_thirds.jpg", 1400)
    for k, v in A.check_layers(img).items():
        IO.save_preview(v, out / f"check_{k}.jpg", 1600)
    A.tiles(img, out / "tiles", "orig", grid=a.grid)
    A.save_json(report, out / "analysis.json")
    print((out / "analysis.json").read_text())


def cmd_inspect(a):
    img, _ = IO.load(a.image)
    if a.check:
        img = A.check_layers(img)[a.check]
    A.crop_view(img, [a.x0, a.y0, a.x1, a.y1], a.out, upscale_to=a.upscale)
    print(a.out)


def cmd_compare(a):
    before, _ = IO.load(a.before)
    after, _ = IO.load(a.after)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    met = A.metrics(before, after)
    A.side_by_side(before, after, out / "side_by_side.jpg")
    for k in ("solarize", "luminosity"):
        A.side_by_side(A.check_layers(before)[k], A.check_layers(after)[k], out / f"check_{k}_side.jpg")
    A.tiles(after, out / "tiles", "edit", grid=a.grid)
    A.save_json(met, out / "metrics.json")
    print((out / "metrics.json").read_text())


def main():
    p = argparse.ArgumentParser(prog="retouch")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("analyze"); s.add_argument("image"); s.add_argument("out"); s.add_argument("--grid", type=int, default=3)
    s.set_defaults(fn=cmd_analyze)
    s = sub.add_parser("run"); s.add_argument("recipe"); s.set_defaults(fn=lambda a: P.run(a.recipe))
    s = sub.add_parser("inspect"); s.add_argument("image"); s.add_argument("out")
    for k in ("x0", "y0", "x1", "y1"):
        s.add_argument(k, type=float)
    s.add_argument("--check"); s.add_argument("--upscale", type=int, default=None); s.set_defaults(fn=cmd_inspect)
    s = sub.add_parser("compare"); s.add_argument("before"); s.add_argument("after"); s.add_argument("out")
    s.add_argument("--grid", type=int, default=3); s.set_defaults(fn=cmd_compare)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

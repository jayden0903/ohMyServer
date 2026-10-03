"""Retouch engine as an MCP server (streamable HTTP).

The artifact page (Claude `sample` for judgement + `mcp` for this server) drives the loop:
  new_job -> put_chunk ... -> analyze -> render(recipe) -> crop_view -> export

Run:  RETOUCH_TOKEN=<secret> python -m retouch.mcp_server --port 8765
The endpoint is  http://host:port/<secret>/mcp  (the secret path is the auth).
"""
from __future__ import annotations

import argparse
import base64
import io as _io
import json
import os
import shutil
import time
import uuid
from pathlib import Path

import numpy as np
from mcp.server.mcpserver import Image, MCPServer
from PIL import Image as PILImage

from . import analysis as A
from . import geometry as G
from . import io as IO
from . import pipeline as P

JOBS = Path(os.environ.get("RETOUCH_JOBS", Path.home() / ".cache/retouch/jobs"))
JOBS.mkdir(parents=True, exist_ok=True)
MAX_BYTES = 60 * 1024 * 1024
JOB_TTL = 6 * 3600

mcp = MCPServer(
    "Retouch Engine",
    instructions="Non-generative photo retouching engine. Upload a photo in base64 chunks, analyze it, "
                 "then render JSON recipes (curves, masks, dodge & burn, heal, grading, crop/rotate).",
)


def _job(job_id: str) -> Path:
    if not job_id or any(c not in "0123456789abcdef" for c in job_id):
        raise ValueError("bad job_id")
    d = JOBS / job_id
    if not d.exists():
        raise ValueError("unknown job_id (expired?)")
    return d


def _jpeg(img: np.ndarray, max_side: int, quality: int = 85) -> bytes:
    h, w = img.shape[:2]
    s = min(1.0, max_side / max(h, w))
    if s < 1:
        import cv2
        img = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
    buf = _io.BytesIO()
    PILImage.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(buf, "JPEG", quality=quality)
    return buf.getvalue()


def describe(img: np.ndarray, n: int = 4) -> dict:
    """Text stand-in for eyes: an n x n grid of tone/colour/texture per cell, plus global facts.
    Lab: L 0..100, a+ red / a- green, b+ yellow / b- blue. 'hue' = Lab hue angle in degrees."""
    import cv2
    from . import color as C
    h, w = img.shape[:2]
    s = 800 / max(h, w)
    small = cv2.resize(img, (max(1, int(w * s)), max(1, int(h * s))), interpolation=cv2.INTER_AREA)
    lab = C.rgb_to_lab(small)
    hsv = C.rgb_to_hsv(small)
    gray = (C.luminance(small) * 255).astype(np.uint8)
    edges = cv2.Canny(gray, 60, 150) > 0
    sh, sw = gray.shape
    rows = []
    for gy in range(n):
        row = []
        for gx in range(n):
            ys, xs = slice(gy * sh // n, (gy + 1) * sh // n), slice(gx * sw // n, (gx + 1) * sw // n)
            L, a, b = (lab[ys, xs, i] for i in range(3))
            hue = (np.degrees(np.arctan2(b.mean(), a.mean())) + 360) % 360
            row.append({"L": round(float(L.mean())), "Lp5_p95": [round(float(np.percentile(L, 5))), round(float(np.percentile(L, 95)))],
                        "a": round(float(a.mean()), 1), "b": round(float(b.mean()), 1), "hue": round(float(hue)),
                        "sat": round(float(hsv[ys, xs, 1].mean()), 2), "edges": round(float(edges[ys, xs].mean()), 3)})
        rows.append(row)
    try:
        from . import masks as M
        sky = float(M.sky(small, refine=0).mean())
    except Exception:
        sky = None
    hist = np.histogram(lab[..., 0], bins=10, range=(0, 100))[0]
    return {"grid": rows, "grid_note": f"{n}x{n}, row 0 = top", "sky_fraction": None if sky is None else round(sky, 3),
            "L_histogram_10bins_pct": [round(float(v) * 100 / hist.sum(), 1) for v in hist]}


def _cleanup() -> None:
    now = time.time()
    for d in JOBS.iterdir():
        if d.is_dir() and now - d.stat().st_mtime > JOB_TTL:
            shutil.rmtree(d, ignore_errors=True)


@mcp.tool()
def new_job(filename: str = "photo.jpg") -> dict:
    """Start a job. Returns job_id. Then send the photo with put_chunk."""
    _cleanup()
    jid = uuid.uuid4().hex
    d = JOBS / jid
    d.mkdir()
    (d / "meta.json").write_text(json.dumps({"filename": filename, "created": time.time()}))
    return {"job_id": jid, "max_chunk_b64_chars": 2_500_000}


@mcp.tool()
def put_chunk(job_id: str, index: int, total: int, data_b64: str) -> dict:
    """Append one base64 chunk of the original photo (JPEG/PNG/WebP/TIFF). Send index 0..total-1 in order."""
    d = _job(job_id)
    part = d / "upload.part"
    if index == 0 and part.exists():
        part.unlink()
    with open(part, "ab") as f:
        f.write(base64.b64decode(data_b64))
    if part.stat().st_size > MAX_BYTES:
        part.unlink()
        raise ValueError("file too large (60 MB max)")
    if index == total - 1:
        raw = part.read_bytes()
        part.unlink()
        img = PILImage.open(_io.BytesIO(raw))
        ext = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "TIFF": ".tif"}.get(img.format or "", ".jpg")
        (d / f"orig{ext}").write_bytes(raw)
        return {"done": True, "format": img.format, "size": list(img.size)}
    return {"done": False, "received": index + 1}


def _orig(d: Path) -> Path:
    for p in d.glob("orig.*"):
        return p
    raise ValueError("no photo uploaded yet")


@mcp.tool()
def analyze(job_id: str) -> list:
    """Analyze the photo: faces/landmarks, horizon & tilt, skin stats, scale hints. Returns JSON + a preview."""
    d = _job(job_id)
    img, meta = IO.load(_orig(d))
    h, w = img.shape[:2]
    faces = A.detect_faces(img)
    fw = faces[0]["width_px"] if faces else None
    rep = {"size": [w, h], "bit_depth": meta["bit_depth"], "faces": faces,
           "horizon": G.detect_horizon(img), "lines_tilt": G.detect_tilt(img),
           "scale_params": A.scale_params(fw, w)}
    if faces:
        from . import faces as F
        prob = F.parse(img, faces)
        skin = F.part_mask(prob, ["face_skin", "neck"], 1.5)
        rep["skin"] = A.skin_stats(img, skin)
    lab = __import__("retouch.color", fromlist=["x"]).rgb_to_lab(img)
    L = lab[..., 0]
    rep["tones"] = {k: [round(float(lab[..., 1][s].mean()), 1), round(float(lab[..., 2][s].mean()), 1)]
                    for k, s in (("shadows_ab", L < 30), ("mids_ab", (L >= 30) & (L < 65)), ("highs_ab", L >= 65))
                    if s.any()}
    rep["describe"] = describe(img)
    rep["clip_pct"] = {"high": round(float((img.max(-1) > 0.995).mean() * 100), 2),
                       "low": round(float((img.min(-1) < 0.005).mean() * 100), 2)}
    (d / "analysis.json").write_text(json.dumps(rep, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    return [json.dumps(rep, default=lambda o: o.item() if hasattr(o, "item") else str(o)),
            Image(data=_jpeg(img, 1400), format="jpeg")]


@mcp.tool()
def render(job_id: str, recipe_json: str, preview_px: int = 1400) -> list:
    """Run a recipe {"steps":[...]} on the photo (same format as retouch/pipeline.py). Returns metrics JSON and
    a preview of the result. The full-resolution result is kept for export."""
    d = _job(job_id)
    recipe = json.loads(recipe_json)
    steps = recipe["steps"] if isinstance(recipe, dict) else recipe
    out = d / "render"
    if out.exists():
        shutil.rmtree(out)
    r = {"input": str(_orig(d)), "output_dir": str(out), "steps": steps,
         "export": {"jpeg_quality": 95}}
    summ = P.run(r, verbose=False)
    (d / "recipe.json").write_text(json.dumps(steps, ensure_ascii=False))
    img, _ = IO.load(out / "final.jpg")
    return [json.dumps({"metrics": summ["metrics"], "output_size": summ["output_size"],
                        "seconds": summ["seconds"], "describe": describe(img)}, ensure_ascii=False),
            Image(data=_jpeg(img, preview_px), format="jpeg")]


@mcp.tool()
def crop_view(job_id: str, x0: float, y0: float, x1: float, y1: float, source: str = "render",
              check: str = "") -> Image:
    """Zoomed crop (normalized box) of the original ('orig') or the latest result ('render'), optionally as a
    check layer: solarize | luminosity | contrast | midpeak | color_check."""
    d = _job(job_id)
    p = (d / "render" / "final.jpg") if source == "render" else _orig(d)
    img, _ = IO.load(p)
    if check:
        img = A.check_layers(img)[check]
    h, w = img.shape[:2]
    c = img[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    return Image(data=_jpeg(c, 1200), format="jpeg")


@mcp.tool()
def export(job_id: str, index: int = 0, chunk_b64_chars: int = 2_000_000) -> dict:
    """Download the full-resolution result as base64 chunks: call with index 0,1,... until done is true."""
    d = _job(job_id)
    data = base64.b64encode((d / "render" / "final.jpg").read_bytes()).decode()
    part = data[index * chunk_b64_chars:(index + 1) * chunk_b64_chars]
    total = (len(data) + chunk_b64_chars - 1) // chunk_b64_chars
    return {"index": index, "total": total, "done": index >= total - 1, "data_b64": part}


def main() -> None:
    import uvicorn
    from mcp.server.transport_security import TransportSecuritySettings
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Mount, Route

    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    token = os.environ.get("RETOUCH_TOKEN")
    if not token or len(token) < 24:
        raise SystemExit("set RETOUCH_TOKEN (24+ chars); it becomes the secret URL path")
    inner = mcp.streamable_http_app(streamable_http_path="/mcp", stateless_http=True, json_response=True,
                                    max_request_body_size=4 * 1024 * 1024,
                                    transport_security=TransportSecuritySettings(
                                        enable_dns_rebinding_protection=False))
    app = Starlette(routes=[Route("/health", lambda r: PlainTextResponse("ok")),
                            Mount(f"/{token}", app=inner)],
                    lifespan=lambda app: inner.router.lifespan_context(inner))
    uvicorn.run(app, host=a.host, port=a.port, log_level="info")


if __name__ == "__main__":
    main()

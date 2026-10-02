"""Image loading and saving. Internal format: float32 RGB in [0, 1], sRGB-encoded."""
from __future__ import annotations

import io as _io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps


def load(path: str | Path) -> tuple[np.ndarray, dict]:
    """Load an image, apply EXIF orientation, return (float32 RGB, meta)."""
    path = Path(path)
    meta: dict = {"source": str(path)}
    raw = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    with Image.open(path) as pil:
        meta["icc_profile"] = pil.info.get("icc_profile")
        meta["exif"] = pil.info.get("exif")
        oriented = ImageOps.exif_transpose(pil)
        transposed = oriented.size != pil.size or pil.getexif().get(0x0112, 1) != 1
        if raw is not None and raw.dtype == np.uint16 and not transposed:
            img = cv2.cvtColor(raw[..., :3], cv2.COLOR_BGR2RGB).astype(np.float32) / 65535.0
            meta["bit_depth"] = 16
        else:
            img = np.asarray(oriented.convert("RGB"), dtype=np.float32) / 255.0
            meta["bit_depth"] = 8
    meta["size"] = (img.shape[1], img.shape[0])
    return np.ascontiguousarray(img), meta


def save(img: np.ndarray, path: str | Path, meta: dict | None = None, quality: int = 95) -> Path:
    """Save float RGB. .jpg/.jpeg/.webp -> 8-bit, .png/.tif -> 16-bit."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = np.clip(img, 0.0, 1.0)
    ext = path.suffix.lower()
    icc = (meta or {}).get("icc_profile")
    if ext in (".png", ".tif", ".tiff"):
        arr = (img * 65535.0 + 0.5).astype(np.uint16)
        cv2.imwrite(str(path), cv2.cvtColor(arr, cv2.COLOR_RGB2BGR))
        return path
    arr = (img * 255.0 + 0.5).astype(np.uint8)
    pil = Image.fromarray(arr, "RGB")
    kwargs = {"quality": quality}
    if ext in (".jpg", ".jpeg"):
        kwargs["subsampling"] = 0
    if icc:
        kwargs["icc_profile"] = icc
    pil.save(path, **kwargs)
    return path


def save_preview(img: np.ndarray, path: str | Path, max_side: int = 1600, quality: int = 90) -> Path:
    """Downscaled 8-bit preview for viewing."""
    h, w = img.shape[:2]
    s = min(1.0, max_side / max(h, w))
    if s < 1.0:
        img = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
    return save(img, path, quality=quality)


def to_gray_u8(x: np.ndarray) -> np.ndarray:
    return (np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8)


def encode_jpeg(img: np.ndarray, quality: int = 92) -> bytes:
    buf = _io.BytesIO()
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB").save(buf, "JPEG", quality=quality)
    return buf.getvalue()

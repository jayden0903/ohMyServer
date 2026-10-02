"""Face detection (YuNet, 5 landmarks) and face parsing (SegFormer, CelebAMask-HQ 19 classes).

Parsing gives the per-part masks a retoucher would otherwise draw by hand: skin, nose, eyes,
brows, lips, inner mouth (teeth), hair, ears, neck, clothes.
"""
from __future__ import annotations

import os
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).parent
YUNET = HERE / "models" / "face_detection_yunet_2023mar.onnx"
PARSER = Path(os.environ.get("RETOUCH_PARSER", Path.home() / ".cache/retouch/face_parsing_q.onnx"))
PARSER_URL = "https://huggingface.co/jonathandinu/face-parsing/resolve/main/onnx/model_quantized.onnx"

LABELS = ["background", "skin", "nose", "eye_g", "l_eye", "r_eye", "l_brow", "r_brow", "l_ear", "r_ear",
          "mouth", "u_lip", "l_lip", "hair", "hat", "ear_r", "neck_l", "neck", "cloth"]
GROUPS = {
    "face_skin": ["skin", "nose"],
    "skin_all": ["skin", "nose", "neck", "l_ear", "r_ear"],
    "eyes": ["l_eye", "r_eye"], "brows": ["l_brow", "r_brow"], "lips": ["u_lip", "l_lip"],
    "teeth": ["mouth"], "ears": ["l_ear", "r_ear"],
}

_sess = None


def detect(img: np.ndarray, score: float = 0.7) -> list[dict]:
    """Faces with landmarks, normalized coords. Landmarks: right eye, left eye, nose, mouth R, mouth L
    (subject's right/left)."""
    h, w = img.shape[:2]
    s = min(1.0, 1600 / max(h, w))
    small = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA) if s < 1 else img
    bgr = cv2.cvtColor((np.clip(small, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    sh, sw = bgr.shape[:2]
    faces = None
    for thr in (score, 0.5, 0.35):   # partial or turned faces score lower; retry before giving up
        det = cv2.FaceDetectorYN.create(str(YUNET), "", (sw, sh), thr, 0.3, 50)
        _, faces = det.detect(bgr)
        if faces is not None and len(faces):
            break
    out = []
    for f in faces if faces is not None else []:
        x, y, fw, fh = f[:4]
        lm = f[4:14].reshape(5, 2)
        out.append({"box": [x / sw, y / sh, (x + fw) / sw, (y + fh) / sh], "score": round(float(f[14]), 3),
                    "width_px": int(fw / s),
                    "landmarks": {k: [round(float(px / sw), 4), round(float(py / sh), 4)]
                                  for k, (px, py) in zip(["eye_r", "eye_l", "nose", "mouth_r", "mouth_l"], lm)},
                    "roll_deg": round(float(np.degrees(np.arctan2(lm[1, 1] - lm[0, 1], lm[1, 0] - lm[0, 0]))), 2)})
    out.sort(key=lambda d: -(d["box"][2] - d["box"][0]))
    return out


def _session():
    global _sess
    if _sess is None:
        import onnxruntime as ort

        if not PARSER.exists():
            import urllib.request

            PARSER.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(PARSER_URL, PARSER)
        so = ort.SessionOptions()
        so.intra_op_num_threads = os.cpu_count() or 4
        _sess = ort.InferenceSession(str(PARSER), so, providers=["CPUExecutionProvider"])
    return _sess


def parse(img: np.ndarray, faces: list[dict] | None = None, margin: float = 0.9) -> np.ndarray:
    """Per-class probabilities for the whole image, shape (19, H, W) float32.
    Each detected face is parsed in its own crop (box expanded by `margin` on every side)."""
    h, w = img.shape[:2]
    faces = detect(img) if faces is None else faces
    prob = np.zeros((len(LABELS), h, w), np.float32)
    prob[0] = 1.0
    sess = _session()
    mean = np.array([0.485, 0.456, 0.406], np.float32)
    std = np.array([0.229, 0.224, 0.225], np.float32)
    for f in faces:
        x0, y0, x1, y1 = f["box"]
        bw, bh = (x1 - x0) * w, (y1 - y0) * h
        side = max(bw, bh) * (1 + 2 * margin)
        cx, cy = (x0 + x1) / 2 * w, (y0 + y1) / 2 * h - 0.1 * bh
        X0, Y0 = int(max(0, cx - side / 2)), int(max(0, cy - side / 2))
        X1, Y1 = int(min(w, cx + side / 2)), int(min(h, cy + side / 2))
        crop = img[Y0:Y1, X0:X1]
        inp = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_AREA)
        inp = ((inp - mean) / std).transpose(2, 0, 1)[None].astype(np.float32)
        logits = sess.run(None, {"pixel_values": inp})[0][0]
        ch, cw = crop.shape[:2]
        up = np.stack([cv2.resize(l, (cw, ch), interpolation=cv2.INTER_CUBIC) for l in logits])
        up = np.exp(up - up.max(0, keepdims=True))
        up /= up.sum(0, keepdims=True)
        # feather the crop border so faces near each other / the crop edge blend smoothly
        fy = np.minimum(np.arange(ch), np.arange(ch)[::-1]) / max(1, ch * 0.08)
        fx = np.minimum(np.arange(cw), np.arange(cw)[::-1]) / max(1, cw * 0.08)
        wgt = np.clip(np.minimum.outer(fy, fx), 0, 1).astype(np.float32)
        region = prob[:, Y0:Y1, X0:X1]
        prob[:, Y0:Y1, X0:X1] = region * (1 - wgt) + up * wgt
    return prob


def part_mask(prob: np.ndarray, names: list[str] | str, soften: float = 1.0) -> np.ndarray:
    names = [names] if isinstance(names, str) else names
    idx = []
    for n in names:
        for m in GROUPS.get(n, [n]):
            idx.append(LABELS.index(m))
    m = prob[idx].sum(0)
    if soften > 0:
        k = int(soften * 6) | 1
        m = cv2.GaussianBlur(m, (k, k), soften)
    return np.clip(m, 0, 1)


def overlay(img: np.ndarray, prob: np.ndarray) -> np.ndarray:
    palette = np.array([[0, 0, 0], [255, 200, 150], [255, 120, 60], [120, 120, 120], [0, 120, 255], [0, 200, 255],
                        [120, 60, 0], [160, 90, 0], [200, 0, 200], [230, 0, 230], [255, 0, 0], [255, 60, 120],
                        [200, 0, 80], [80, 40, 10], [60, 60, 60], [255, 255, 0], [0, 160, 0], [0, 255, 120],
                        [120, 0, 255]], np.float32) / 255
    lab = prob.argmax(0)
    col = palette[lab]
    return np.where((lab > 0)[..., None], img * 0.45 + col * 0.55, img * 0.6)

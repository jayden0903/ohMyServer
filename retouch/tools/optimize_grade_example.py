import sys, json, itertools, math, copy
sys.path.insert(0, '/home/user/ohMyServer')
import numpy as np, cv2
from retouch import io as IO, color as C, pipeline as P, masks as M

D = sys.argv[1]
base = json.load(open(f'{D}/K/cinema2.json'))
img, _ = IO.load(base['input'])
h, w = img.shape[:2]; s = 900 / w
small = cv2.resize(img, (900, int(h * s)), interpolation=cv2.INTER_AREA)

def build(p):
    r = copy.deepcopy(base)
    for st in r['steps']:
        n = st['name']
        if n.startswith('Hard teal'):
            st.update(shadow_hue=p['sh_hue'], shadow_sat=p['sh_sat'], highlight_hue=48, highlight_sat=p['hi_sat'], balance=0.15)
        if n.startswith('Strip natural'):
            st['amount'] = -p['strip']
        if n.startswith('Water: electric'):
            st['sat'] = p['water']
        if n.startswith('Mist: cold'):
            st.update(da=-2, db=-6)
    # neutralize residual green in foliage (shift toward olive, less saturation)
    r['steps'].insert(3, {"op": "hue_sat", "name": "Foliage: kill green", "center": 120, "width": 80, "soft": 30,
                          "hue": -18, "sat": -p['green']})
    return r

def run_small(r):
    x = small.copy(); ctx = {"prob": None}
    for st in r['steps']:
        op = st['op']
        if op in P.GEOMETRY: x = P.GEOMETRY[op](x, st); continue
        if op == 'grain': continue
        m = M.build(x, st.get('mask'), ctx)
        if op in P.MASK_AWARE:
            res = P.ADJUST[op](x, st, m if m is not None else np.ones(x.shape[:2], np.float32)); x = res
        else:
            res = P.ADJUST[op](x, st, m)
            x = x + (res - x) * (m[..., None] if m is not None else 1) * st.get('opacity', 1.0)
        x = np.clip(x, 0, 1).astype(np.float32)
    return x

def stats(x):
    lab = C.rgb_to_lab(x); L = lab[..., 0]; o = {}
    for k, sel in [('sh', L < 30), ('mid', (L >= 30) & (L < 65)), ('hi', L >= 65)]:
        a = float(lab[..., 1][sel].mean()); b = float(lab[..., 2][sel].mean())
        o[k] = (a, b, math.hypot(a, b), (math.degrees(math.atan2(b, a)) + 360) % 360)
    o['Lmean'] = float(L.mean())
    return o

def loss(o):
    a, b, c, hue = o['sh']
    l = 0
    l += abs(c - 5.0) * 1.0                              # shadows: gentle teal, not saturated
    l += min(abs(hue - 222), 360 - abs(hue - 222)) / 6   # teal-blue, not green (green ~ 130-180)
    l += max(0, -1.0 - o['mid'][0]) * 3                  # midtones must not go green (a* < -1)
    l += max(0, o['mid'][2] - 4.0) * 1.5                 # midtones near neutral
    a, b, c, hue = o['hi']
    l += abs(c - 9.0) * 0.6 + min(abs(hue - 65), 360 - abs(hue - 65)) / 10   # warm amber highlights
    return l

grid = dict(sh_hue=[210, 225, 240], sh_sat=[0.2, 0.3, 0.4], hi_sat=[0.35, 0.5, 0.65], strip=[0.45, 0.6],
            green=[0.3, 0.5], water=[0.15, 0.3])
best = []
for vals in itertools.product(*grid.values()):
    p = dict(zip(grid.keys(), vals))
    o = stats(run_small(build(p)))
    best.append((loss(o), p, o))
best.sort(key=lambda t: t[0])
for l, p, o in best[:5]:
    print(round(l, 2), p, {k: tuple(round(v, 1) for v in o[k]) for k in ('sh', 'mid', 'hi')})
r = build(best[0][1]); r['output_dir'] = f'{D}/K/cinema3'
json.dump(r, open(f'{D}/K/cinema3.json', 'w'), indent=1)

import math

def rotp(p, a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return (c * p[0] - s * p[1], s * p[0] + c * p[1])

def fmt(p):
    return f'{p[0]:.1f},{p[1]:.1f}'

def _cr(p0, p1, p2, p3, t):
    t2 = t * t; t3 = t2 * t
    return tuple(0.5 * ((2 * p1[i]) + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2
                        + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3) for i in (0, 1))

def sample(pts, per=24, closed=False):
    n = len(pts); out = []
    segs = n if closed else n - 1
    for i in range(segs):
        p0 = pts[(i - 1) % n] if closed else pts[max(i - 1, 0)]
        p1 = pts[i % n]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed else pts[min(i + 2, n - 1)]
        for k in range(per):
            out.append(_cr(p0, p1, p2, p3, k / per))
    if not closed:
        out.append(pts[-1])
    return out

def bez(pts, closed=False, move=True):
    n = len(pts); d = ('M' + fmt(pts[0])) if move else ''
    segs = n if closed else n - 1
    for i in range(segs):
        p0 = pts[(i - 1) % n] if closed else pts[max(i - 1, 0)]
        p1 = pts[i % n]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed else pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{fmt(c1)} {fmt(c2)} {fmt(p2)}'
    if closed:
        d += 'Z'
    return d

def ss(e0, e1, x):
    if e1 == e0:
        return 1.0 if x >= e1 else 0.0
    t = min(max((x - e0) / (e1 - e0), 0), 1)
    return t * t * (3 - 2 * t)

def taperf(w, a=0.25, b=0.25):
    def f(t):
        v = w
        if a > 0: v *= ss(0, a, t)
        if b > 0: v *= 1 - ss(1 - b, 1, t)
        return v
    return f

def lockf(w0, bulge=0.2, power=0.9):
    return lambda t: w0 * (1 - t) ** power * (1 + bulge * math.sin(math.pi * t))

def ribbon_pts(pts, wf, per=24, shift=0.0):
    s = sample(pts, per)
    L = [0.0]
    for i in range(1, len(s)):
        L.append(L[-1] + math.hypot(s[i][0] - s[i - 1][0], s[i][1] - s[i - 1][1]))
    tot = L[-1] or 1
    lf = []; rt = []
    for i, p in enumerate(s):
        a = s[max(i - 1, 0)]; b = s[min(i + 1, len(s) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; l = math.hypot(tx, ty) or 1
        nx, ny = -ty / l, tx / l
        w = max(wf(L[i] / tot), 0) / 2
        c = (p[0] + nx * shift * w, p[1] + ny * shift * w)
        lf.append((c[0] + nx * w, c[1] + ny * w)); rt.append((c[0] - nx * w, c[1] - ny * w))
    return lf, rt

def ribbon(pts, wf, per=24, shift=0.0):
    lf, rt = ribbon_pts(pts, wf, per, shift)
    poly = lf + rt[::-1]
    return 'M' + ' L'.join(fmt(p) for p in poly) + 'Z'

def edge(pts, wf, side=1, per=24):
    """points along one edge of a ribbon (side=1 left, -1 right)"""
    lf, rt = ribbon_pts(pts, wf, per)
    return lf if side == 1 else rt

def sub(pts, t0, t1, per=24):
    """sub-polyline of a spline between normalised arc positions"""
    s = sample(pts, per)
    L = [0.0]
    for i in range(1, len(s)):
        L.append(L[-1] + math.hypot(s[i][0] - s[i - 1][0], s[i][1] - s[i - 1][1]))
    tot = L[-1]
    return [p for p, l in zip(s, L) if t0 * tot <= l <= t1 * tot]

def P(d, fill='none', stroke=None, sw=None, op=None, extra=''):
    s = f'<path d="{d}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        s += f' opacity="{op}"'
    return s + (f' {extra}' if extra else '') + '/>'

def ln(pts, w, col, a=0.2, b=0.2, op=None, extra='', per=24):
    return P(ribbon(pts, taperf(w, a, b), per), fill=col, op=op, extra=extra)

def poly_d(pts):
    return 'M' + ' L'.join(fmt(p) for p in pts) + 'Z'

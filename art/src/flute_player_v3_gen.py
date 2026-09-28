import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import *

W, H = 1000, 1300
HX, HY, HA = 590.0, 425.0, 6.0

def T(p):
    x, y = rotp(p, HA); return (HX + x, HY + y)

FL = (-560.0, 70.0); FR = (62.0, 113.0)
FA = math.degrees(math.atan2(FR[1] - FL[1], FR[0] - FL[0]))
FLEN = math.hypot(FR[0] - FL[0], FR[1] - FL[1])

def Fl(p):
    x, y = rotp(p, FA); return (FL[0] + x, FL[1] + y)

def F(p):
    return T(Fl(p))

HEAD = f'translate({HX} {HY}) rotate({HA})'
FLUTE = f'{HEAD} translate({FL[0]} {FL[1]}) rotate({FA:.3f})'

def grav(pts, k=1.0):
    """make a head-local hanging lock fall vertically in world space"""
    y0 = pts[0][1]
    s = math.tan(math.radians(HA)) * k
    return [(x + s * (y - y0), y) for x, y in pts]

# ---------------------------------------------------------------- colours
SKIN = '#FFEADF'; SKIN_SH = '#F3B7A6'; SKIN_SH2 = '#E4988A'; SKIN_LN = '#7A3B3A'
HAIR_LN = '#120C16'
RIM = '#FFD690'; RIM2 = '#FFF3D6'

out = []
A = out.append

# ================================================================ defs
A(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <radialGradient id="bg" cx="660" cy="330" r="820" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFF8E4"/><stop offset="0.12" stop-color="#FFE7AE"/>
    <stop offset="0.3" stop-color="#F7BE72"/><stop offset="0.55" stop-color="#DA8753"/>
    <stop offset="0.8" stop-color="#9A5238"/><stop offset="1" stop-color="#5B2E27"/>
  </radialGradient>
  <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/><stop offset="0.35" stop-color="#FFF4D2" stop-opacity="0.85"/>
    <stop offset="1" stop-color="#FFE0A0" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="lant" cx="0.5" cy="0.45" r="0.6">
    <stop offset="0" stop-color="#FFF0B8"/><stop offset="0.45" stop-color="#FF9A4A"/><stop offset="1" stop-color="#C2382A"/>
  </radialGradient>
  <linearGradient id="hairL" x1="0" y1="-250" x2="0" y2="340" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#3A3358"/><stop offset="0.25" stop-color="#221C36"/>
    <stop offset="0.6" stop-color="#16121F"/><stop offset="1" stop-color="#2A1F2E"/>
  </linearGradient>
  <linearGradient id="hairW" x1="0" y1="250" x2="0" y2="1300" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#221C36"/><stop offset="0.5" stop-color="#15111D"/><stop offset="1" stop-color="#3E2630"/>
  </linearGradient>
  <linearGradient id="skinG" x1="0" y1="-150" x2="0" y2="160" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFF1E8"/><stop offset="1" stop-color="#FFE2D4"/>
  </linearGradient>
  <linearGradient id="eyeW" x1="0" y1="-10" x2="0" y2="28" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#D9C3D3"/><stop offset="0.45" stop-color="#FBF4F6"/><stop offset="1" stop-color="#FFFFFF"/>
  </linearGradient>
  <radialGradient id="iris" cx="0.5" cy="0.82" r="0.75">
    <stop offset="0" stop-color="#FFD27A"/><stop offset="0.35" stop-color="#D98A38"/>
    <stop offset="0.7" stop-color="#7A3A1E"/><stop offset="1" stop-color="#2A1216"/>
  </radialGradient>
  <linearGradient id="robe" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFDF9"/><stop offset="0.6" stop-color="#FDF3F1"/><stop offset="1" stop-color="#F6DDE4"/>
  </linearGradient>
  <linearGradient id="sleeveG" x1="0" y1="500" x2="0" y2="910" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFFDF8"/><stop offset="0.55" stop-color="#FDF1F0"/><stop offset="1" stop-color="#F4C9D6"/>
  </linearGradient>
  <linearGradient id="skirt" x1="0" y1="700" x2="0" y2="1300" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#3A4A9C"/><stop offset="0.5" stop-color="#2A3478"/><stop offset="1" stop-color="#1A1F4E"/>
  </linearGradient>
  <linearGradient id="fluteG" x1="0" y1="-12" x2="0" y2="12" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFF0C8"/><stop offset="0.25" stop-color="#EDC47C"/><stop offset="0.7" stop-color="#C98E48"/><stop offset="1" stop-color="#8E5824"/>
  </linearGradient>
  <linearGradient id="handG" x1="0" y1="-20" x2="0" y2="100" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFF0E6"/><stop offset="1" stop-color="#FAD9CA"/>
  </linearGradient>
  <linearGradient id="shawl" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#EAF0FF"/><stop offset="1" stop-color="#C9D4FF"/>
  </linearGradient>
  <linearGradient id="sash" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F7A9BC"/><stop offset="1" stop-color="#D86A88"/>
  </linearGradient>
  <filter id="b1" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.2"/></filter>
  <filter id="b3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="b6" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="b24" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="24"/></filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="11"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer>
  </filter>
  <filter id="paper" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="3"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.85  0 0 0 0 0.6  0 0 0 0.35 -0.05"/>
  </filter>
''')

# ---------------------------------------------------------------- face geometry (head-local)
FACE = [(-130, -140), (-129, -40), (-126, 18), (-117, 58), (-99, 93), (-70, 122), (-38, 140), (-14, 147),
        (8, 143), (44, 127), (84, 101), (114, 66), (132, 18), (137, -40), (137, -140)]
FACE_D = bez(FACE, closed=True)
A(f'<clipPath id="cFace"><path d="{FACE_D}"/></clipPath>')

# eyes
def mir(p, k=0.9, m=-4):
    return (m - (p[0] - m) * k, p[1])

UP = [(20, 6), (32, -3), (50, -9), (70, -9), (88, -3), (98, 4), (104, 12)]
LO = [(20, 6), (33, 17), (52, 25), (74, 26), (92, 20), (104, 12)]
def eye_d(up, lo):
    return bez(up) + bez(lo[::-1], move=False)[0:] + 'Z'
EYE_N = eye_d(UP, LO)
UPF = [mir(p) for p in UP]; LOF = [mir(p) for p in LO]
EYE_F = eye_d(UPF, LOF)
A(f'<clipPath id="cEyeN"><path d="{EYE_N}"/></clipPath><clipPath id="cEyeF"><path d="{EYE_F}"/></clipPath>')

# ---------------------------------------------------------------- hair locks (head-local)
BANGS = [
    ([(-80, -190), (-124, -140), (-146, -70), (-150, 0), (-140, 52)], 62),
    ([(46, -196), (118, -144), (150, -76), (158, -6), (150, 50)], 64),
    ([(-60, -196), (-96, -140), (-112, -80), (-108, -30), (-96, -6)], 56),
    ([(28, -200), (74, -140), (98, -80), (102, -36), (94, -12)], 56),
    ([(-44, -200), (-70, -140), (-78, -80), (-70, -40), (-60, -18)], 52),
    ([(10, -204), (38, -140), (54, -86), (56, -44), (48, -26)], 52),
    ([(-8, -204), (4, -140), (12, -80), (12, -40), (6, -14)], 44),
    ([(-24, -204), (-36, -140), (-38, -80), (-30, -30), (-18, 4)], 46),
]
THIN = [
    ([(-12, -196), (-22, -120), (-16, -60), (-6, -10), (2, 18)], 8),
    ([(60, -190), (96, -120), (110, -60), (112, -10), (104, 22)], 7),
    ([(-70, -190), (-102, -120), (-118, -60), (-122, 0), (-114, 30)], 7),
]
DOME = [(-152, 40), (-164, -60), (-154, -150), (-104, -214), (-22, -238), (64, -234), (146, -198), (194, -124), (204, -30), (198, 50), (100, 30), (0, 20), (-100, 30)]
DOME_D = bez(DOME, closed=True)
DOME_TOP = [(-154, -150), (-104, -214), (-22, -238), (64, -234), (146, -198), (194, -124), (150, -140), (0, -168), (-120, -140)]
bang_paths = [ribbon(p, lockf(w, 0.15, 0.85)) for p, w in BANGS]
thin_paths = [ribbon(p, lockf(w, 0.1, 1.0)) for p, w in THIN]
A('<clipPath id="cBangs">' + ''.join(f'<path d="{d}"/>' for d in bang_paths) + f'<path d="{bez(DOME_TOP, closed=True)}"/></clipPath>')
A('<g id="bangShape">' + ''.join(f'<path d="{d}"/>' for d in bang_paths) + '</g>')
A(f'<clipPath id="cHair"><path d="{DOME_D}"/>' + ''.join(f'<path d="{d}"/>' for d in bang_paths) + '</clipPath>')
A('</defs>')

# ================================================================ BACKGROUND
A(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
A(f'<rect width="{W}" height="{H}" filter="url(#paper)" opacity="0.5"/>')
# light shafts
for ang, wdt, op in [(-150, 60, .10), (-120, 40, .08), (-60, 70, .09), (-30, 45, .07), (20, 60, .06), (160, 50, .06)]:
    a = math.radians(ang); b1 = math.radians(ang - wdt / 20); b2 = math.radians(ang + wdt / 20)
    cx, cy = 650, 330
    pts = [(cx, cy), (cx + 1400 * math.cos(b1), cy + 1400 * math.sin(b1)), (cx + 1400 * math.cos(b2), cy + 1400 * math.sin(b2))]
    A(P(poly_d(pts), fill='#FFF3D0', op=op, extra='filter="url(#b12)"'))
# distant lanterns & window glows
for x, y, rx, ry, op in [(96, 150, 34, 42, .75), (880, 110, 28, 34, .7), (930, 420, 22, 27, .55), (60, 520, 20, 25, .45), (840, 700, 26, 32, .35)]:
    A(f'<ellipse cx="{x}" cy="{y}" rx="{rx * 2.2}" ry="{ry * 2.2}" fill="#FFB060" opacity="{op * .35}" filter="url(#b24)"/>')
    A(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#lant)" opacity="{op}" filter="url(#b6)"/>')
# blurred plum branch, top-right background
A(ln([(1010, 40), (900, 90), (820, 170), (760, 200)], 16, '#6A382A', 0.02, .5, op=.55, extra='filter="url(#b6)"'))
A(ln([(900, 90), (870, 30), (840, 0)], 9, '#6A382A', 0.02, .6, op=.5, extra='filter="url(#b6)"'))
for x, y, r in [(770, 196, 16), (800, 160, 13), (842, 150, 18), (880, 100, 14), (860, 40, 12), (930, 80, 15), (960, 60, 11), (820, 200, 10)]:
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFC3CF" opacity="0.7" filter="url(#b6)"/>')
# sun disc behind head
A('<circle cx="650" cy="320" r="330" fill="url(#sun)" opacity="0.95"/>')
A('<circle cx="650" cy="320" r="235" fill="none" stroke="#FFFBEF" stroke-width="2" opacity="0.35" filter="url(#b1)"/>')
# bokeh
import random
random.seed(4)
for i in range(38):
    x = random.uniform(0, W); y = random.uniform(0, H * 0.8); r = random.choice([5, 7, 9, 12, 16, 22])
    d = math.hypot(x - 650, y - 330)
    if d < 180: continue
    op = random.uniform(0.15, 0.45)
    A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FFF1C8" opacity="{op:.2f}" filter="url(#b3)"/>')
    if r > 10:
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r - 1}" fill="none" stroke="#FFF8E2" stroke-width="1.2" opacity="{op * .8:.2f}" filter="url(#b1)"/>')

# ================================================================ BACK HAIR (world)
BACK = [
    ([(500, 300), (420, 500), (384, 700), (362, 900), (332, 1060)], 84),
    ([(510, 270), (446, 480), (422, 680), (412, 880), (392, 1070)], 110),
    ([(540, 240), (500, 480), (488, 720), (470, 960), (452, 1180)], 120),
    ([(640, 230), (660, 480), (672, 740), (684, 1000), (694, 1230)], 150),
    ([(690, 240), (760, 500), (782, 760), (804, 1000), (826, 1250)], 112),
    ([(710, 260), (792, 480), (818, 700), (846, 920), (884, 1120)], 118),
    ([(730, 290), (836, 500), (872, 700), (912, 880), (966, 1040)], 90),
    ([(730, 280), (824, 470), (858, 640), (906, 780), (968, 876)], 58),
]
FLY = [([(800, 340), (862, 444), (904, 560), (952, 640), (1004, 690)], 9),
       ([(790, 380), (842, 520), (874, 660), (926, 772)], 7),
       ([(786, 300), (850, 380), (900, 470), (944, 520)], 6)]
A(P(bez([(456, 300), (400, 640), (372, 900), (560, 980), (840, 960), (900, 860), (858, 620), (792, 330), (620, 200)], closed=True), fill='url(#hairW)'))
for pts, w in BACK:
    A(P(ribbon(pts, lockf(w, .12, .8)), fill='url(#hairW)', stroke=HAIR_LN, sw=1.5, extra='stroke-linejoin="round"'))
    A(ln(sub(pts, .08, .85), 1.2, '#4B4166', .3, .4, op=.8))
    A(P(ribbon(sub(pts, .16, .3), taperf(w * .3, .45, .45), 12, shift=.4), fill='#5A5280', op=.55))
    if pts[-1][0] > 900:
        e = edge(pts, lockf(w, .12, .8), -1)
        A(ln(e[:int(len(e) * .92)], 4, RIM, .1, .3, op=.85, extra='filter="url(#b1)"'))
for pts, w in FLY:
    A(P(ribbon(pts, lockf(w, 0, 1.2)), fill='#2A2236', stroke=HAIR_LN, sw=.8))
    A(ln(pts, 1.4, RIM, .1, .5, op=.8))


# ================================================================ BODY (world)
W_N = F((510, 66))    # near wrist (enters sleeve)
W_F = F((246, 92))    # far wrist

NECK = [(546, 470), (542, 560), (536, 628), (522, 668), (584, 690), (650, 664), (638, 626), (632, 556), (630, 470)]
NECK_D = bez(NECK, closed=True)
A(f'<clipPath id="cNeck"><path d="{NECK_D}"/></clipPath>')

# sheer shawl (pibo) streaming behind the figure
def shawl(pts, w0, twist):
    return ribbon(pts, lambda t: w0 * (0.18 + 0.82 * abs(math.cos(math.pi * (t - twist) * 1.6))) * (1 - .25 * t), 30)
SHAWL_R = [(760, 850), (850, 900), (884, 980), (872, 1060), (916, 1150), (1010, 1210)]
SHAWL_L = [(200, 870), (150, 930), (150, 1010), (112, 1090), (40, 1150), (-30, 1190)]
for pts, w0, tw in [(SHAWL_R, 64, .3), (SHAWL_L, 64, .35)]:
    d = shawl(pts, w0, tw)
    A(P(d, fill='#C8D2F6', op=.78))
    A(P(d, fill='#FFF3E0', op=.35, extra='filter="url(#b3)" style="mix-blend-mode:screen"'))
    A(P(d, stroke='#5C6494', sw=1.6, op=.85))
    A(ln(sub(pts, .05, .95), 1.4, '#FFFFFF', .2, .2, op=.8))
# neck
A(P(NECK_D, fill='#FCE0D2', stroke=SKIN_LN, sw=2))
A(f'<g clip-path="url(#cNeck)"><path d="{FACE_D}" transform="{HEAD} translate(6 34)" fill="{SKIN_SH}"/>'
  f'<path d="{FACE_D}" transform="{HEAD} translate(4 22)" fill="{SKIN_SH2}" opacity=".35" filter="url(#b3)"/></g>')
A(ln([(628, 500), (634, 580), (644, 640)], 5, RIM2, .2, .3, op=.8, extra='filter="url(#b1)"'))

# torso (outer robe) + collar
TORSO = [(522, 662), (470, 674), (436, 690), (412, 720), (404, 800), (412, 900), (420, 1000), (770, 1000), (790, 900), (800, 800), (795, 720), (768, 694), (720, 676), (650, 662)]
A(P(bez(TORSO, closed=True), fill='url(#robe)', stroke='#6A4B5A', sw=2))
A(ln([(512, 676), (540, 650), (584, 640), (630, 648), (662, 670)], 16, '#F2A2B6', 0, 0))
A(ln([(514, 668), (540, 644), (584, 634), (630, 642), (660, 662)], 2.5, '#E8C06A', 0, 0))
A(P(poly_d([(522, 664), (600, 740), (648, 662)]), fill='#FFFFFF'))
A(ln([(528, 662), (566, 704), (598, 742)], 20, '#F2A2B6', 0, 0))
A(ln([(650, 660), (604, 716), (548, 800)], 26, '#F2A2B6', 0, 0))
A(ln([(640, 660), (596, 716), (540, 798)], 4, '#E8C06A', 0, 0, op=.9))
A(ln([(662, 664), (614, 720), (560, 802)], 1.6, '#6A4B5A', 0, 0))
A(ln([(637, 657), (590, 713), (534, 795)], 1.6, '#6A4B5A', 0, 0))

# skirt (chest-high ruqun) + ribbons
SKIRT = [(420, 740), (780, 740), (812, 900), (840, 1060), (872, 1300), (330, 1300), (366, 1060), (392, 900)]
A(P(poly_d(SKIRT), fill='url(#skirt)', stroke='#141838', sw=2, extra='stroke-linejoin="round"'))
A(f'<clipPath id="cSkirt"><path d="{poly_d(SKIRT)}"/></clipPath><g clip-path="url(#cSkirt)">')
for x0, x1, sh in [(470, 430, 1), (530, 510, 0), (600, 600, 1), (670, 690, 0), (740, 780, 1)]:
    A(P(poly_d([(x0, 760), (x0 + 22, 760), (x1 + 40, 1300), (x1, 1300)]), fill='#11163A', op=.45 if sh else .25, extra='filter="url(#b3)"'))
    A(ln([(x0 + 26, 760), (x1 + 50, 1300)], 3, '#6376C8', .1, .1, op=.55, extra='filter="url(#b1)"'))
for gy in range(900, 1320, 70):
    for gx in range(340, 900, 64):
        ox = gx + (32 if (gy // 70) % 2 else 0)
        for k in range(4):
            a = math.radians(k * 90 + 45)
            A(f'<circle cx="{ox + 3.6 * math.cos(a):.1f}" cy="{gy + 3.6 * math.sin(a):.1f}" r="2.3" fill="#B9A6D8" opacity=".32"/>')
        A(f'<circle cx="{ox}" cy="{gy}" r="1.3" fill="#E8C06A" opacity=".5"/>')
A(ln([(780, 740), (812, 900), (840, 1060), (872, 1300)], 14, '#F6C07A', 0, 0, op=.75, extra='filter="url(#b6)"'))
A(ln([(790, 760), (818, 900), (846, 1060), (876, 1300)], 3, '#FFE2A8', 0, 0, op=.9))
A('</g>')
for pts, w in [([(600, 880), (592, 990), (600, 1100), (614, 1200), (626, 1300)], 34), ([(622, 880), (640, 990), (656, 1090), (684, 1190), (712, 1300)], 30)]:
    d = ribbon(pts, lambda t, w=w: w * (0.85 + 0.25 * math.sin(t * 3.4)))
    A(P(d, fill='url(#sash)', stroke='#8A2C48', sw=1.6))
    A(ln(sub(pts, .02, .98), w * .22, '#FFD6E0', .1, .1, op=.55, extra=f'transform="translate({-w * .22:.0f} 0)"'))
    A(ln(sub(pts, .02, .98), w * .18, '#A53A5C', .1, .1, op=.35, extra=f'transform="translate({w * .28:.0f} 0)"'))
# jade pendant on a cord
A(ln([(560, 880), (556, 960), (560, 1010)], 2.4, '#B8323F', 0, 0))
A('<circle cx="560" cy="1034" r="22" fill="#7AD6B6" stroke="#2E7A63" stroke-width="2"/><circle cx="560" cy="1034" r="7" fill="#2A3478" stroke="#2E7A63" stroke-width="1.5"/>')
A('<path d="M548,1022 A16,16 0 0 1 574,1024" fill="none" stroke="#E6FFF6" stroke-width="3" opacity=".8"/>')
for dx in (-8, -3, 2, 7):
    A(ln([(560 + dx * .3, 1056), (560 + dx, 1100), (560 + dx * 1.4, 1140)], 2, '#C0303F', 0, .2))

def plum_sprig(x, y, sc, rot, op=.75):
    A(f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})" opacity="{op}">')
    A(ln([(0, 0), (20, -10), (44, -12), (66, -26)], 3, '#B77C8C', .05, .6))
    A(ln([(20, -10), (30, 6), (44, 14)], 2.2, '#B77C8C', .05, .6))
    for bx, by, r in [(44, -12, 9), (66, -26, 7), (44, 14, 7.5), (14, -6, 6)]:
        for k in range(5):
            a = math.radians(k * 72 - 90)
            A(f'<circle cx="{bx + r * .55 * math.cos(a):.1f}" cy="{by + r * .55 * math.sin(a):.1f}" r="{r * .5:.1f}" fill="#F7B6C6" stroke="#D98AA2" stroke-width=".7"/>')
        A(f'<circle cx="{bx}" cy="{by}" r="{r * .25:.1f}" fill="#E8C06A"/>')
    A('<circle cx="74" cy="-32" r="3" fill="#F29AB0"/><circle cx="52" cy="20" r="2.6" fill="#F29AB0"/>')
    A('</g>')

# ---- sleeve helper
def sleeve(pts, clip_id, valleys, rims, hem, dark_side, motifs=()):
    d = bez(pts, closed=True)
    A(f'<clipPath id="{clip_id}"><path d="{d}"/></clipPath>')
    A(P(d, fill='url(#sleeveG)'))
    A(f'<g clip-path="url(#{clip_id})">')
    A(P(bez(dark_side, closed=True), fill='#EAD3DE'))
    for v, w in valleys:
        A(P(ribbon(v, taperf(w, .55, 0), 20), fill='#EAD3DE'))
    for v, w in valleys:
        A(P(ribbon(v, taperf(w * .45, .6, 0), 20, shift=.3), fill='#D7B9CB'))
    for m in motifs:
        plum_sprig(*m)
    A(ln(hem, 34, '#F2A2B6', 0, 0, op=.95))
    A(ln([(x, y - 14) for x, y in hem], 3, '#E8C06A', 0, 0))
    A(ln([(x, y - 9) for x, y in hem], 1.2, '#FFF3F6', 0, 0, op=.8))
    for i in range(0, len(hem) - 1):
        (x0, y0), (x1, y1) = hem[i], hem[i + 1]
        for k in range(4):
            t = (k + .5) / 4; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            for j in range(5):
                a = math.radians(j * 72 - 90)
                A(f'<circle cx="{x + 4 * math.cos(a):.1f}" cy="{y + 3 + 4 * math.sin(a):.1f}" r="2.6" fill="#FFF6F8" opacity=".9"/>')
            A(f'<circle cx="{x:.1f}" cy="{y + 3:.1f}" r="1.6" fill="#E8C06A"/>')
    for r in rims:
        A(ln(r, 16, '#FFEBC2', .1, .2, op=.9, extra='filter="url(#b3)"'))
        A(ln(r, 3, '#FFFBEE', .1, .2))
    A('</g>')
    A(P(d, stroke='#6A4B5A', sw=2.4, extra='stroke-linejoin="round"'))
    for v, w in valleys:
        A(ln(v, 2.2, '#8E6A82', .35, .15, op=.85))

# far sleeve
cL = (W_F[0] - 26, W_F[1] - 4); cR = (W_F[0] + 26, W_F[1] + 6)
FAR = [cR, (290, 596), (290, 650), (334, 682), (400, 682), (448, 692), (460, 760), (444, 842), (372, 894), (262, 908), (170, 882), (128, 804), (134, 722), (176, 620), cL]
sleeve(FAR, 'cSF',
       valleys=[([(254, 560), (244, 660), (240, 780), (250, 905)], 42), ([(310, 690), (318, 780), (324, 860), (330, 900)], 34),
                ([(186, 650), (170, 740), (164, 820), (172, 885)], 30), ([(392, 690), (410, 770), (420, 850)], 30)],
       rims=[[cL, (176, 620), (134, 722)], [(322, 686), (400, 682), (448, 692)]],
       hem=[(128, 850), (170, 890), (262, 910), (372, 898), (444, 850)],
       dark_side=[(260, 670), (330, 690), (440, 690), (460, 760), (440, 850), (372, 900), (300, 910), (280, 780)],
       motifs=[(150, 800, 1.1, -30), (330, 760, .9, 20), (220, 700, .7, -60)])
A(P(f'M{fmt(cL)} Q{W_F[0] - 4:.1f},{W_F[1] + 24:.1f} {fmt(cR)} Q{W_F[0] + 2:.1f},{W_F[1] - 10:.1f} {fmt(cL)}Z', fill='#C9798F', stroke='#6A4B5A', sw=1.8))

# ================================================================ HEAD
A(f'<g transform="{HEAD}">')
# --- bun
A('<circle cx="46" cy="-262" r="66" fill="url(#hairL)" stroke="#120C16" stroke-width="2.4"/>')
for r0, a0, a1, w in [(56, 200, 380, 3), (44, 230, 420, 2.6), (30, 250, 470, 2.2), (60, 150, 250, 2)]:
    pts = [(46 + r0 * math.cos(math.radians(a)) * (1 - (a - a0) / (a1 - a0) * .25), -262 + r0 * .92 * math.sin(math.radians(a)) * (1 - (a - a0) / (a1 - a0) * .25)) for a in range(a0, a1 + 1, 20)]
    A(ln(pts, w, '#0E0A14', .2, .3, op=.8))
for r0, a0, a1 in [(50, 200, 290), (36, 215, 300), (22, 230, 310)]:
    pts = [(46 + r0 * math.cos(math.radians(a)), -266 + r0 * .9 * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 10)]
    A(ln(pts, 7, '#7B72A8', .35, .35, op=.75))
    A(ln(pts, 2.4, '#D6CEF4', .4, .4, op=.8))
A(ln([(46 + 66 * math.cos(math.radians(a)), -262 + 66 * math.sin(math.radians(a))) for a in range(250, 380, 10)], 6, RIM, .2, .3, op=.9, extra='filter="url(#b1)"'))
# --- hairpin (through the bun)
A(ln([(-78, -318), (40, -268), (176, -210)], 8, '#8A5A1E', .05, .05))
A(ln([(-76, -318), (40, -269), (174, -211)], 3, '#F6D68A', .05, .1))
A('<circle cx="-80" cy="-319" r="6" fill="#E9C46A" stroke="#6E4512" stroke-width="1.5"/>')

# --- dome (skull hair)
A(P(DOME_D, fill='url(#hairL)', stroke=HAIR_LN, sw=2.6))
A(ln([(60, -234), (140, -200), (190, -128), (202, -40)], 5, RIM, .1, .3, op=.95, extra='filter="url(#b1)"'))

# face
A(P(FACE_D, fill='url(#skinG)'))
A('<g clip-path="url(#cFace)">')
A(f'<use href="#bangShape" transform="translate(5 16)" fill="{SKIN_SH}" opacity="0.85"/>')
A(P(bez([(-134, -20), (-128, 50), (-104, 100), (-60, 140), (-14, 152), (-40, 170), (-140, 170)], closed=True), fill=SKIN_SH, op=.55, extra='filter="url(#b6)"'))
A(ln([(136, -60), (134, 10), (118, 64), (88, 104)], 10, RIM2, .1, .4, op=.9, extra='filter="url(#b3)"'))
A('</g>')
# jaw line (tapered, coloured)
A(ln([(-128, -6), (-123, 40), (-108, 80), (-82, 112), (-46, 136), (-14, 148), (10, 143), (48, 126), (88, 98), (117, 62), (134, 16)], 3.0, SKIN_LN, .08, .08))

# blush
A(f'<ellipse cx="76" cy="54" rx="38" ry="16" fill="#FF7C8A" opacity="0.42" filter="url(#b6)"/>')
A(f'<ellipse cx="-84" cy="54" rx="30" ry="14" fill="#FF7C8A" opacity="0.38" filter="url(#b6)"/>')
for i in range(5):
    A(ln([(52 + i * 10, 64), (60 + i * 10, 48)], 1.8, '#E35F6F', .3, .3, op=.75))
for i in range(4):
    A(ln([(-104 + i * 9, 62), (-97 + i * 9, 48)], 1.6, '#E35F6F', .3, .3, op=.7))

A('<ellipse cx="92" cy="44" rx="9" ry="4" fill="#FFFFFF" opacity=".55" filter="url(#b1)"/>')

# eyes
def draw_eye(up, lo, eye_d, clip, ic, rx, ry, k=1.0):
    A(P(eye_d, fill='url(#eyeW)'))
    A(f'<g clip-path="url(#{clip})">')
    cx, cy = ic
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#iris)"/>')
    A(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#2A1216" stroke-width="2"/>')
    A(f'<ellipse cx="{cx}" cy="{cy + 3}" rx="{rx * .36:.1f}" ry="{ry * .44:.1f}" fill="#1A0B10"/>')
    for a in range(-60, 61, 20):
        r0 = 0.45; r1 = 0.9; t = math.radians(90 + a)
        A(ln([(cx + rx * r0 * math.cos(t), cy + 3 + ry * r0 * math.sin(t)), (cx + rx * r1 * math.cos(t), cy + 3 + ry * r1 * math.sin(t))], 1.6, '#FFD98E', .3, .5, op=.45))
    A(f'<ellipse cx="{cx}" cy="{cy + ry * .62:.1f}" rx="{rx * .62:.1f}" ry="{ry * .28:.1f}" fill="#FFE3A0" opacity="0.55" filter="url(#b3)"/>')
    # lid shadow
    sh = [(x, y + 11) for x, y in up]
    A(P(bez(up) + ' L' + ' L'.join(fmt(p) for p in sh[::-1]) + 'Z', fill='#3A2233', op=.45, extra='filter="url(#b1)"'))
    A(f'<ellipse cx="{cx + rx * .36 * k:.1f}" cy="{cy - ry * .22:.1f}" rx="{rx * .3:.1f}" ry="{ry * .2:.1f}" fill="#FFFFFF"/>')
    A(f'<circle cx="{cx - rx * .42 * k:.1f}" cy="{cy + ry * .45:.1f}" r="{rx * .12:.1f}" fill="#FFFFFF" opacity="0.95"/>')
    A(f'<circle cx="{cx + rx * .5 * k:.1f}" cy="{cy + ry * .35:.1f}" r="{rx * .07:.1f}" fill="#FFFFFF" opacity="0.8"/>')
    A('</g>')

def lash(up, lo, k=1):
    # main lash line: thin inner, thick outer
    A(P(ribbon(up, lambda t: 1.8 + 6.2 * ss(0.05, 0.6, t), 24), fill='#1E1016'))
    o = up[-1]; o2 = up[-2]
    A(ln([o2, o, (o[0] + 8 * k, o[1] + 7), (o[0] + 13 * k, o[1] + 15)], 6.5, '#1E1016', 0.0, .7))
    A(ln([(o2[0] - 2 * k, o2[1] - 2), (o2[0] + 6 * k, o2[1] - 6), (o2[0] + 14 * k, o2[1] - 6)], 3.0, '#1E1016', 0.0, .8))
    A(ln([(o[0] - 3 * k, o[1] - 3), (o[0] + 5 * k, o[1] - 4), (o[0] + 13 * k, o[1] - 1)], 2.6, '#1E1016', 0.0, .8))
    A(ln([(o2[0] - 12 * k, o2[1] - 5), (o2[0] - 6 * k, o2[1] - 12), (o2[0] + 1 * k, o2[1] - 15)], 2.2, '#1E1016', 0.0, .8))
    # crease
    cr = [(x, y - 13 - 4 * math.sin(math.pi * i / (len(up) - 1))) for i, (x, y) in enumerate(up[1:-1])]
    A(ln(cr, 1.7, '#8E5563', .2, .3, op=.8))
    # lower lash
    A(ln(lo[2:], 2.2, '#7A4150', .5, .15, op=.8))
    A(ln([lo[-2], (lo[-2][0] + 4 * k, lo[-2][1] + 6)], 1.2, '#7A4150', .1, .6, op=.6))

draw_eye(UP, LO, EYE_N, 'cEyeN', (52, 12), 22, 27, 1)
lash(UP, LO, 1)
draw_eye(UPF, LOF, EYE_F, 'cEyeF', (-72, 12), 19.5, 27, 1)
lash(UPF, LOF, -1)

# brows
A(ln([(34, -52), (58, -60), (82, -59), (104, -50)], 3.4, '#3A2230', .15, .45, op=.85))
A(ln([mir(p) for p in [(34, -52), (58, -60), (82, -59), (104, -50)]], 3.0, '#3A2230', .15, .45, op=.85))

# nose + mouth
A(ln([(-6, 52), (-13, 63), (-20, 70)], 2.6, '#C27468', .2, .5))
A('<ellipse cx="-3" cy="56" rx="2.4" ry="3" fill="#FFFFFF" opacity="0.7"/>')
A(P(bez([(-30, 98), (-22, 92), (-12, 90), (-2, 92), (5, 98)]) + ' L-12,101Z', fill='#EC8E95'))
A(ln([(-31, 97), (-22, 91.5), (-12, 89.5), (-2, 91.5), (6, 97)], 1.8, '#A24A56', .25, .25))
A('<ellipse cx="-8" cy="93" rx="5" ry="1.6" fill="#FFFFFF" opacity=".55"/>')
A(ln([(-4, 76), (-12, 80), (-20, 78)], 5, SKIN_SH, .3, .3, op=.5, extra='filter="url(#b1)"'))

# --- side locks framing the face
SIDE = [
    (grav([(-126, -112), (-150, -40), (-158, 0), (-162, 90), (-152, 170), (-156, 250), (-140, 322), (-126, 340)]), 52),
    (grav([(-130, -40), (-148, 40), (-148, 120), (-138, 190), (-124, 252), (-112, 262)]), 22),
    (grav([(128, -112), (156, -40), (164, 0), (170, 90), (162, 170), (170, 250), (156, 322), (140, 342)]), 56),
    (grav([(134, -40), (154, 40), (156, 120), (146, 190), (132, 248), (120, 258)]), 24),
]
for pts, w in SIDE:
    A(P(ribbon(pts, lambda t, w=w: w * (.25 + .75 * ss(0, .18, t)) * (1 - t) ** .75), fill='url(#hairL)', stroke=HAIR_LN, sw=1.8, extra='stroke-linejoin="round"'))
    A(ln(sub(pts, .1, .85), 1.2, '#0E0A14', .3, .4, op=.6))
    A(ln(sub(pts, .15, .45), 2.2, '#8A80BE', .4, .4, op=.8))


# bangs: fill as one mass, then lock edges as tapered line art
A(P(''.join(bang_paths), fill='url(#hairL)'))
# inner shadow where locks overlap (darker toward the tips)
A('<g clip-path="url(#cBangs)">')
for pts, w in BANGS:
    A(P(ribbon(sub(pts, .35, 1), taperf(w * .3, .3, .0), 16, shift=0.7), fill='#120C18', op=.35))
A('</g>')
# angel-ring shine band
A('<g clip-path="url(#cBangs)">')
RING = [(-156, -96), (-110, -150), (-30, -176), (50, -174), (130, -146), (184, -96)]
A(P(ribbon(RING, taperf(30, .2, .2), 30), fill='#5A5288', op=.9, extra='filter="url(#b3)"'))
A(P(ribbon(RING, taperf(16, .25, .25), 30, shift=-.3), fill='#8A80BE', op=.8, extra='filter="url(#b1)"'))
rs = sample(RING, 30)
for i in range(4, len(rs) - 8, 11):
    seg = rs[i:i + 7]
    A(P(ribbon(seg, taperf(4, .5, .5), 4), fill='#E2DBFF', op=.85))
A('</g>')
for d, (pts, w) in zip(bang_paths, BANGS):
    for side in (1, -1):
        e = edge(pts, lockf(w, 0.15, 0.85), side)
        A(ln(e[int(len(e) * .28):], 2.4, HAIR_LN, .45, .04))
    A(ln(sub(pts, .1, .82), 1.3, '#0E0A14', .3, .4, op=.55))
    A(ln(sub(pts, .25, .7), 1.1, '#5E5484', .3, .4, op=.7))
for d, (pts, w) in zip(thin_paths, THIN):
    A(P(d, fill='#241E33', stroke=HAIR_LN, sw=1.0))
A('</g>')


# near sleeve (player's left arm crossing below the chin)
nT = (W_N[0] + 24, W_N[1] - 16); nB = (W_N[0] - 18, W_N[1] + 16)
NEAR = [nT, (560, 612), (630, 672), (686, 730), (716, 700), (748, 684), (784, 684), (806, 720), (812, 760), (814, 810), (800, 864), (730, 898), (630, 906), (530, 886), (470, 848), (450, 760), (448, 660), nB]
sleeve(NEAR, 'cSN',
       valleys=[([(492, 600), (486, 700), (490, 800), (502, 890)], 46), ([(562, 640), (568, 740), (580, 840), (592, 910)], 38),
                ([(640, 700), (652, 790), (662, 860), (674, 910)], 30), ([(722, 730), (746, 800), (762, 870)], 26)],
       dark_side=[(448, 640), (480, 600), (500, 640), (520, 760), (540, 890), (470, 850), (450, 760)],
       motifs=[(620, 800, 1.2, -20), (740, 760, .9, 30), (500, 780, .8, -50)],
       rims=[[(748, 684), (784, 684), (806, 720), (814, 810), (800, 864)], [nT, (560, 612), (630, 672), (690, 742)]],
       hem=[(452, 800), (470, 848), (530, 888), (630, 908), (730, 900), (806, 858)])
A(P(f'M{fmt(nT)} Q{W_N[0] + 16:.1f},{W_N[1] + 14:.1f} {fmt(nB)} Q{W_N[0] - 6:.1f},{W_N[1] - 18:.1f} {fmt(nT)}Z', fill='#C9798F', stroke='#6A4B5A', sw=1.8))

# ================================================================ FLUTE + HANDS (flute frame)
A(f'<g transform="{FLUTE}">')
# wrists/back of hands first so the sleeve cuffs read as behind? (hands sit in front of flute)
# near hand (player's left): BEHIND the flute — palm, thumb, and finger arches over the top edge
NEAR_PALM = [(420, 0), (500, 0), (514, 22), (526, 44), (536, 70), (500, 80), (474, 62), (448, 42), (428, 24)]
A(P(bez(NEAR_PALM, closed=True), fill='url(#handG)', stroke=SKIN_LN, sw=1.8))
A(P(bez([(420, 10), (510, 10), (516, 30), (424, 26)], closed=True), fill=SKIN_SH, op=.6, extra='filter="url(#b1)"'))

for u, w in [(484, 15), (467, 16), (450, 15), (434, 12.5)]:
    A(f'<ellipse cx="{u}" cy="-13" rx="{w / 2 + 1:.1f}" ry="11" fill="#FFEFE6" stroke="{SKIN_LN}" stroke-width="1.6"/>')
    A(ln([(u - w * .3, -20), (u, -23), (u + w * .3, -20)], 1.6, '#FFFFFF', .3, .3, op=.8))
A(f'<rect x="0" y="-12" width="{FLEN:.1f}" height="24" rx="11" fill="url(#fluteG)" stroke="#4A2C12" stroke-width="1.8"/>')
A(ln([(10, -6), (FLEN - 10, -6)], 3.2, '#FFF7E0', .05, .05, op=.85))
A(ln([(10, 7), (FLEN - 10, 7)], 4, '#7A461A', .05, .05, op=.35))
for u in (150, 360):
    A(f'<rect x="{u - 2}" y="-12.5" width="5" height="25" rx="2" fill="#B07A3A" stroke="#4A2C12" stroke-width="1"/>')
for u0, u1 in [(8, 34), (FLEN - 30, FLEN - 8), (104, 112), (300, 308), (522, 530)]:
    A(f'<rect x="{u0}" y="-13" width="{u1 - u0}" height="26" rx="2.5" fill="#B42A38" stroke="#5A1018" stroke-width="1.2"/>')
    for u in range(int(u0) + 3, int(u1), 4):
        A(f'<line x1="{u}" y1="-12" x2="{u}" y2="12" stroke="#E8707C" stroke-width="0.8" opacity=".8"/>')
A('<rect x="498" y="-9" width="14" height="9" rx="2" fill="#FFF8E8" opacity=".75" stroke="#8A5A2A" stroke-width=".8"/>')
A('<ellipse cx="505" cy="-4.5" rx="3.2" ry="2.4" fill="#3A220E" opacity=".7"/>')
for u in (62, 82):
    A(f'<ellipse cx="{u}" cy="-3" rx="3.2" ry="2.6" fill="#3A220E"/>')

def finger(pts, w, fill='url(#handG)'):
    A(P(ribbon(pts, lambda t: w * (1 - .12 * t), 16), fill=fill, stroke=SKIN_LN, sw=1.6))
    tip = pts[-1]
    A(f'<circle cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="{w * .44:.1f}" fill="{fill}" stroke="{SKIN_LN}" stroke-width="1.6"/>')
    A(P(ribbon(pts, lambda t: w * .86 * (1 - .12 * t), 16), fill=fill))
    A(f'<circle cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="{w * .38:.1f}" fill="{fill}"/>')

# far hand (player's right): in FRONT of the flute, back of hand to viewer, fingers arch over the top
FAR_BACK = [(204, 42), (210, 32), (228, 28), (246, 27), (264, 25), (280, 30), (285, 46), (279, 64), (268, 80), (264, 100), (232, 102), (228, 82), (214, 64)]
A(P(bez(FAR_BACK, closed=True), fill='url(#handG)', stroke=SKIN_LN, sw=1.8))
A(f'<clipPath id="cFH"><path d="{bez(FAR_BACK, closed=True)}"/></clipPath><g clip-path="url(#cFH)">')
A(P(bez([(200, 66), (240, 76), (290, 70), (290, 110), (200, 110)], closed=True), fill=SKIN_SH, op=.55, extra='filter="url(#b3)"'))
A(ln([(212, 60), (230, 96)], 8, SKIN_SH, .2, .2, op=.5, extra='filter="url(#b1)"'))
A(ln([(234, 84), (250, 88), (264, 84)], 1.3, '#C98A7A', .3, .3, op=.7))
for x in (224, 242, 260):
    A(ln([(x + 4, 38), (x + 2, 60), (x - 2, 86)], 3, '#F5C9B8', .3, .4, op=.8))
A('</g>')
for (bu, bv), (tu, tv), w in [((217, 36), (214, 1), 14), ((233, 32), (231, -9), 16.5), ((250, 31), (248, -12), 17.5), ((267, 29), (265, -9), 16.5)]:
    pts = [(bu, bv), (bu - 1, (bv + tv) / 2 + 4), (tu, tv)]
    finger(pts, w)
    mid = ((bu + tu) / 2, (bv + tv) / 2 + 4)
    A(ln([(mid[0] - w * .32, mid[1] - 2), (mid[0], mid[1] - 4), (mid[0] + w * .32, mid[1] - 2)], 1.2, '#C98A7A', .3, .3, op=.9))
    A(ln([(tu - w * .25, tv + 2), (tu + w * .2, tv - 2)], 2, '#FFFFFF', .3, .3, op=.85))
    A(ln([(bu + w * .38, bv - 2), (tu + w * .38, tv + 4)], w * .25, SKIN_SH, .2, .3, op=.55))
    A(f'<ellipse cx="{bu - 1}" cy="{bv + 2}" rx="{w * .3:.1f}" ry="2.2" fill="#FFFFFF" opacity=".6"/>')

# near-hand fingertips draped down over the front of the flute (nails toward viewer)
for u, w, tip in [(484, 15, 4), (467, 16, 5), (450, 15, 4), (434, 12.5, -2)]:
    finger([(u, -14), (u + 1, -6), (u + 2, tip)], w, fill='#FFEFE6')
    A(f'<ellipse cx="{u + 2:.1f}" cy="{tip - 1:.1f}" rx="{w * .26:.1f}" ry="5.2" fill="#FFD9D2" stroke="#D29A8E" stroke-width=".8"/>')
    A(f'<rect x="{u + 2 - w * .18:.1f}" y="{tip - 4:.1f}" width="{w * .16:.1f}" height="4" rx="1.5" fill="#FFFFFF" opacity=".8"/>')
    A(ln([(u - w * .3, -10), (u + 1, -12), (u + w * .3, -10)], 1.1, '#C98A7A', .3, .3, op=.8))
# lips' soft shadow on the flute
A('<ellipse cx="552" cy="-4" rx="18" ry="6" fill="#6A3A1A" opacity=".35" filter="url(#b1)"/>')
A('</g>')

# flute tassel (hangs with gravity)
ta = F((16, 12))
A(ln([ta, (ta[0] - 2, ta[1] + 20), (ta[0] + 1, ta[1] + 40)], 2.6, '#B42A38', 0, 0))
kx, ky = ta[0] + 1, ta[1] + 48
A(P(poly_d([(kx, ky - 9), (kx + 9, ky), (kx, ky + 9), (kx - 9, ky)]), fill='#C8303F', stroke='#6A1420', sw=1.4))
A(f'<circle cx="{kx}" cy="{ky + 30}" r="17" fill="#7AD6B6" stroke="#2E7A63" stroke-width="2"/><circle cx="{kx}" cy="{ky + 30}" r="5.5" fill="#E7A357" stroke="#2E7A63" stroke-width="1.2"/>')
A(ln([(kx, ky + 9), (kx, ky + 13)], 2, '#B42A38', 0, 0))
for dx in (-9, -5, -1, 3, 7, 10):
    A(ln([(kx + dx * .3, ky + 48), (kx + dx * .8, ky + 90), (kx + dx * 1.3 + 4, ky + 130)], 2.2, '#C22E3E', 0, .15))
A(f'<rect x="{kx - 8}" y="{ky + 46}" width="16" height="8" rx="3" fill="#E8C06A" stroke="#6E4512" stroke-width="1"/>')

# hairpin ornament + dangles (buyao)
A(f'<g transform="{HEAD}">')
for fx, fy, r, rot in [(160, -226, 15, 10), (184, -240, 11, 40), (178, -206, 10, 70), (140, -236, 9, 20)]:
    for k in range(5):
        a = math.radians(rot + k * 72)
        A(f'<ellipse cx="{fx + r * .62 * math.cos(a):.1f}" cy="{fy + r * .62 * math.sin(a):.1f}" rx="{r * .55:.1f}" ry="{r * .45:.1f}" transform="rotate({rot + k * 72} {fx + r * .62 * math.cos(a):.1f} {fy + r * .62 * math.sin(a):.1f})" fill="#FFD3DE" stroke="#B24A6A" stroke-width="1.1"/>')
    A(f'<circle cx="{fx}" cy="{fy}" r="{r * .28:.1f}" fill="#FFE07A" stroke="#B07A20" stroke-width=".8"/>')
    for k in range(5):
        a = math.radians(rot + 36 + k * 72)
        A(f'<circle cx="{fx + r * .42 * math.cos(a):.1f}" cy="{fy + r * .42 * math.sin(a):.1f}" r="1.2" fill="#C0702A"/>')
A('</g>')
da = T((166, -208))
for dx, L, bead in [(-10, 70, '#FFF6EE'), (0, 104, '#7AD6B6'), (10, 84, '#FFF6EE')]:
    x0 = da[0] + dx
    A(ln([(da[0], da[1]), (x0, da[1] + L * .5), (x0 + 2, da[1] + L)], 1.4, '#D9A94A', 0, 0))
    for k in range(1, 4):
        A(f'<circle cx="{x0 + 2 * k / 4:.1f}" cy="{da[1] + L * k / 4:.1f}" r="3.2" fill="#FFF8F0" stroke="#B89A70" stroke-width=".8"/>')
    A(f'<path d="M{x0 + 2:.1f},{da[1] + L:.1f} c-7,7 -7,15 0,17 c7,-2 7,-10 0,-17z" fill="{bead}" stroke="#6E6040" stroke-width="1"/>')


# ================================================================ ATMOSPHERE + GRADE
A('<defs><radialGradient id="warm" cx="700" cy="300" r="760" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFE3A6" stop-opacity=".9"/><stop offset=".6" stop-color="#FFB870" stop-opacity=".25"/><stop offset="1" stop-color="#FF9A5A" stop-opacity="0"/></radialGradient>'
  '<radialGradient id="vig" cx="560" cy="560" r="900" gradientUnits="userSpaceOnUse"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#2A0E0A" stop-opacity=".5"/></radialGradient>'
  '<linearGradient id="pet" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFB9C9"/></linearGradient></defs>')

def petal(x, y, sc, rot, op=1, blur=None):
    f = f' filter="url(#{blur})"' if blur else ''
    A(f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})" opacity="{op}"{f}>'
      '<path d="M0,0 C6,-10 20,-12 28,-4 L24,0 L28,4 C20,12 6,10 0,0Z" fill="url(#pet)" stroke="#D77A93" stroke-width="1"/>'
      '<path d="M3,0 C10,-3 17,-3 22,0" fill="none" stroke="#F2A0B4" stroke-width="1" opacity=".7"/></g>')

# motes + petals trailing from the flute's far end, drifting up-left (the music)
end = F((0, 0))
random.seed(9)
for i in range(26):
    t = i / 25
    x = end[0] + 30 - t * 60 + 40 * math.sin(t * 7)
    y = end[1] - 20 - t * 330 + 18 * math.cos(t * 5)
    r = random.uniform(1.5, 4.2)
    A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="#FFE7A8" opacity="{.35 * (1 - t) + .1:.2f}" filter="url(#b3)"/>')
    A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * .6:.1f}" fill="#FFFFFF" opacity="{.9 * (1 - t) + .1:.2f}"/>')
for x, y, sc, rot in [(70, 300, 1.0, -20), (140, 220, .8, 30), (40, 170, .9, 70), (190, 120, .7, -50), (300, 70, .8, 10),
                      (860, 520, .9, 40), (930, 760, .8, -30), (720, 150, .7, 60)]:
    petal(x, y, sc, rot)
petal(880, 1180, 3.2, -25, .85, 'b6')
petal(-10, 980, 2.6, 20, .8, 'b6')
petal(960, 40, 2.2, 60, .7, 'b3')

# light: warm wash, bloom around the halo, backlit edge glow on the head
A(f'<rect width="{W}" height="{H}" fill="url(#warm)" opacity=".3" style="mix-blend-mode:soft-light"/>')
A('<ellipse cx="700" cy="330" rx="210" ry="190" fill="#FFF0C8" opacity=".22" filter="url(#b24)" style="mix-blend-mode:screen"/>')
A(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
A(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')

A('</svg>')
open(os.path.join(HERE, '..', 'flute_player_v3.svg'), 'w').write('\n'.join(out))
print('written', len(out))

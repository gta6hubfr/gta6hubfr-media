"""Design kit « tuto en étapes » pour @gta6hubfr_ (format de la vidéo de référence).
Layout 1080x1920 : bandeau étape en haut, gameplay au centre, bande coucher de soleil + sous-titres en bas."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = os.path.expanduser('~/.fonts/')
BLK, XB, SB = 'BarlowCondensed-BlackItalic.ttf', 'BarlowCondensed-ExtraBoldItalic.ttf', 'BarlowCondensed-SemiBoldItalic.ttf'
INK = (14, 7, 26); WHITE = (255, 255, 255); GOLD = (255, 205, 70); PINK = (255, 62, 165); RED = (235, 42, 78)
YEL = (255, 199, 44)

TOP_H = 340            # bandeau du haut
GY0, GY1 = 340, 1300   # zone gameplay (1080x960)
BAND_Y = 1300          # bande du bas

def font(n, s): return ImageFont.truetype(FD + n, s)
def clamp(x): return max(0.0, min(1.0, x))
def prog(t, a, d): return (t - a) / d if d > 0 else 1.0
def ease_out_cubic(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_out_back(x, s=1.7): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1

def text_layer(txt, size, fill, fname=BLK, stroke=0, stroke_fill=(0, 0, 0)):
    f = font(fname, size); l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    im = Image.new('RGBA', (r - l + 24, b - t + 24), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((12 - l, 12 - t), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im

def grad_text(txt, size, c1=(255, 236, 150), c2=(255, 140, 30), fname=BLK, stroke=8):
    """texte dégradé vertical (or -> orange) avec contour sombre + ombre."""
    f = font(fname, size); l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    w, h = r - l + 40, b - t + 40
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).text((20 - l, 20 - t), txt, font=f, fill=255)
    st = Image.new('L', (w, h), 0); ImageDraw.Draw(st).text((20 - l, 20 - t), txt, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    g = Image.new('RGBA', (w, h))
    for y in range(h):
        k = clamp((y - 20) / max(1, h - 40)); c = tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))
        ImageDraw.Draw(g).line([(0, y), (w, y)], fill=c + (255,))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); sh.putalpha(st.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .8)))
    out.alpha_composite(sh, (0, 6))
    dark = Image.new('RGBA', (w, h), (40, 8, 30, 255)); dark.putalpha(st); out.alpha_composite(dark)
    g.putalpha(mask); out.alpha_composite(g)
    return out

def put(base, layer, x, y, anchor='mm', alpha=1.0):
    if alpha <= 0.01: return
    if alpha < 1:
        layer = layer.copy(); layer.putalpha(layer.split()[3].point(lambda v: int(v * alpha)))
    if anchor == 'mm': x -= layer.width / 2; y -= layer.height / 2
    elif anchor == 'lm': y -= layer.height / 2
    elif anchor == 'rm': x -= layer.width; y -= layer.height / 2
    base.alpha_composite(layer, (int(x), int(y)))

def scaled(layer, s):
    if abs(s - 1) < 1e-3: return layer
    return layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.BICUBIC)

# ---------- bande coucher de soleil (bas) ----------
def _palm(d, x0, y0, h, flip=1, col=(26, 6, 34)):
    pts = []
    for i in range(21):
        k = i / 20; pts.append((x0 + flip * (math.sin(k * 1.3) * h * 0.16), y0 - k * h))
    for i in range(len(pts) - 1):
        wdt = int(20 - 10 * i / 20); d.line([pts[i], pts[i + 1]], fill=col, width=wdt)
    tx, ty = pts[-1]
    d.ellipse((tx - 16, ty - 16, tx + 16, ty + 16), fill=col)
    for ang, ln in [(-165, 1.0), (-140, 0.9), (-115, 0.75), (-90, 0.6), (-65, 0.75), (-40, 0.9), (-15, 1.0), (10, 0.95), (-190, 0.95)]:
        a = math.radians(ang); L = h * 0.42 * ln; poly_up = []; poly_dn = []
        for j in range(13):
            k = j / 12; droop = (k ** 2) * L * 0.55
            px = tx + flip * math.cos(a) * L * k; py = ty + math.sin(a) * L * k + droop
            th = math.sin(k * math.pi) * 26 + 2; nx, ny = -math.sin(a) * flip, math.cos(a)
            poly_up.append((px + nx * th, py + ny * th)); poly_dn.append((px - nx * th, py - ny * th))
        d.polygon(poly_up + poly_dn[::-1], fill=col)

def sunset_band():
    h = H - BAND_Y; im = Image.new('RGBA', (W, h)); d = ImageDraw.Draw(im)
    hz = int(h * 0.80)  # horizon
    top, mid, low = (34, 8, 62), (120, 20, 110), (238, 70, 120)
    for y in range(hz):
        k = y / hz
        c = tuple(int(top[i] + (mid[i] - top[i]) * min(1, k * 1.4)) for i in range(3)) if k < 0.7 else \
            tuple(int(mid[i] + (low[i] - mid[i]) * ((k - 0.7) / 0.3)) for i in range(3))
        d.line([(0, y), (W, y)], fill=c + (255,))
    # soleil rayé
    R = 250; cx, cy = W // 2, hz - 10
    sun = Image.new('RGBA', (2 * R, 2 * R)); sd = ImageDraw.Draw(sun)
    for y in range(2 * R):
        k = y / (2 * R); c1, c2 = (255, 228, 90), (255, 70, 120)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3)); sd.line([(0, y), (2 * R, y)], fill=c + (255,))
    m = Image.new('L', (2 * R, 2 * R), 0); md = ImageDraw.Draw(m); md.ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
    y = int(R * 0.42); gap = 4
    while y < 2 * R:
        md.rectangle((0, y, 2 * R, y + gap), fill=0); y += 26; gap = min(gap + 3, 18)
    sun.putalpha(m)
    glow = Image.new('RGBA', (2 * R + 200, 2 * R + 200)); ImageDraw.Draw(glow).ellipse((60, 60, 2 * R + 140, 2 * R + 140), fill=(255, 120, 120, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(50)); im.alpha_composite(glow, (cx - R - 100, cy - R - 100))
    im.alpha_composite(sun.crop((0, 0, 2 * R, R + (hz - cy))), (cx - R, cy - R))
    # sol + grille
    for y in range(hz, h):
        k = (y - hz) / max(1, h - hz); c = tuple(int(a + (b - a) * k) for a, b in zip((60, 10, 70), (18, 4, 30)))
        d.line([(0, y), (W, y)], fill=c + (255,))
    for i in range(-14, 15):
        d.line([(cx + i * 22, hz), (cx + i * 190, h)], fill=(255, 60, 170, 150), width=2)
    yy = hz; step = 6
    while yy < h: d.line([(0, yy), (W, yy)], fill=(255, 60, 170, 140), width=2); yy += step; step = int(step * 1.6) + 2
    d.line([(0, hz), (W, hz)], fill=(255, 150, 210, 255), width=3)
    _palm(d, 70, hz + 8, 560, 1); _palm(d, 205, hz + 14, 400, -1)
    _palm(d, W - 70, hz + 8, 600, -1); _palm(d, W - 230, hz + 16, 380, 1)
    # filet néon en haut de la bande
    neon = Image.new('RGBA', (W, 24)); ImageDraw.Draw(neon).rectangle((0, 9, W, 14), fill=PINK + (255,))
    im.alpha_composite(neon.filter(ImageFilter.GaussianBlur(5)), (0, -6)); ImageDraw.Draw(im).rectangle((0, 0, W, 3), fill=(255, 170, 220, 255))
    return im

# ---------- bandeau du haut ----------
def top_band():
    im = Image.new('RGBA', (W, TOP_H)); d = ImageDraw.Draw(im)
    for y in range(TOP_H):
        k = y / TOP_H; c = tuple(int(a + (b - a) * k) for a, b in zip((10, 4, 20), (44, 10, 64)))
        d.line([(0, y), (W, y)], fill=c + (255,))
    d.rectangle((0, TOP_H - 4, W, TOP_H), fill=(255, 150, 210, 255))
    neon = Image.new('RGBA', (W, 30)); ImageDraw.Draw(neon).rectangle((0, 12, W, 18), fill=PINK + (255,))
    im.alpha_composite(neon.filter(ImageFilter.GaussianBlur(6)), (0, TOP_H - 22))
    return im

def step_badge(n, size=104):
    b = Image.new('RGBA', (size + 20, size + 20)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((10, 14, size + 10, size + 14), 24, fill=(120, 10, 40, 255))
    g = Image.new('RGBA', (size, size)); gd = ImageDraw.Draw(g)
    for y in range(size):
        k = y / size; c = tuple(int(a + (bb - a) * k) for a, bb in zip((255, 90, 80), (225, 30, 90))); gd.line([(0, y), (size, y)], fill=c + (255,))
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), 24, fill=255); g.putalpha(m)
    b.alpha_composite(g, (10, 6)); t = text_layer(str(n), int(size * 0.82), WHITE, BLK, 4, (90, 0, 30)); put(b, t, 10 + size / 2 - 2, 6 + size / 2 - 2)
    return b

def badge(size=112, path='/home/claude/repo/tools/rockstar/pdp_2.png'):
    im = Image.open(path).convert('RGBA').resize((size * 4, size * 4), Image.LANCZOS)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((0, 0, im.width - 1, im.height - 1), fill=255); im.putalpha(m)
    im = im.resize((size, size), Image.LANCZOS)
    o = Image.new('RGBA', (size + 8, size + 8)); ImageDraw.Draw(o).ellipse((0, 0, size + 7, size + 7), fill=(255, 150, 210, 255)); o.alpha_composite(im, (4, 4))
    return o

# ---------- boutons PS5 ----------
def ps_key(sym, size=128, active=True, crossed=False):
    k = Image.new('RGBA', (size + 16, size + 22)); d = ImageDraw.Draw(k)
    base = (255, 205, 70) if active else (70, 62, 86); shade = (190, 120, 20) if active else (40, 34, 52)
    d.rounded_rectangle((8, 14, size + 8, size + 14), 26, fill=shade + (255,))
    d.rounded_rectangle((8, 6, size + 8, size + 6), 26, fill=base + (255,))
    ink = INK if active else (200, 196, 210); cx, cy, r = 8 + size / 2, 6 + size / 2, size * 0.25; lw = max(6, size // 14)
    if sym == 'square': d.rectangle((cx - r, cy - r, cx + r, cy + r), outline=ink, width=lw)
    elif sym == 'triangle': d.polygon([(cx, cy - r * 1.15), (cx - r * 1.15, cy + r * 0.85), (cx + r * 1.15, cy + r * 0.85)], outline=ink, width=lw)
    elif sym == 'circle': d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=lw)
    elif sym == 'cross':
        d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=ink, width=lw); d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=ink, width=lw)
    elif sym == 'arrow':
        d.line([(cx - r, cy), (cx + r * 0.7, cy)], fill=ink, width=lw); d.polygon([(cx + r * 1.1, cy), (cx + r * 0.2, cy - r * 0.8), (cx + r * 0.2, cy + r * 0.8)], fill=ink)
    elif sym == 'r2':
        t = text_layer('R2', int(size * 0.5), ink, BLK); put(k, t, cx, cy)
    if crossed: d.line([(14, size), (size + 2, 14)], fill=RED + (255,), width=lw + 2)
    return k

def card(title, w=880, h=250):
    c = Image.new('RGBA', (w + 40, h + 40)); d = ImageDraw.Draw(c)
    sh = Image.new('RGBA', c.size); ImageDraw.Draw(sh).rounded_rectangle((20, 28, w + 20, h + 28), 34, fill=(0, 0, 0, 170))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d.rounded_rectangle((20, 20, w + 20, h + 20), 34, fill=(16, 8, 30, 238), outline=PINK + (255,), width=5)
    if title:
        t = text_layer(title, 46, GOLD, BLK); put(c, t, 20 + w / 2, 20 + 44)
    return c

def lbl(s, size=40, col=WHITE): return text_layer(s, size, col, BLK)

def strike(layer, col=RED):
    l = layer.copy(); d = ImageDraw.Draw(l); y = l.height // 2 + 2; d.line([(10, y), (l.width - 10, y)], fill=col + (255,), width=5); return l

def money(n): return f'{n:,}'.replace(',', ' ') + ' $'

def night_band(seed=3):
    """bande du bas originale : skyline de nuit au bord de l'eau, néon rose/cyan, reflets."""
    import random; rnd = random.Random(seed)
    h = H - BAND_Y; im = Image.new('RGBA', (W, h)); d = ImageDraw.Draw(im)
    hz = int(h * 0.66)
    for y in range(hz):
        k = y / hz; c = tuple(int(a + (b - a) * k ** 1.6) for a, b in zip((8, 6, 26), (40, 18, 78)))
        d.line([(0, y), (W, y)], fill=c + (255,))
    # étoiles
    for _ in range(70):
        x, y = rnd.randrange(W), rnd.randrange(int(hz * 0.55)); a = rnd.randrange(60, 200)
        d.point((x, y), fill=(255, 255, 255, a))
    # lueur d'horizon cyan
    glow = Image.new('RGBA', (W, 200)); ImageDraw.Draw(glow).rectangle((0, 90, W, 110), fill=(40, 220, 255, 140))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(28)), (0, hz - 100))
    # skyline
    city = Image.new('RGBA', (W, hz)); cd = ImageDraw.Draw(city); x = -10
    while x < W:
        bw = rnd.randrange(40, 110); bh = rnd.randrange(60, 300) if not (380 < x < 700) else rnd.randrange(30, 120)
        top = hz - bh; cd.rectangle((x, top, x + bw, hz), fill=(14, 8, 30, 255))
        if rnd.random() < 0.25: cd.rectangle((x + bw // 2 - 2, top - 40, x + bw // 2 + 2, top), fill=(14, 8, 30, 255))
        for wy in range(top + 10, hz - 8, 16):
            for wx in range(x + 8, x + bw - 8, 13):
                if rnd.random() < 0.28:
                    col = rnd.choice([(255, 210, 120), (255, 90, 180), (90, 230, 255)])
                    cd.rectangle((wx, wy, wx + 5, wy + 7), fill=col + (rnd.randrange(140, 230),))
        x += bw + rnd.randrange(0, 8)
    im.alpha_composite(city)
    # contour néon des toits
    edge = city.split()[3].filter(ImageFilter.FIND_EDGES)
    neon = Image.new('RGBA', (W, hz), PINK + (0,)); neon.putalpha(edge.point(lambda v: 200 if v > 40 else 0))
    im.alpha_composite(neon.filter(ImageFilter.GaussianBlur(2)))
    # eau + reflets
    for y in range(hz, h):
        k = (y - hz) / (h - hz); c = tuple(int(a + (b - a) * k) for a, b in zip((22, 10, 48), (6, 3, 14)))
        d.line([(0, y), (W, y)], fill=c + (255,))
    refl = city.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, W, h - hz)).filter(ImageFilter.GaussianBlur(3))
    refl.putalpha(refl.split()[3].point(lambda v: int(v * 0.35)))
    im.alpha_composite(refl, (0, hz))
    for _ in range(40):
        y = rnd.randrange(hz + 4, h); x0 = rnd.randrange(W); ln = rnd.randrange(20, 120)
        d.line([(x0, y), (x0 + ln, y)], fill=rnd.choice([(255, 90, 180, 110), (90, 230, 255, 110)]), width=2)
    d.line([(0, hz), (W, hz)], fill=(120, 240, 255, 255), width=2)
    # filet néon en haut
    n2 = Image.new('RGBA', (W, 24)); ImageDraw.Draw(n2).rectangle((0, 9, W, 14), fill=PINK + (255,))
    im.alpha_composite(n2.filter(ImageFilter.GaussianBlur(5)), (0, -6)); ImageDraw.Draw(im).rectangle((0, 0, W, 3), fill=(255, 170, 220, 255))
    return im

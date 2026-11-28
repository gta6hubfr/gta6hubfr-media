import sys, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
F = os.path.expanduser('~/.fonts/')
def font(name, size): return ImageFont.truetype(F + name, size)
BLACK = font('BarlowCondensed-BlackItalic.ttf', 10)
YEL = (255, 199, 44); INK = (11, 6, 20); WHITE = (255, 255, 255)
IMG = '/home/claude/rockstar/img/'

REGIONS = [('vice_city', ['VICE CITY']), ('leonida_keys', ['LEONIDA KEYS']),
           ('grassrivers', ['GRASSRIVERS']), ('port_gellhorn', ['PORT GELLHORN']),
           ('ambrosia', ['AMBROSIA']), ('mount_kalaga', ['MOUNT KALAGA', 'NATIONAL PARK'])]

def clamp(x): return max(0.0, min(1.0, x))
def ease_out_cubic(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_cubic(x): x = clamp(x); return x ** 3
def ease_out_back(x, s=1.6):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def prog(t, a, d): return (t - a) / d

_bg = {}
def background(key):
    if key in _bg: return _bg[key]
    im = Image.open(IMG + f'gta6_{key}.jpg').convert('RGB')
    BW, BH = int(W * 1.18), int(H * 1.18)
    s = max(BW / im.width, BH / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    l = (im.width - BW) // 2; t = (im.height - BH) // 2
    im = im.crop((l, t, l + BW, t + BH)).filter(ImageFilter.GaussianBlur(14))
    im = ImageEnhance.Brightness(im).enhance(0.5)
    tint = Image.new('RGB', im.size, (40, 12, 70))
    im = Image.blend(im, tint, 0.28)
    _bg[key] = im
    return im

_card = {}
def card(key):
    if key in _card: return _card[key]
    im = Image.open(IMG + f'gta6_{key}.jpg').convert('RGB')
    cw = 960; ch = int(cw * im.height / im.width)
    im = im.resize((cw, ch), Image.LANCZOS)
    b = 14
    c = Image.new('RGBA', (cw + 2 * b, ch + 2 * b), WHITE + (255,))
    c.paste(im, (b, b))
    _card[key] = c
    return c

def bg_frame(key, t, dur):
    im = background(key)
    p = t / dur
    ox = int((im.width - W) / 2)
    oy = int((im.height - H) * (0.25 + 0.5 * p))
    return im.crop((ox, oy, ox + W, oy + H)).convert('RGBA')

def paste_rot(base, img, cx, cy, angle, shadow=True):
    r = img.rotate(angle, resample=Image.BICUBIC, expand=True)
    if shadow:
        sh = Image.new('RGBA', r.size, (0, 0, 0, 0))
        sh.paste((0, 0, 0, 150), (0, 0), r.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        base.alpha_composite(sh, (int(cx - r.width / 2 + 18), int(cy - r.height / 2 + 28)))
    base.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))

def text_layer(txt, size, fill, fname='BarlowCondensed-BlackItalic.ttf', stroke=0, stroke_fill=None):
    f = font(fname, size)
    l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    im = Image.new('RGBA', (r - l + 40, b - t + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((20 - l, 20 - t), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im

def put(base, layer, x, y, anchor='mm', alpha=1.0):
    if alpha <= 0: return
    if alpha < 1:
        layer = layer.copy(); a = layer.split()[3].point(lambda v: int(v * alpha)); layer.putalpha(a)
    if anchor == 'mm': x -= layer.width / 2; y -= layer.height / 2
    elif anchor == 'lm': y -= layer.height / 2
    elif anchor == 'rm': x -= layer.width; y -= layer.height / 2
    base.alpha_composite(layer, (int(x), int(y)))

def yellow_box(w, h, skew=0.18):
    im = Image.new('RGBA', (int(w + h * skew) + 4, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(h * skew, 0), (w + h * skew, 0), (w, h), (0, h)], fill=YEL + (255,))
    return im

def header(base, t):
    a = ease_out_cubic(prog(t, 0, 0.4))
    hd = text_layer('BIENVENUE À LEONIDA', 46, WHITE, 'BarlowCondensed-ExtraBoldItalic.ttf')
    put(base, hd, 90 - (1 - a) * 60, 150, 'lm', a * 0.9)
    # G6 badge
    bd = Image.new('RGBA', (96, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(bd)
    d.rounded_rectangle((0, 0, 95, 95), 18, fill=YEL)
    g = text_layer('G6', 64, INK); bd.alpha_composite(g, ((96 - g.width) // 2, (96 - g.height) // 2 - 2))
    put(base, bd, 990 - (1 - a) * -60, 150, 'rm', a)

def credit(base):
    c = text_layer('Images : @RockstarGames  ·  Page fan, non officielle', 34, (255, 255, 255, 150), 'BarlowCondensed-SemiBoldItalic.ttf')
    put(base, c, W / 2, 1790)

# ---------------- scenes ----------------
def scene_intro(t, dur=2.4):
    base = bg_frame('vice_city', t, dur)
    dark = Image.new('RGBA', (W, H), INK + (120,)); base.alpha_composite(dark)
    header(base, t)
    # yellow bar wipe
    bw = int(820 * ease_out_cubic(prog(t, 0.05, 0.5)))
    if bw > 0:
        bar = Image.new('RGBA', (bw, 10), YEL + (255,)); base.alpha_composite(bar, (130, 640))
    a1 = ease_out_cubic(prog(t, 0.1, 0.55))
    l1 = text_layer('6 RÉGIONS', 240, WHITE)
    put(base, l1, W / 2 - (1 - a1) * 700, 820, alpha=a1)
    a2 = ease_out_cubic(prog(t, 0.28, 0.55))
    box = yellow_box(820, 230)
    l2 = text_layer('À VISITER', 220, INK)
    x2 = W / 2 + (1 - a2) * 800
    put(base, box, x2, 1080, alpha=a2); put(base, l2, x2, 1072, alpha=a2)
    a3 = ease_out_cubic(prog(t, 0.6, 0.5))
    l3 = text_layer('dans la carte de GTA 6', 72, WHITE, 'BarlowCondensed-SemiBoldItalic.ttf')
    put(base, l3, W / 2, 1290 + (1 - a3) * 40, alpha=a3)
    # exit: everything slides up fast
    e = ease_in_cubic(prog(t, dur - 0.25, 0.25))
    if e > 0:
        out = Image.new('RGBA', (W, H)); out.alpha_composite(base.crop((0, int(e * 300), W, H)), (0, 0))
        fl = Image.new('RGBA', (W, H), YEL + (int(255 * e),)); out.alpha_composite(fl)
        return out
    return base

def scene_region(i, t, dur=1.9):
    key, lines = REGIONS[i]
    base = bg_frame(key, t, dur)
    header(base, 1.0)
    # big outline number behind
    an = ease_out_cubic(prog(t, 0.0, 0.5))
    num = text_layer(f'0{i+1}', 560, (0, 0, 0, 0), 'Anton-Regular.ttf', stroke=4, stroke_fill=YEL + (200,))
    put(base, num, 70 - (1 - an) * 400 - t * 20, 470, 'lm', an * 0.85)
    # counter
    ac = ease_out_cubic(prog(t, 0.2, 0.4))
    cnt = text_layer(f'RÉGION {i+1:02d} / 06', 44, YEL, 'BarlowCondensed-ExtraBoldItalic.ttf')
    put(base, cnt, 990, 470, 'rm', ac)
    ln = int(260 * ac)
    if ln > 0: base.alpha_composite(Image.new('RGBA', (ln, 6), YEL + (255,)), (990 - ln, 505))
    # card: enters from right with overshoot, drifts, exits left
    ae = ease_out_back(prog(t, 0.0, 0.55))
    ax = ease_in_cubic(prog(t, dur - 0.28, 0.28))
    cx = W / 2 + (1 - ae) * 1100 - ax * 1300 - t * 18
    ang = 4 - 7 * ae + ax * 6
    paste_rot(base, card(key), cx, 860, ang)
    # title: white then yellow shadow offset (décalage)
    y = 1330
    for j, ln_txt in enumerate(lines):
        size = 170 if j == 0 else 80
        if len(ln_txt) > 11 and j == 0: size = 150
        yy = y + j * 150
        ay = ease_out_cubic(prog(t, 0.32 + j * 0.08, 0.45))
        aw = ease_out_cubic(prog(t, 0.22 + j * 0.08, 0.45))
        sh = text_layer(ln_txt, size, YEL)
        wt = text_layer(ln_txt, size, WHITE)
        off = -(1 - ax) * 0 - ax * 900
        put(base, sh, W / 2 + 12 - (1 - ay) * 600 + off, yy + 12, alpha=ay)
        put(base, wt, W / 2 - (1 - aw) * 900 + off, yy, alpha=aw)
    credit(base)
    return base

def scene_outro(t, dur=2.6):
    base = bg_frame('jason_lucia_rooftop', t, dur)
    base.alpha_composite(Image.new('RGBA', (W, H), INK + (110,)))
    header(base, 1.0)
    a1 = ease_out_cubic(prog(t, 0.05, 0.5))
    l1 = text_layer('TON PREMIER', 200, WHITE)
    put(base, l1, W / 2 + (1 - a1) * 800, 820, alpha=a1)
    a2 = ease_out_back(prog(t, 0.2, 0.55))
    box = yellow_box(620, 220); l2 = text_layer('ARRÊT ?', 210, INK)
    x2 = W / 2 - (1 - a2) * 900
    put(base, box, x2, 1040, alpha=clamp(a2)); put(base, l2, x2, 1032, alpha=clamp(a2))
    a3 = ease_out_cubic(prog(t, 0.55, 0.5))
    l3 = text_layer('Dis-le en commentaire', 78, WHITE, 'BarlowCondensed-SemiBoldItalic.ttf')
    put(base, l3, W / 2, 1250 + (1 - a3) * 40, alpha=a3)
    a4 = ease_out_cubic(prog(t, 0.8, 0.5))
    l4 = text_layer('@GTA6HUBFR_', 70, YEL, 'BarlowCondensed-ExtraBoldItalic.ttf')
    put(base, l4, W / 2, 1420, alpha=a4)
    credit(base)
    return base

SCENES = [('intro', scene_intro, 2.4)] + [(f'r{i}', (lambda i: (lambda t: scene_region(i, t)))(i), 1.9) for i in range(6)] + [('outro', scene_outro, 2.6)]

def render(name, fn, dur, outdir):
    tmp = f'{outdir}/{name}.tmp.mp4'; final = f'{outdir}/{name}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    S = 1.45
    n = int(round(dur * S * FPS))
    for k in range(n):
        p.stdin.write(fn(k / FPS / S).convert('RGB').tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, final)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        for name, fn, dur, ts in [('intro', scene_intro, 2.4, [0.5, 1.2]), ('r5', SCENES[6][1], 1.9, [0.4, 1.2]), ('outro', scene_outro, 2.6, [1.5])]:
            for tt in ts: fn(tt).convert('RGB').save(f'/home/claude/rockstar/still_{name}_{tt}.jpg', quality=88)
    else:
        out = '/home/claude/rockstar/scenes'; os.makedirs(out, exist_ok=True)
        for name, fn, dur in SCENES: render(name, fn, dur, out)

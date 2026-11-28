"""Montage « Le perroquet balance la planque » — format tuto en étapes (réf. utilisateur)."""
import sys, os, json, subprocess, math
sys.path.insert(0, '/home/claude/pq')
from design import *
from PIL import Image, ImageDraw
import numpy as np

SRC = '/home/claude/opus/perroquet/src.mp4'
OUT = '/home/claude/pq/out'; os.makedirs(OUT, exist_ok=True)
VO = json.load(open('/home/claude/pq/vo.json'))
TAIL = 0.9
END = VO[-1]['start'] + VO[-1]['dur'] + TAIL
SEG_T = [s['start'] for s in VO] + [END]
LOOK = 'eq=contrast=1.12:brightness=0.035:saturation=1.28:gamma=1.14'
CW, CH = 1215, 1080  # fenêtre source de base (ratio 1080x960)
GW, GH = W, GY1 - GY0

# (src_start, dur, focus, zoom keys [(t_rel, z, focus|None)])
SHOTS = {
 0: [(80.00, None, (0.50, 0.45), [(0, 1.32, None), (2.0, 1.06, (0.48, 0.5))])],
 1: [(12.40, None, (0.48, 0.42), [(0, 1.12, None), (1.75, 1.34, (0.55, 0.38))])],
 2: [(26.57, None, (0.46, 0.42), [(0, 1.12, None), (2.1, 1.30, (0.43, 0.52))])],
 3: [(30.97, 1.96, (0.55, 0.55), [(0, 1.12, None)]), (41.27, None, (0.40, 0.52), [(0, 1.12, None)])],
 4: [(44.00, None, (0.47, 0.47), [(0, 1.08, None), (2.66, 1.40, (0.57, 0.40)), (4.25, 1.12, (0.5, 0.47))])],
 5: [(52.55, None, (0.50, 0.655), [(0, 1.42, None), (3.1, 1.58, (0.53, 0.63))])],
 6: [(64.92, 2.0, (0.47, 0.50), [(0, 1.10, None)]), (66.96, None, (0.36, 0.55), [(0, 1.12, None)])],
 7: [(70.30, 5.65, (0.50, 0.52), [(0, 1.10, None)]), (84.78, None, (0.46, 0.47), [(0, 1.08, None)])],
}

def seg_dur(i): return SEG_T[i + 1] - SEG_T[i]

def read_frames(ss, dur):
    n = int(round(dur * FPS))
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', f'{ss:.3f}', '-i', SRC, '-vf', f'fps={FPS},{LOOK}', '-frames:v', str(n),
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    fr = []
    while len(fr) < n:
        b = p.stdout.read(1920 * 1080 * 3)
        if len(b) < 1920 * 1080 * 3: break
        fr.append(Image.frombytes('RGB', (1920, 1080), b))
    p.stdout.close(); p.wait()
    while len(fr) < n: fr.append(fr[-1])
    return fr

def crop_view(im, focus, z):
    cw, ch = CW / z, CH / z
    cx = min(max(focus[0] * 1920, cw / 2), 1920 - cw / 2); cy = min(max(focus[1] * 1080, ch / 2), 1080 - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize((GW, GH), Image.BILINEAR, box=box)

def gameplay_frames(i):
    shots = SHOTS[i]; total = seg_dur(i); n_total = int(round(total * FPS))
    out = []; used = 0.0
    for k, (ss, dur, focus, zk) in enumerate(shots):
        d = dur if dur is not None else total - used
        fr = read_frames(ss, d)
        for j, im in enumerate(fr):
            t = j / FPS; z, f = zk[0][1], focus
            for tk, zz, ff in zk:
                if t >= tk: z = zz; f = ff or f
            # légère poussée continue
            tk0 = max(tk for tk, _, _ in zk if t >= tk)
            z *= 1 + 0.018 * (t - tk0)
            out.append(crop_view(im, f, z))
        used += d
    out = (out + [out[-1]] * n_total)[:n_total]
    return out

# ---------- éléments fixes ----------
TOPB = top_band(); BAND = night_band(); LOGO = badge(112)
CRED = text_layer('Gameplay : ZoneX (YouTube)  ·  Page fan, non officielle', 30, (255, 255, 255, 200), SB)
def title_row(txt, step=None, size=104):
    t = grad_text(txt, size)
    if step is None: return t
    b = step_badge(step, 100); w = b.width + 14 + t.width; h = max(b.height, t.height)
    L = Image.new('RGBA', (w, h)); put(L, b, 0, h / 2, 'lm'); put(L, t, b.width + 14, h / 2, 'lm'); return L
def fit(layer, maxw=1000):
    return scaled(layer, min(1, maxw / layer.width))

TITLES = {  # seg -> [(t_rel, layer)]
 0: [(0, fit(title_row('CE PERROQUET BALANCE', None, 108)))],
 1: [(0, fit(title_row('VA À LA BOUTIQUE', 1)))],
 2: [(0, fit(title_row('PASSE DERRIÈRE', 2)))],
 3: [(0, fit(title_row('VIDE LA COUR', 2)))],
 4: [(0, fit(title_row('PARLE AU PERROQUET', 3)))],
 5: [(0, fit(title_row('OUVRE LA GRILLE', 4)))],
 6: [(0, fit(title_row('BONUS : LE COFFRE', None)))],
 7: [(0, fit(title_row('RÉSULTAT', None, 120))), (VO[7]['words'][6]['s'] - VO[7]['start'], fit(title_row("TU L'AVAIS TROUVÉ ?", None, 108)))],
}

# ---------- cartes ----------
CARD_Y = 1150; CARD_X = 500
def pill(txt, size=84, fg=INK, bg=GOLD, pad=(34, 10)):
    t = text_layer(txt, size, fg, BLK); w, h = t.width + 2 * pad[0], t.height + 2 * pad[1]
    p = Image.new('RGBA', (w, h)); ImageDraw.Draw(p).rounded_rectangle((0, 0, w - 1, h - 1), h // 2 - 6, fill=bg + (255,)); put(p, t, w / 2, h / 2); return p

def card_location():
    c = card(None, 880, 210); d = ImageDraw.Draw(c)
    cx, cy = 20 + 95, 20 + 105  # épingle
    d.ellipse((cx - 38, cy - 52, cx + 38, cy + 24), fill=RED + (255,)); d.polygon([(cx - 34, cy - 4), (cx + 34, cy - 4), (cx, cy + 58)], fill=RED + (255,)); d.ellipse((cx - 15, cy - 30, cx + 15, cy), fill=(16, 8, 30, 255))
    put(c, text_layer('THREE SHEETS LIQUOR', 70, GOLD, BLK), 20 + 175, 20 + 78, 'lm')
    put(c, text_layer('KEY LENTO  ·  DÈS LE CHAPITRE 1', 44, WHITE, XB), 20 + 178, 20 + 150, 'lm')
    return c

def card_route():
    c = card(None, 880, 210)
    put(c, ps_key('arrow', 120), 20 + 100, 20 + 105)
    put(c, text_layer('PAR LA RUELLE DE DROITE', 62, GOLD, BLK), 20 + 190, 20 + 75, 'lm')
    put(c, text_layer('PUIS SAUTE LA CLÔTURE', 46, WHITE, XB), 20 + 192, 20 + 148, 'lm')
    return c

def card_guards(n_down):
    c = card('GARDES ARMÉS DANS LA COUR', 880, 230)
    for k in range(4):
        x = 20 + 190 + k * 165; y = 20 + 150; d = ImageDraw.Draw(c)
        down = k < n_down
        d.rounded_rectangle((x - 58, y - 52, x + 58, y + 52), 22, fill=((70, 62, 86) if down else (255, 205, 70)) + (255,))
        put(c, text_layer(str(k + 1), 70, (200, 196, 210) if down else INK, BLK), x, y)
        if down: d.line([(x - 50, y + 44), (x + 50, y - 44)], fill=RED + (255,), width=10)
    return c

def card_parrot(t):
    c = card('MENU DU PERROQUET', 880, 260)
    ta = w_s(4, 7); s1 = 1 + 0.1 * max(0, math.sin(min(1, max(0, (t - ta) / 0.5)) * math.pi))
    put(c, scaled(ps_key('cross', 112, True), s1), 20 + 140, 20 + 138)
    put(c, text_layer('CASH ?', 46, WHITE, BLK), 20 + 140, 20 + 232)
    put(c, text_layer('PAS', 80, GOLD, BLK), 20 + 440, 20 + 150)
    tb = w_s(4, 10) + 0.15; sh = 12 * math.sin(t * 40) * max(0, 1 - abs(t - tb) / 0.3)
    put(c, ps_key('square', 112, False, True), 20 + 740 + sh, 20 + 138)
    put(c, strike(text_layer('TAIS-TOI', 44, (255, 120, 140), BLK)), 20 + 740 + sh, 20 + 232)
    return c

def card_vent():
    c = card('LA PLANQUE', 880, 230)
    put(c, ps_key('triangle', 112, True), 20 + 120, 20 + 145)
    put(c, text_layer('LA GRILLE', 66, WHITE, BLK), 20 + 215, 20 + 118, 'lm')
    put(c, text_layer('À CÔTÉ DU GÉNÉRATEUR', 46, GOLD, XB), 20 + 217, 20 + 180, 'lm')
    return c

def card_money(label, value, p):
    c = card(label, 880, 250)
    v = int(round(value * ease_out_cubic(p)))
    put(c, pill('+ ' + money(v), 104), 20 + 440, 20 + 155)
    return c

def card_total(p_tot, t):
    c = card('LE PERROQUET PAIE', 900, 330)
    put(c, pill(money(1330), 64, INK, WHITE), 20 + 200, 20 + 125); put(c, text_layer('LA GRILLE', 34, WHITE, BLK), 20 + 200, 20 + 182)
    put(c, text_layer('+', 70, GOLD, BLK), 20 + 450, 20 + 125)
    put(c, pill(money(1047), 64, INK, WHITE), 20 + 700, 20 + 125); put(c, text_layer('LE COFFRE', 34, WHITE, BLK), 20 + 700, 20 + 182)
    if p_tot > 0:
        v = int(round(2377 * ease_out_cubic(p_tot))); pl = pill('= ' + money(v), 96)
        put(c, scaled(pl, 0.6 + 0.4 * ease_out_back(min(1, p_tot * 2))), 20 + 450, 20 + 272)
    return c

def card_cta(t):
    c = card(None, 880, 200)
    put(c, text_layer('DIS-LE EN', 56, WHITE, BLK), 20 + 440, 20 + 62)
    s = 1 + 0.05 * math.sin(t * 6)
    put(c, scaled(grad_text('COMMENTAIRE', 104, stroke=6), s), 20 + 440, 20 + 140)
    return c

def chip_q():
    return pill("TU L'AVAIS TROUVÉ ?", 46, WHITE, PINK, (26, 8))

CHIPQ = chip_q()
LOC, ROUTE, VENT = card_location(), card_route(), card_vent()

def w_s(seg, idx): return VO[seg]['words'][idx]['s'] - VO[seg]['start']

def cards_for(i, t):
    """renvoie [(layer, appear_t)] actifs au temps t (relatif au segment)."""
    if i == 0:
        L = []
        L.append((CHIPQ, -1, 410))
        a = w_s(0, 7)
        if t >= a: L.append((card_money('CASH CACHÉ PAR LE GANG', 2300, prog(t, a, 1.1)), a, CARD_Y))
        return L
    if i == 1: return [(LOC, 0.5, CARD_Y)] if t >= 0.5 else []
    if i == 2: return [(ROUTE, 0.45, CARD_Y)] if t >= 0.45 else []
    if i == 3:
        n = sum(1 for x in (0.55, 1.45, 2.25, 3.0) if t >= x)
        return [(card_guards(n), 0.2, CARD_Y)] if t >= 0.2 else []
    if i == 4: return [(card_parrot(t), 0.9, CARD_Y - 15)] if t >= 0.9 else []
    if i == 5:
        a = w_s(5, 10)
        if t < 0.4: return []
        if t < a: return [(VENT, 0.4, CARD_Y)]
        return [(card_money('LA GRILLE', 1330, prog(t, a, 0.9)), a, CARD_Y)]
    if i == 6:
        a = w_s(6, 5)
        return [(card_money('LE COFFRE DU BUREAU', 1047, prog(t, a, 0.9)), a, CARD_Y)] if t >= a else []
    if i == 7:
        q = w_s(7, 6)
        if t < q: return [(card_total(prog(t, w_s(7, 1), 1.2) if t >= w_s(7, 1) else 0, t), 0.15, CARD_Y - 40)]
        return [(card_cta(t), q, CARD_Y)]
    return []

# ---------- sous-titres ----------
NUMC = GOLD
def cap_layer(w):
    col = NUMC if any(ch.isdigit() for ch in w) or w.strip('!?.,: ').upper() in ('CASH', 'TAIS-TOI') else WHITE
    w = w.rstrip('.,;')
    if w.endswith(' :'): w = w[:-2]
    return fit(text_layer(w.upper(), 118, col, BLK, 11, (0, 0, 0)), 980)
CAPS = {}
def caption_at(i, t):
    for wd in VO[i]['words']:
        a, b = wd['s'] - VO[i]['start'], wd['e'] - VO[i]['start']
        if a <= t < max(b, a + 0.12): return wd['w'], a
    return None, None

def build(i):
    fr = gameplay_frames(i); n = len(fr); dur = seg_dur(i)
    tmp = f'{OUT}/s{i}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for k in range(n):
        t = k / FPS
        b = Image.new('RGBA', (W, H), INK + (255,))
        b.paste(fr[k], (0, GY0))
        # vignette légère en bas du gameplay pour la carte
        b.alpha_composite(TOPB, (0, 0)); b.alpha_composite(BAND, (0, BAND_Y))
        b.alpha_composite(LOGO, (28, 26))
        # titre d'étape
        cur = None; t0 = 0
        for tt, L in TITLES[i]:
            if t >= tt: cur, t0 = L, tt
        if cur is not None:
            if i == 0 and t0 == 0: put(b, cur, W / 2, 258)
            else:
                a = ease_out_back(prog(t, t0, 0.32)); put(b, scaled(cur, 0.7 + 0.3 * a), W / 2, 258, alpha=clamp(prog(t, t0, 0.12)))
        if i == 0 and t < 1.95:
            r = 78 + 8 * math.sin(t * 9); al = int(255 * (1 - clamp(prog(t, 1.7, 0.25))))
            ring = Image.new('RGBA', (240, 240)); dr = ImageDraw.Draw(ring)
            dr.ellipse((120 - r, 120 - r, 120 + r, 120 + r), outline=GOLD + (al,), width=9)
            b.alpha_composite(ring, (643 - 120, 719 - 120))
        # cartes
        for L, a0, y in cards_for(i, t):
            a = ease_out_back(prog(t, a0, 0.35))
            put(b, scaled(L, 0.85 + 0.15 * a), CARD_X if L is not CHIPQ else W / 2, y + (1 - clamp(a)) * 60, alpha=clamp(prog(t, a0, 0.15)))
        # sous-titre mot par mot
        w, a0 = caption_at(i, t)
        if w:
            key = w
            if key not in CAPS: CAPS[key] = cap_layer(w)
            s = 1 + 0.14 * (1 - ease_out_cubic(prog(t, a0, 0.12)))
            put(b, scaled(CAPS[key], s), W / 2, 1418)
        put(b, CRED, W / 2, 1880)
        p.stdin.write(b.convert('RGB').tobytes())
    p.stdin.close(); assert p.wait() == 0
    return tmp

if __name__ == '__main__':
    todo = [int(x) for x in sys.argv[1:]] or list(range(len(VO)))
    for i in todo: print(build(i), flush=True)

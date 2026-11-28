import sys; sys.path.insert(0,'/home/claude/rockstar')
from kit2 import *

def s_open(t, d):
    base = kenburns('vice_city_01', t / d, True, 0.55)
    top_fade(base); bottom_fade(base, 0.45)
    header(base, t)
    a1 = ease_out_cubic(prog(t, 0.3, 0.8)); a2 = ease_out_back(prog(t, 0.6, 0.8))
    put(base, text_layer('GTA 6', 230, YEL), W/2 - (1-a1)*700, 1290, alpha=a1)
    box = yellow_box(800, 210); x2 = W/2 + (1-clamp(a2))*900
    put(base, box, x2, 1490, alpha=clamp(a2)); put(base, text_layer('EST SORTI', 200, INK), x2, 1482, alpha=clamp(a2))
    a3 = ease_out_cubic(prog(t, 1.2, 0.7))
    put(base, text_layer('Jeudi 19 novembre 2026  ·  PS5 et Xbox Series X|S', 50, WHITE, 'BarlowCondensed-SemiBoldItalic.ttf'), W/2, 1650 + (1-a3)*30, alpha=a3)
    credit(base); return base

SHOTS = [('leonida_keys_01', 'LEONIDA KEYS', True, 0.4), ('mount_kalaga_04', 'MOUNT KALAGA', False, 0.5), ('vice_city_08', 'VICE CITY', True, 0.6)]
def make_shot(i):
    key, region, zi, pan = SHOTS[i]
    def f(t, d):
        base = kenburns(key, t / d, zi, pan)
        top_fade(base); bottom_fade(base, 0.55)
        header(base, 1.0)
        label(base, t, region, i + 1, 3)
        # exit wipe: yellow bar sweeps
        e = ease_in_cubic(prog(t, d - 0.35, 0.35))
        if e > 0:
            base.alpha_composite(Image.new('RGBA', (int(W * e), H), INK + (255,)), (0, 0))
        credit(base); return base
    return f

def s_end(t, d):
    base = kenburns('vice_city_15', t / d, False, 0.5)
    # entry: reveal from the ink wipe
    e = 1 - ease_out_cubic(prog(t, 0, 0.45))
    top_fade(base); bottom_fade(base, 0.4)
    header(base, 1.0)
    a1 = ease_out_cubic(prog(t, 0.4, 0.8)); a2 = ease_out_back(prog(t, 0.65, 0.8))
    put(base, text_layer('TU Y ES', 210, WHITE), W/2 + (1-a1)*700, 1260, alpha=a1)
    box = yellow_box(640, 210); x2 = W/2 - (1-clamp(a2))*900
    put(base, box, x2, 1460, alpha=clamp(a2)); put(base, text_layer('DÉJÀ ?', 200, INK), x2, 1452, alpha=clamp(a2))
    a3 = ease_out_cubic(prog(t, 1.2, 0.7))
    put(base, text_layer('Réponds en commentaire  ·  @GTA6HUBFR_', 52, WHITE, 'BarlowCondensed-SemiBoldItalic.ttf'), W/2, 1630, alpha=a3)
    if e > 0: base.alpha_composite(Image.new('RGBA', (int(W * e), H), INK + (255,)), (W - int(W * e), 0))
    credit(base); return base

SC = [('open', s_open, 3.6)] + [(f'shot{i}', make_shot(i), 3.0) for i in range(3)] + [('end', s_end, 3.6)]
if __name__ == '__main__':
    out = '/home/claude/rockstar/sortie'; os.makedirs(out, exist_ok=True)
    if sys.argv[1] == 'stills':
        for n, f, d in SC:
            f(d * 0.7, d).convert('RGB').resize((360, 640)).save(f'{out}/st_{n}.jpg')
    else:
        for n, f, d in SC: render_scene(n, f, d, out)
        assemble([n for n, _, _ in SC], out, '/home/claude/gta6hubfr_cest_sorti.mp4')

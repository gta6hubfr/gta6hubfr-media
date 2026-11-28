import os, sys, subprocess
sys.path.insert(0, '/home/claude/rockstar')
from leonida import *   # helpers: text_layer, put, yellow_box, ease_*, prog, header, credit, W, H, FPS, YEL, INK, WHITE
from PIL import Image, ImageDraw, ImageEnhance

LIB = '/home/claude/rockstar/lib/'

_full = {}
def full(name):
    """cover-crop a landscape screenshot into a 9:16 frame at 1.25x for Ken Burns."""
    if name in _full: return _full[name]
    im = Image.open(LIB + name + '.jpg').convert('RGB')
    BW, BH = int(W * 1.25), int(H * 1.25)
    s = max(BW / im.width, BH / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    _full[name] = im
    return im

def kenburns(name, p, zoom_in=True, pan=0.5):
    im = full(name)
    zf = 1.0 + 0.15 * (p if zoom_in else 1 - p)
    cw = int(1.25 * W / zf); ch = int(cw * H / W)
    span = im.width - cw
    cx = span * (pan + (p - 0.5) * 0.25)
    cx = max(0, min(span, cx)); cy = (im.height - ch) / 2
    return im.crop((int(cx), int(cy), int(cx) + cw, int(cy) + ch)).resize((W, H), Image.BILINEAR).convert('RGBA')

def bottom_fade(base, start=0.5, strength=235):
    g = Image.linear_gradient('L').resize((W, H))
    g = g.point(lambda v: 0 if v < 255 * start else int((v - 255 * start) / (255 * (1 - start)) * strength))
    shade = Image.new('RGBA', (W, H), INK + (0,)); shade.putalpha(g)
    base.alpha_composite(shade)

def top_fade(base, h=360, strength=170):
    g = Image.linear_gradient('L').resize((W, h)).transpose(Image.FLIP_TOP_BOTTOM)
    g = g.point(lambda v: int(v / 255 * strength))
    shade = Image.new('RGBA', (W, h), INK + (0,)); shade.putalpha(g)
    base.alpha_composite(shade, (0, 0))

def label(base, t, region, idx, total, delay=0.35):
    """lower third: yellow tick + region name in two offset layers + counter."""
    a = ease_out_cubic(prog(t, delay, 0.6)); b = ease_out_cubic(prog(t, delay + 0.15, 0.6))
    bar = int(140 * a)
    if bar > 0: base.alpha_composite(Image.new('RGBA', (bar, 10), YEL + (255,)), (90, 1395))
    sh = text_layer(region, 150, YEL); wt = text_layer(region, 150, WHITE)
    put(base, sh, 90 + 10 - (1 - b) * 500, 1500 + 10, 'lm', b)
    put(base, wt, 90 - (1 - a) * 700, 1500, 'lm', a)
    c = text_layer(f'{idx:02d} / {total:02d}', 46, (255, 255, 255, 190), 'BarlowCondensed-ExtraBoldItalic.ttf')
    put(base, c, 990, 1395, 'rm', a)

def render_scene(name, fn, dur, outdir, S=1.0):
    tmp = f'{outdir}/{name}.tmp.mp4'; final = f'{outdir}/{name}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for k in range(n): p.stdin.write(fn(k / FPS, dur).convert('RGB').tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, final)

def assemble(names, outdir, final):
    with open(f'{outdir}/list.txt', 'w') as f:
        for n in names: f.write(f"file '{n}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-i', f'{outdir}/list.txt', '-c', 'copy', f'{outdir}/v.tmp.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{outdir}/v.tmp.mp4', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', final + '.tmp.mp4'], check=True)
    os.replace(final + '.tmp.mp4', final)

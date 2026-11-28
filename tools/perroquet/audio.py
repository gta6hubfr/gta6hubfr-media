"""Bande-son : nappe synthwave discrète + effets (whoosh, pop, ka-ching, tick), mixée sous la voix."""
import json, wave, numpy as np
SR = 44100
VO = json.load(open('/home/claude/pq/vo.json')); END = VO[-1]['start'] + VO[-1]['dur'] + 0.9
N = int(END * SR); t = np.arange(N) / SR
rng = np.random.default_rng(7)

def env_adsr(n, a=0.01, d=0.1, s=0.6, r=0.2):
    e = np.ones(n) * s; A = min(n, int(a * SR)); D = min(n - A, int(d * SR)); R = min(n, int(r * SR))
    e[:A] = np.linspace(0, 1, A); e[A:A + D] = np.linspace(1, s, D)
    if R > 0: e[n - R:] *= np.linspace(1, 0, R)
    return e
def saw(f, tt): return 2 * ((tt * f) % 1) - 1
def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def lp_fast(x, cutoff):
    # FFT lowpass (rapide)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x))

# --- musique : 104 BPM, Am - F - C - G ---
BPM = 104; beat = 60 / BPM; bar = 4 * beat
chords = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
midi = lambda m: 440 * 2 ** ((m - 69) / 12)
music = np.zeros(N)
nb = int(END / bar) + 1
for b in range(nb):
    ch = chords[b % 4]; s0 = int(b * bar * SR); n = min(int(bar * SR), N - s0)
    if n <= 0: break
    tt = np.arange(n) / SR
    pad = sum(saw(midi(m), tt) + saw(midi(m) * 1.004, tt) for m in ch) / 6
    music[s0:s0 + n] += pad * env_adsr(n, 0.25, 0.4, 0.8, 0.5) * 0.35
    root = midi(ch[0] - 24)
    for e in range(8):  # basse en croches
        bs = s0 + int(e * beat / 2 * SR); bn = min(int(beat / 2 * SR * 0.9), N - bs)
        if bn <= 0: continue
        bt = np.arange(bn) / SR; music[bs:bs + bn] += (saw(root, bt) * 0.6 + np.sin(2 * np.pi * root * bt)) * env_adsr(bn, 0.005, 0.08, 0.5, 0.05) * 0.32
music = lp_fast(music, 1400)
# batterie
drum = np.zeros(N)
for k in range(int(END / beat) + 1):
    s0 = int(k * beat * SR)
    if s0 >= N: break
    n = min(int(0.25 * SR), N - s0); tt = np.arange(n) / SR
    f = 50 + 90 * np.exp(-tt * 30); drum[s0:s0 + n] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14) * 0.9
    if k % 2 == 1:  # clap/snare
        sn = rng.normal(0, 1, n) * np.exp(-tt * 22) * 0.35; drum[s0:s0 + n] += lp_fast(sn, 5000) if n > 64 else 0
    hs = int((k + 0.5) * beat * SR); hn = min(int(0.05 * SR), N - hs)
    if hn > 0: drum[hs:hs + hn] += np.diff(np.concatenate([[0], rng.normal(0, 1, hn)])) * np.exp(-np.arange(hn) / SR * 80) * 0.12
bed = music + drum
bed /= np.abs(bed).max() + 1e-9
fade = np.ones(N); fi = int(0.4 * SR); fo = int(1.2 * SR); fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
bed *= fade

# --- effets ---
fx = np.zeros(N)
def add(x, at, g=1.0):
    s0 = int(at * SR); n = min(len(x), N - s0)
    if n > 0: fx[s0:s0 + n] += x[:n] * g
def whoosh(d=0.35):
    n = int(d * SR); tt = np.arange(n) / SR; x = rng.normal(0, 1, n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X *= np.exp(-((f - 1800) / 1400) ** 2); x = np.fft.irfft(X, n)
    return x / np.abs(x).max() * np.sin(np.pi * tt / d) ** 2
def pop():
    n = int(0.09 * SR); tt = np.arange(n) / SR; f = 900 - 500 * tt / 0.09
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45)
def kaching():
    n = int(0.9 * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for f0, dl in [(2093, 0), (2637, 0.06), (3136, 0.12), (4186, 0.12)]:
        s0 = int(dl * SR); u = tt[:n - s0]; x[s0:] += np.sin(2 * np.pi * f0 * u) * np.exp(-u * 5) * 0.4
    k = int(0.05 * SR); x[:k] += rng.normal(0, 1, k) * np.exp(-np.arange(k) / SR * 90) * 0.5
    return x
def tick():
    n = int(0.04 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * 1500 * tt) * np.exp(-tt * 120)

S = [s['start'] for s in VO]
def w(seg, i): return VO[seg]['words'][i]['s']
for k in range(1, len(S)): add(whoosh(), S[k] - 0.12, 0.35)
add(pop(), 0.15, 0.5); add(kaching(), w(0, 7) + 0.9, 0.55)
for seg, at in [(1, 0.5), (2, 0.45), (3, 0.2), (4, 0.9), (5, 0.4)]: add(pop(), S[seg] + at, 0.5)
for x in (0.55, 1.45, 2.25, 3.0): add(tick(), S[3] + x, 0.6)
add(kaching(), w(5, 10) + 0.85, 0.6); add(kaching(), w(6, 5) + 0.85, 0.6)
add(kaching(), w(7, 1) + 1.15, 0.7); add(pop(), w(7, 6), 0.5)

def save(name, x):
    x = np.clip(x, -1, 1)
    with wave.open(name, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((x * 32767).astype(np.int16).tobytes())
save('/home/claude/pq/bed.wav', bed * 0.8); save('/home/claude/pq/fx.wav', fx * 0.8)
print('ok', round(END, 2))

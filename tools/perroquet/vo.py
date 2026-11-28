"""Voix off Piper « tom » : une ligne par segment + timing mot par mot (au prorata des phonèmes, recalé sur les pauses)."""
import json, wave, sys, re
import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

LINES = json.load(open('/home/claude/pq/lines.json'))
v = PiperVoice.load('/home/claude/tts/tom/fr_FR-tom-medium.onnx', config_path='/home/claude/tts/tom/fr_FR-tom-medium.onnx.json')
SR = v.config.sample_rate
cfg = SynthesisConfig(length_scale=float(sys.argv[1]) if len(sys.argv) > 1 else 0.9, noise_scale=0.55, noise_w_scale=0.7)
GAP = 0.22
out = []; meta = []; t = 0.0
for i, L in enumerate(LINES):
    say = L['say']
    sents = []
    for ch in v.synthesize(say, syn_config=cfg):
        sents.append((ch.audio_float_array.astype(np.float32), ch.phonemes))
    # concat sentences with a short breath
    raw = L['show'].split(); words_disp = []
    for tok in raw:
        base = tok.split('~')[0]
        if words_disp and re.fullmatch(r'[!?:;»]+', base): words_disp[-1] = words_disp[-1].split('~')[0] + '_' + base + ('~' + words_disp[-1].split('~')[1] if '~' in words_disp[-1] else '')
        else: words_disp.append(tok)
    fixed = []; carry = ''
    for tok in words_disp:
        if tok == '«': carry = '«_'; continue
        fixed.append(carry + tok); carry = ''
    words_disp = fixed
    audio = []; ph_all = []
    for a, ph in sents:
        thr = 0.012 * np.abs(a).max(); idx = np.where(np.abs(a) > thr)[0]
        a = a[max(0, idx[0] - int(.01 * SR)): idx[-1] + int(.03 * SR)]
        audio += [a, np.zeros(int(0.12 * SR), np.float32)]
    x = np.concatenate(audio[:-1]) if len(audio) > 1 else audio[0]
    dur = len(x) / SR
    # word timing: proportional to letters (vowel-weighted), snapped to energy dips
    def wt(s):
        sp = s.split('~')[1] if '~' in s else s
        return max(1.0, len(re.sub(r'[^A-Za-zÀ-ÿ0-9]', '', sp)) + (2.5 if re.search(r'[,.!?:]$', s.split('~')[0]) else 0))
    w = [wt(s) for s in words_disp]
    tot = sum(w); env = np.convolve(np.abs(x), np.ones(int(.02 * SR)) / int(.02 * SR), 'same')
    bounds = [0.0]; acc = 0
    for k in range(len(w) - 1):
        acc += w[k]; guess = acc / tot * dur
        a0, a1 = int(max(0, guess - .09) * SR), int(min(dur, guess + .09) * SR)
        if a1 > a0: guess = (a0 + int(np.argmin(env[a0:a1]))) / SR
        bounds.append(max(guess, bounds[-1] + 0.08))
    bounds.append(dur)
    words = [{'w': words_disp[k].split('~')[0].replace('_', ' '), 's': round(t + bounds[k], 3), 'e': round(t + bounds[k + 1], 3)} for k in range(len(words_disp))]
    meta.append({'i': i, 'start': round(t, 3), 'dur': round(dur, 3), 'words': words})
    out += [x, np.zeros(int(GAP * SR), np.float32)]; t += dur + GAP
y = np.concatenate(out); y = y / max(1e-6, np.abs(y).max()) * 0.9
with wave.open('/home/claude/pq/vo_raw.wav', 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((y * 32767).astype(np.int16).tobytes())
json.dump(meta, open('/home/claude/pq/vo.json', 'w'), ensure_ascii=False, indent=1)
for m in meta: print(m['i'], m['start'], m['dur'])
print('TOTAL', round(t, 2))

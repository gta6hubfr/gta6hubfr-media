import sys, json, wave, io, numpy as np, soundfile as sf
from piper import PiperVoice
from piper.config import SynthesisConfig
m, sid, ls, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
import glob; d=f'/home/claude/tts/{m}'; onnx=glob.glob(d+'/*.onnx')[0]
v=PiperVoice.load(onnx, config_path=onnx+'.json')
L=json.load(open('/home/claude/tts/vo3/lines.json')); outa=[];meta=[];t=0;gap=0.12
for i,s in enumerate(L):
    cfg=SynthesisConfig(speaker_id=sid if v.config.num_speakers>1 else None, length_scale=ls)
    x=np.concatenate([c.audio_float_array for c in v.synthesize(s, syn_config=cfg)]).astype(np.float32); sr=v.config.sample_rate
    thr=0.01*np.abs(x).max(); idx=np.where(np.abs(x)>thr)[0]; x=x[max(0,idx[0]-int(.01*sr)):idx[-1]+int(.02*sr)]
    meta.append({'i':i,'start':t,'dur':len(x)/sr}); outa+=[x,np.zeros(int(gap*sr),np.float32)]; t+=len(x)/sr+gap
sf.write(out+'.wav',np.concatenate(outa),sr); json.dump(meta,open(out+'.json','w')); print(out,round(t,2))

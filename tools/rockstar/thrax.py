import sys, json; sys.path.insert(0,'/home/claude/rockstar')
import rares2
rares2.SRC='/home/claude/opus/mogi/thrax.mp4'
rares2.CRED1='Gameplay : Mogi (YouTube)  ·  Infos : GTA-Xtreme, TheBestMods'
from rares2 import *
C1b=text_layer(rares2.CRED1,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
OUT='/home/claude/rockstar/thrax'+('_nocap' if os.environ.get('NOCAP')=='1' else ''); os.makedirs(OUT,exist_ok=True)
VOICE=os.environ.get('VOICE','free'); META=json.load(open('/home/claude/tts/vo3/'+('meta' if VOICE=='free' else VOICE)+'.json')); TXT=json.load(open('/home/claude/tts/vo3/lines.json'))
TOTAL=META[-1]['start']+META[-1]['dur']+0.7
def span(i): return (META[i+1]['start'] if i+1<len(META) else TOTAL)-META[i]['start']
def chunks(i):
    w=TXT[i].replace(' ?',' ?').replace(' !',' !').replace(' :',' :').split(' ')
    out=[];cur=[]
    for x in w:
        if cur and (len(cur)>=2 or len(' '.join(cur+[x]))>14): out.append(' '.join(cur)); cur=[]
        cur.append(x)
    if cur: out.append(' '.join(cur))
    tot=sum(len(c) for c in out); t=0; res=[]
    for c in out: d=META[i]['dur']*len(c)/tot; res.append((t,t+d,c)); t+=d
    return res
CAPF='BarlowCondensed-BlackItalic.ttf'
def cap(s): return text_layer(s.upper(),92,WHITE,CAPF,stroke=9,stroke_fill=(0,0,0))
M=MAP(240,95,1200,900,640)
SC=[ # shots, chip, top lines
 ([(16.6,2.6,CAR(700,580)),(32.5,span(0)-2.6,CAR(528,580))],'ALERTE BON PLAN',
   [(text_layer('UNE BUGATTI',120,WHITE),300,None),(grad_text('GRATUITE',190),462,None),(B('dans GTA 6, sans attendre le chapitre 3',54),600,None)]),
 ([(12.3,span(1),M)],'OÙ LA TROUVER',
   [(pin('BOONE SPEEDWAY'),300,0),(B('Hamlet · entre par le sud',54),410,0.2)]),
 ([(0.2,2.7,CAR(500,580)),(9.5,span(2)-2.7,CAR(500,580))],'ÉTAPE 1',
   [(grad_text('LE CAMION-PLATEAU',112),330,0),(B("à l'entrée du circuit",54),460,0.15)]),
 ([(24.6,2.5,CAR(400,580)),(3.3,span(3)-2.5,CAR(500,580))],'PAS LÀ ?',
   [(grad_text('REVIENS PLUS TARD',112),330,0),(B('elle finit par réapparaître',54),460,0.15)]),
 ([(21.5,1.45,CAR(500,580)),(27.2,2.65,CAR(560,580)),(30.45,span(4)-4.1,CAR(560,580))],'ATTENTION',
   [(grad_text('TRACEUR',150),330,0),(B('Scanne-la avec WAiNK, puis file vite',52),462,0.15)]),
 ([(36.0,span(5),CAR(528,580))],'PARTIE 2 ?',
   [(text_layer('UNE 2E THRAX',112,WHITE),300,0),(grad_text('SANS TRACEUR',150),455,0.1),(B('à Starfish Island · abonne-toi pour la suite',48,YEL),590,0.3)]),
]
def build(i):
    shots,lab,lines=SC[i]; fr=frames(shots); n=int(round(span(i)*30)); fr=(fr+[fr[-1]]*n)[:n]
    L=chip(lab,RED,size=38); caps=[(a,b,cap(c)) for a,b,c in chunks(i)]
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,720,235)
        b.alpha_composite(BADGE,(60,60)); put(b,L,W/2,102)
        kit2.bottom_fade(b,0.16,200); put(b,C1b,W/2,1838); put(b,C2,W/2,1874)
        for Lx,y,st in lines:
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.35)))
            put(b,Lx,W/2+(1-a)*500,y,alpha=a)
        for a0,b0,c in (caps if os.environ.get('NOCAP')!='1' else []):
            if a0<=t<b0:
                s=1+0.12*(1-clamp(prog(t,a0,0.08))); cl=c.resize((int(c.width*s),int(c.height*s))) if s>1.001 else c
                put(b,cl,W/2,1180); break
        return b
    encode(f't{i}',gen,n,OUT)
if __name__=='__main__':
    todo=[int(x) for x in sys.argv[1:]] or range(len(SC))
    for i in todo: build(i)
    assemble([f't{i}' for i in range(len(SC))],OUT,OUT+'/video.mp4')
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',OUT+'/video.mp4','-i','/home/claude/tts/vo3/'+VOICE+'.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-15:TP=-1.5:LRA=11,apad','-shortest','/home/claude/gta6hubfr_bugatti_gratuite.mp4'],check=True)

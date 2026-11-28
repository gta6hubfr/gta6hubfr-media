import sys, json; sys.path.insert(0,'/home/claude/rockstar')
import rares2
rares2.SRC='/home/claude/opus/nf/nf.mp4'
rares2.CRED1='Gameplay : « Free Blue Bugatti From No Flusher » (YouTube)  ·  Infos : GameSpot, GTABase'
from rares2 import *
C1b=text_layer(rares2.CRED1,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
OUT='/home/claude/rockstar/thrax2'; os.makedirs(OUT,exist_ok=True)
VOICE='tom'; META=json.load(open('/home/claude/tts/vo4/tom.json')); TXT=json.load(open('/home/claude/tts/vo4/lines.json'))
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
M=MAP(180,100,1200,900,640)
CARB=lambda x,py=580: CAR(x,py).replace(rares2.LOOK,rares2.LOOK+',eq=gamma=1.35:brightness=0.03')
SC=[
 ([(414.5,1.9,CAR(480,580)),(494.0,span(0)-1.9,CAR(460,580))],'BUGATTI GRATUITE · PARTIE 2',
   [(text_layer('LA 2E BUGATTI',116,WHITE),300,None),(grad_text('GRATUITE',190),462,None),(B('sans traceur : tu la gardes pour toujours',52),600,None)]),
 ([(250.6,span(1),CAR(800,580))],'ÉTAPE 1',
   [(grad_text('LE MESSAGE DE CAL',108),330,0),(B('il arrive au chapitre 3',54),460,0.15)]),
 ([(118.0,2.0,CARB(560)),(124.6,span(2)-2.0,CARB(560))],'ÉTAPE 2',
   [(grad_text('10 TAGS BLEUS',130),330,0),(B('à scanner avec WAiNK, à Vice Beach',54),462,0.15)]),
 ([(278.6,2.6,CAR(520,580)),(289.5,span(3)-2.6,CAR(500,580))],'ÉTAPE 3',
   [(grad_text('CODE : 8554013',130),330,0),(B('la porte de leur planque, à Ocean Beach',52),462,0.15)]),
 ([(351.0,1.9,CAR(700,580)),(373.5,span(4)-1.9,M)],'ÉTAPE 4',
   [(grad_text('STARFISH ISLAND',120),330,0),(B("l'adresse d'Andrew Node",54),462,0.15)]),
 ([(386.0,1.8,CAR(450,580)),(440.0,span(5)-1.8,CAR(700,580))],'ÉTAPE 5',
   [(grad_text('SON GARAGE',140),330,0),(B("pas de traceur, pas d'alarme",54),462,0.15)]),
 ([(470.0,2.2,CAR(500,580)),(488.0,span(6)-2.2,CAR(460,580))],'À TOI',
   [(text_layer('ELLE EST À TOI',112,WHITE),300,0),(grad_text('ENREGISTRE',170),455,0.1),(B('la vidéo pour ta prochaine partie',50,YEL),590,0.3)]),
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
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',OUT+'/video.mp4','-i','/home/claude/tts/vo4/tom.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-15:TP=-1.5:LRA=11,apad','-shortest','/home/claude/gta6hubfr_bugatti_gratuite_2.mp4'],check=True)

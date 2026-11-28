import sys, json; sys.path.insert(0,'/home/claude/rockstar')
import rares2
rares2.SRC='/home/claude/opus/jet/jet.mp4'
rares2.CRED1='Gameplay : CookAgain (YouTube)  ·  Infos : PC Gamer, Beebom'
from rares2 import *
C1b=text_layer(rares2.CRED1,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
OUT='/home/claude/rockstar/jet'; os.makedirs(OUT,exist_ok=True)
VOICE='tom'; META=json.load(open('/home/claude/tts/vo6/tom.json')); TXT=json.load(open('/home/claude/tts/vo6/lines.json'))
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
CARp=lambda x: PANEL(x,0,864,1080,560)
WIDE=lambda x: PANEL(x,0,1100,1080,600)
MZ=PANEL(240,0,1440,1080,560)
MK=PANEL(240,220,1440,860,620)
SC=[
 ([(0.0,1.6,WIDE(580)),(3.85,span(0)-1.6,CARp(528))],'GRATUIT',
   [(text_layer('AVION DE CHASSE',100,WHITE),300,None),(grad_text('+ TANK',180),455,None),(B('gratuits dans GTA 6, dès le début',54),595,None)]),
 ([(6.5,2.0,MZ),(39.5-(span(1)-2.0),span(1)-2.0,CARp(528))],'OÙ ALLER',
   [(pin('MILE ZERO AIR STATION'),300,0),(B('la base militaire, tout au sud',54),410,0.2)]),
 ([(39.5,span(2),WIDE(410))],'ÉTAPE 1',
   [(grad_text('SAUTE LA CLÔTURE',120),330,0),(B('grâce à la butte de terre',54),462,0.15)]),
 ([(39.5+span(2),0.93,WIDE(410)),(15.25,span(3)-0.93,PANEL(240,300,1440,780,620))],'LE TANK',
   [(grad_text('RHINO',170),330,0),(B('garé juste à côté',54),470,0.15)]),
 ([(63.6,span(4),CARp(528))],'LE TANK',
   [(grad_text('RHINO',170),330,None),(B('pulvérise tout',54),470,0.0)]),
 ([(76.2,span(5),CARp(528))],'LE JET',
   [(grad_text('HYDRAVION',150),330,0),(B('pose-toi sur la piste et saute',54),462,0.15)]),
 ([(12.15,0.85,MK),(90.0,span(6)-0.85,CARp(528))],'LE JET',
   [(grad_text('P-996 LAZER',130),330,0),(B('décolle direct',54),462,0.15)]),
 ([(93.3,span(7),WIDE(410))],'À TOI',
   [(text_layer('JET OU TANK ?',120,WHITE),300,0),(grad_text('COMMENTE',170),455,0.1),(B('et abonne-toi pour la suite',50,YEL),590,0.3)]),
]
OV={3:(pin('TANK ICI',56),0.93,span(3),715),6:(pin('JET ICI',56),0,0.85,775)}
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
        if i in OV:
            P,o0,o1,oy=OV[i]
            if o0<=t<o1:
                a=clamp(ease_out_back(prog(t,o0,0.25))); put(b,P,W/2,oy-(1-a)*40,alpha=min(1,a))
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
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',OUT+'/video.mp4','-i','/home/claude/tts/vo6/tom.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-15:TP=-1.5:LRA=11,apad','-shortest','/home/claude/gta6hubfr_jet_tank.mp4'],check=True)

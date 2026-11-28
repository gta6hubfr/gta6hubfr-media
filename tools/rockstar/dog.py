import sys, json; sys.path.insert(0,'/home/claude/rockstar')
import rares2
rares2.SRC='/home/claude/opus/dog/dog.mp4'
rares2.CRED1='Gameplay : « Secret Jet Ski Dog Location » (YouTube)  ·  Infos : Insider Gaming, Gfinity'
from rares2 import *
C1b=text_layer(rares2.CRED1,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
OUT='/home/claude/rockstar/dog'; os.makedirs(OUT,exist_ok=True)
VOICE='tom'; META=json.load(open('/home/claude/tts/vo7/tom.json')); TXT=json.load(open('/home/claude/tts/vo7/lines.json'))
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
MZ=PANEL(240,0,1440,1080,560)
SC=[
 ([(38.9,1.2,CARp(560)),(42.85,span(0)-1.2,CARp(260))],'SECRET',
   [(text_layer('UN CHIEN EN JET-SKI',96,WHITE),300,None),(grad_text('TE SAUVE',170),455,None),(B('caché dans GTA 6',54),595,None)]),
 ([(10.2,1.2,MZ),(13.0,span(1)-1.2,CARp(560))],'OÙ ALLER',
   [(pin('GAMBIT BAY'),300,0),(B("saute à l'eau, loin des bateaux",54),410,0.2)]),
 ([(27.4,span(2),CARp(528))],'ATTENDS',
   [(grad_text('± 5 MIN',170),330,0),(B('écoute les aboiements',54),470,0.15)]),
 ([(33.6,span(3)-1.9,CARp(560)),(37.0,1.9,CARp(560))],'MONTE',
   [(grad_text('NE DESCENDS PAS',112),330,0),(B("reste jusqu'au bout",54),462,0.15)]),
 ([(48.3,span(4),CARp(528))],'DESTINATION',
   [(grad_text("L'ÎLE AUX CHIENS",110),330,0),(B('aucun repère sur la carte',54),462,0.15)]),
 ([(69.6,span(5),CARp(300))],'BONUS',
   [(grad_text('+1 200 $',180),330,0),(B('gratuits, dès le début',54),470,0.15)]),
 ([(57.0,span(6),CARp(528))],'À TOI',
   [(text_layer("TU L'AVAIS VU ?",110,WHITE),300,0),(grad_text('COMMENTE',170),455,0.1),(B('et envoie-la à un pote',50,YEL),590,0.3)]),
]
OV={}
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
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',OUT+'/video.mp4','-i','/home/claude/tts/vo7/tom.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-15:TP=-1.5:LRA=11,apad','-shortest','/home/claude/gta6hubfr_cool_dog.mp4'],check=True)

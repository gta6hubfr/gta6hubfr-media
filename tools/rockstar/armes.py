import sys, json; sys.path.insert(0,'/home/claude/rockstar')
import rares2
rares2.SRC='/home/claude/opus/armes/armes.mp4'
rares2.CRED1='Gameplay : « 2 SECRET Legendary Weapons EARLY in GTA 6 » (YouTube)  ·  Infos : GTA BOOM, Sportskeeda'
from rares2 import *
C1b=text_layer(rares2.CRED1,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
OUT='/home/claude/rockstar/armes'; os.makedirs(OUT,exist_ok=True)
VOICE='tom'; META=json.load(open('/home/claude/tts/vo5/tom.json')); TXT=json.load(open('/home/claude/tts/vo5/lines.json'))
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
TOP=lambda x: PANEL(x,0,664,830,580)
BOX=lambda x: PANEL(x,52,618,766,580)
MB=lambda x: PANEL(x,52,1024,766,640)
SC=[
 ([(49.9,1.85,TOP(300)),(70.1,span(0)-1.85,BOX(550))],'ARMES GRATUITES',
   [(text_layer('2 ARMES LÉGENDAIRES',100,WHITE),300,None),(grad_text('GRATUITES',180),455,None),(B('dans GTA 6, dès le chapitre 1',54),595,None)]),
 ([(9.3,span(1),MB(480))],'OÙ ALLER',
   [(pin('PERMIT KEYS'),300,0),(B('tout au sud, près de Mile Zero',54),410,0.2)]),
 ([(21.15,1.9,TOP(430)),(43.0,span(2)-1.9,TOP(440))],'ARME N°1',
   [(grad_text("L'ÉPAVE",150),330,0),(B('ouvre la trappe dans le plancher',54),462,0.15)]),
 ([(44.4,1.5,TOP(440)),(47.95,span(3)-1.5,TOP(300))],'ARME N°1',
   [(grad_text('ASSASSIN NIPPER',112),330,0),(B('pistolet avec silencieux intégré',54),462,0.15)]),
 ([(53.0,span(4),MB(480))],'ARME N°2',
   [(pin('ÎLE LA PLUS AU NORD'),300,0),(B('toujours dans les Permit Keys',54),410,0.2)]),
 ([(65.0,span(5),BOX(600))],'ARME N°2',
   [(grad_text('SMUGGLER GORSE',112),330,0),(B('fusil à pompe, posé sur le sable',54),462,0.15)]),
 ([(61.0,3.7,BOX(620))],'À TOI',
   [(text_layer('0 $ DÉPENSÉ',120,WHITE),300,0),(grad_text('ENREGISTRE',170),455,0.1),(B('la vidéo pour ta prochaine partie',50,YEL),590,0.3)]),
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
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',OUT+'/video.mp4','-i','/home/claude/tts/vo5/tom.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-15:TP=-1.5:LRA=11,apad','-shortest','/home/claude/gta6hubfr_armes_legendaires.mp4'],check=True)

import sys, subprocess, re, json; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os
SRC='/home/claude/opus/rares/rares.mp4'
OUT='/home/claude/rockstar/vorares'; os.makedirs(OUT,exist_ok=True)
META=json.load(open(sys.argv[1] if len(sys.argv)>1 and sys.argv[1].endswith('.json') else '/home/claude/tts/vo2/meta.json'))
TEXTS=json.load(open('/home/claude/tts/vo2/lines.json'))
COVER=lambda cx=656: f'fps=30,crop=608:1080:{cx}:0,scale=1080:1920:flags=lanczos'
def PANEL(x,y,w,h,py=700,pw=1080):
    return (f'fps=30,split[a][b];[a]crop=608:1080:656:0,scale=1080:1920,boxblur=24:2,eq=brightness=-0.25[bg];'
            f'[b]crop={w}:{h}:{x}:{y},scale={pw}:-2:flags=lanczos[fg];[bg][fg]overlay={(1080-pw)//2}:{py}')
O=25  # la plage OpusClip commence à 0:25 de la vidéo source
# plans : (temps dans la vidéo source, filtre) ; la durée est donnée par la voix
SHOTS=[
 [(90.0,COVER())],
 [(50.7,COVER())],
 [(38.5,PANEL(300,250,1400,750)),(65.6,COVER())],
 [(47.4,COVER())],
 [(140.4,COVER()),(165.6,COVER())],
 [(155.4,PANEL(200,240,1500,800)),(160.4,COVER())],
 [(158.0,PANEL(1040,160,800,840,660,760))],
 [(280.0,COVER())],
 [(297.0,COVER(450))],
 [(259.8,COVER())],
 [(399.4,COVER())],
 [(425.7,COVER())],
 [(429.4,COVER())],
]
SPLIT={2:2.4,4:2.95,5:1.6}   # durée du 1er plan quand une ligne a 2 plans
TITLES={0:('VOITURES GRATUITES',None,'5 VÉHICULES RARES','GRATUITS',None),
 1:('VÉHICULE N°1','1 / 5','ROYAL RUBY','EMERUS','Hypercar + nitro'),
 4:('VÉHICULE N°2','2 / 5','CHARRED','TOROS','Le SUV jaune et noir'),
 7:('VÉHICULE N°3','3 / 5','DRIFTER','ELEGY','La reine du drift'),
 9:('VÉHICULE N°4','4 / 5','BRIMSTONE','GOLFER','La voiturette en flammes'),
 10:('VÉHICULE N°5','5 / 5','PENUMBRA FF',"L'ECLIPSE",'de Paul Walker'),
 12:('À TOI',None,'LAQUELLE','EN PREMIER ?',None)}
TAIL=0.5
CRED='Gameplay : WiLLiSGaming (YouTube)  ·  Infos : DETONATED, KeenGamer, Screen Hype  ·  Page fan, non officielle'
B=lambda s,z=54,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
def words():
    out=[]
    for li,m in enumerate(META):
        s,d=m['start'],m['dur']; toks=TEXTS[li].replace('GTA 6','GTA 6').split(' ')
        ws=[(len(re.sub(r'[^\wÀ-ÿ\']','',t))+1.5, 2.5 if t[-1]==',' else (4 if t[-1] in '.:;?!' else 0)) for t in toks]
        tot=sum(a+p for a,p in ws)-ws[-1][1]; a,b=s+0.03,s+d-0.05; t=a
        for tok,(x,p) in zip(toks,ws): out.append([tok,t,li]); t+=(b-a)*(x+p)/tot
    return out
def chunks():
    ws=words(); res=[]; i=0
    while i<len(ws):
        tok,t,li=ws[i]; grp=[tok]; j=i+1
        while j<len(ws) and len(grp)<2 and ws[j][2]==li and tok[-1] not in '.,:;!?' and len(' '.join(grp+[ws[j][0]]))<=14:
            grp.append(ws[j][0]); tok=ws[j][0]; j+=1
        res.append((' '.join(grp),t)); i=j
    end=META[-1]['start']+META[-1]['dur']+TAIL
    return [(c,t,(res[k+1][1] if k+1<len(res) else end)) for k,(c,t) in enumerate(res)]
CH=chunks(); _c={}
def cap(txt):
    if txt not in _c:
        s=re.sub(r'[.,:;!?…]','',txt).upper().strip()
        _c[txt]=text_layer(s,104,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf',stroke=8,stroke_fill=(0,0,0,255))
    return _c[txt]
BADGE=Image.new('RGBA',(84,84),(0,0,0,0)); ImageDraw.Draw(BADGE).rounded_rectangle((0,0,83,83),16,fill=YEL)
_g=text_layer('G6',56,INK,'BarlowCondensed-ExtraBoldItalic.ttf'); BADGE.alpha_composite(_g,((84-_g.width)//2,(84-_g.height)//2-2))
C1=text_layer(CRED,25,(255,255,255,180),'BarlowCondensed-SemiBoldItalic.ttf')
def title_for(li):
    k=max(x for x in TITLES if x<=li); return k,TITLES[k]
_t={}
def title_layers(k):
    if k not in _t:
        lab,idx,l1,l2,sub=TITLES[k]
        _t[k]=(chip(lab,RED,size=38), text_layer(idx,36,(255,255,255,215),'BarlowCondensed-ExtraBoldItalic.ttf') if idx else None,
               text_layer(l1,112,WHITE), grad_text(l2,132), B(sub,56,YEL) if sub else None)
    return _t[k]
def frames(ss,dur,vf):
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss-O),'-t',str(dur+0.1),'-i',SRC,'-filter_complex',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]; n=round(dur*30)
    while len(out)<n:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close(); p.wait()
    while len(out)<n: out.append(out[-1])
    return out
def scene(li):
    s=META[li]['start']; e=META[li+1]['start'] if li+1<len(META) else META[li]['start']+META[li]['dur']+TAIL
    f0,f1=round(s*30),round(e*30); n=f1-f0
    sh=SHOTS[li]; fr=[]
    if len(sh)==1: fr=frames(sh[0][0],n/30,sh[0][1])
    else:
        n1=round(SPLIT[li]*30); fr=frames(sh[0][0],n1/30,sh[0][1])+frames(sh[1][0],(n-n1)/30,sh[1][1])
    k,_=title_for(li); L,I,T1,T2,SB=title_layers(k); t_in=META[k]['start']
    def gen(j):
        t=(f0+j)/30; b=fr[j].convert('RGBA'); kit2.top_fade(b,820,225)
        b.alpha_composite(BADGE,(60,60)); put(b,L,W/2,102)
        if I: put(b,I,1020,102,'rm')
        for lay,y,dl in ((T1,320,0),(T2,450,0.08),(SB,565,0.2)):
            if lay is None: continue
            a=clamp(ease_out_back(prog(t,t_in+dl,0.4))) if k>0 else 1
            put(b,lay,W/2+(1-a)*500,y,alpha=a)
        kit2.bottom_fade(b,0.9,200); put(b,C1,W/2,1868)
        for c,a0,a1 in CH:
            if a0<=t<a1:
                Lc=cap(c); sc=0.86+0.14*clamp(ease_out_back(prog(t,a0,0.12)))
                if sc<0.999: Lc=Lc.resize((max(1,int(Lc.width*sc)),max(1,int(Lc.height*sc))))
                put(b,Lc,W/2,1420)
        return b
    encode(f's{li:02d}',gen,n,OUT)
if __name__=='__main__':
    args=[a for a in sys.argv[1:] if not a.endswith('.json')]
    for li in ([int(a) for a in args] or range(len(META))): scene(li)

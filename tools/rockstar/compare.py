import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/comp/comp.mp4'; OUT='/home/claude/rockstar/compare'; os.makedirs(OUT,exist_ok=True)
LOOK='eq=contrast=1.08:saturation=1.15'
PW,PH=1080,790; YA,YB=320,1120
def grab(ss,dur,x,y,w,h):
    vf=f'fps=30,crop={w}:{h}:{x}:{y},scale={PW}:{PH}:flags=lanczos,{LOOK}'
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    fr=[]
    while len(fr)<round(dur*30):
        b=p.stdout.read(PW*PH*3)
        if len(b)<PW*PH*3: break
        fr.append(Image.frombytes('RGB',(PW,PH),b))
    p.stdout.close(); p.wait(); return fr
FULL=lambda x: (x,300,1013,741)
L5=lambda x: (x,300,960,702)          # left half (GTA 5) in split mode
R6=lambda x: (960+x,300,960,702)      # right half (GTA 6)
B=lambda s,z=54,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
from logo import badge; BADGE=badge(104)
def label(txt,bg,fg):
    t=B(txt,46,fg); w,h=t.width+40,t.height+16
    L=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(L).rounded_rectangle((0,0,w-1,h-1),12,fill=bg); L.alpha_composite(t,(20,8)); return L
LA=label('GTA 5 · 2013',(30,30,36,235),WHITE); LB=label('GTA 6 · 2026',YEL,INK)
CR=text_layer('Gameplay : Comparaholic (YouTube, PS5 Pro)  ·  Page fan, non officielle',26,(255,255,255,190),'BarlowCondensed-SemiBoldItalic.ttf')
EPS={
 1:('',[('EXPLOSION',(304.0,FULL(150)),(316.3,FULL(150)),4.2),('SAUT DE VOITURE',(554.6,FULL(450)),(566.6,FULL(400)),4.2),("TIR DANS L'EAU",(196.8,L5(0)),(196.8,R6(0)),4.2),('BAIGNADE',(151.4,L5(0)),(151.4,R6(0)),4.2)]),
 2:("L'EAU",[('PLONGEON',(103.0,FULL(453)),(111.0,FULL(453)),4.2),('ENTRER DANS LA MER',(139.5,L5(0)),(139.5,R6(0)),4.2),('NAGE',(158.5,L5(0)),(158.5,R6(0)),4.2),("SOUS L'EAU",(176.5,FULL(453)),(182.5,FULL(453)),4.2)]),
 3:('BAGARRES & POLICE',[('BAGARRE',(235.0,FULL(453)),(282.0,FULL(453)),4.2),('COUP DE POING',(266.5,FULL(453)),(250.5,FULL(453)),4.2),('ARRESTATION',(340.5,FULL(453)),(367.0,FULL(453)),4.2),('ARRÊTÉ EN VOITURE',(386.0,FULL(453)),(399.6,FULL(453)),4.2)]),
 4:('LES DÉCORS',[('LA PLAGE',(433.0,FULL(453)),(440.0,FULL(453)),4.2),('COUCHER DE SOLEIL',(467.0,FULL(453)),(474.5,FULL(453)),4.2),('LA VILLE',(481.5,FULL(453)),(489.0,FULL(453)),4.2),('LA VILLE DE NUIT',(531.0,FULL(453)),(538.0,FULL(453)),4.2)]),
 5:('CHUTES & CASCADES',[('CHUTE À MOTO',(576.0,FULL(453)),(586.0,FULL(453)),4.2),("CHUTE D'UN IMMEUBLE",(14.0,FULL(453)),(28.5,FULL(453)),4.2),("SAUT D'HÉLICO",(39.0,FULL(453)),(68.0,FULL(453)),4.2),('PARACHUTE',(50.5,FULL(453)),(76.0,FULL(453)),4.2)]),
}
EP=int(os.environ.get('EP','1')); THEME,TESTS=EPS[EP]
OUT=OUT+(f'_ep{EP}' if EP>1 else ''); os.makedirs(OUT,exist_ok=True)
HOLD=1.8
def build(i):
    name,(s5,c5),(s6,c6),d=TESTS[i]
    A=grab(s5,d,*c5); Bf=grab(s6,d,*c6); n=min(len(A),len(Bf))
    last=(i==len(TESTS)-1); N=n+(int(HOLD*30) if last else 0)
    T=grad_text(name,118 if len(name)<12 else (100 if len(name)<17 else 88)); C=chip((f'GTA 5 VS GTA 6 · ÉP. {EP} · ' if EP>1 else 'GTA 5 VS GTA 6 · ')+f'TEST {i+1}/4',RED,size=34 if EP>1 else 36)
    H0=text_layer('GTA 5 VS GTA 6',100,WHITE) if i==0 else None
    Q1=text_layer('LE PLUS GROS ÉCART ?',92,WHITE); Q2=B('1, 2, 3 ou 4 : dis-le en commentaire',50,YEL)
    def gen(k):
        t=k/30; b=Image.new('RGBA',(W,H),(12,12,16,255))
        b.paste(A[min(k,n-1)],(0,YA)); b.paste(Bf[min(k,n-1)],(0,YB))
        d_=ImageDraw.Draw(b); d_.rectangle((0,YA+PH,W,YB),fill=YEL)
        put(b,LA,40+LA.width/2,YA+48); put(b,LB,40+LB.width/2,YB+48)
        kit2.bottom_fade(b,0.08,200); put(b,CR,W/2,1888)
        b.alpha_composite(BADGE,(40,28)); put(b,C,W/2+40,82)
        q=last and t>d-0.6
        if i==0 and t<1.6: put(b,H0,W/2,205)
        elif q:
            a=clamp(ease_out_back(prog(t,d-0.6,0.35))); put(b,Q1,W/2,190,alpha=a); put(b,Q2,W/2,272,alpha=a)
        else:
            a=clamp(ease_out_back(prog(t,1.6 if i==0 else 0,0.3))); put(b,T,W/2+(1-a)*500,205,alpha=a)
        return b
    encode(f'c{i}',gen,N,OUT)
if __name__=='__main__':
    todo=[int(x) for x in sys.argv[1:]] or range(len(TESTS))
    for i in todo: build(i)
    assemble([f'c{i}' for i in range(len(TESTS))],OUT,'/home/claude/gta6hubfr_gta5_vs_gta6'+(f'_ep{EP}' if EP>1 else '')+'.mp4')

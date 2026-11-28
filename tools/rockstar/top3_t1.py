import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, ease_in_cubic, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
S='/home/claude/opus/shorts/'
CROP={'mro':'crop=1080:1220:0:700,scale=1700:1920,crop=1080:1920:310:0','squanch':'crop=1080:1590:0:330,scale=1304:1920,crop=1080:1920:112:0','eggz':'crop=1080:1500:0:420,scale=1382:1920,crop=1080:1920:151:0'}
def frames(f,ss,dur):
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',S+f+'.mp4','-vf',CROP[f]+',fps=30','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait(); return out
B=lambda s,z=56,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
def seg(name,f,ss,dur,rank,who,desc,hook=False,outro=False):
    fr=frames(f,ss,dur); n=len(fr); D=n/30
    R=grad_text(f'#{rank}',230); WHO=B(f'Stunt : @{who}',58,YEL); DS=B(desc,54)
    cred=text_layer(f'Gameplay : @{who} (YouTube)  ·  Page fan, non officielle',28,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf')
    H1=text_layer('LES 3 STUNT JUMPS',120,WHITE); H2=grad_text('LES PLUS FOUS.',140); H3=B('Reste jusqu\'au n°1…',56)
    O1=text_layer('TON PRÉFÉRÉ :',120,WHITE); O2=grad_text('1, 2 OU 3 ?',150); O3=B('Abonne-toi @gta6hubfr_ pour la suite',52,YEL)
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,800,230)
        bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
        g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
        put(b,chip('TOP STUNTS GTA 6',RED,size=38),W/2,102)
        kit2.bottom_fade(b,0.9,190); put(b,cred,W/2,1860)
        if hook and t<2.2:
            put(b,H1,W/2,330); put(b,H2,W/2,470); put(b,H3,W/2,590)
        elif outro and t>D-2.3:
            a=clamp(ease_out_back(prog(t,D-2.3,0.4)))
            put(b,O1,W/2,330,alpha=a); put(b,O2,W/2+(1-a)*500,480,alpha=a); put(b,O3,W/2,610,alpha=a)
        else:
            t0=2.2 if hook else 0
            a=clamp(ease_out_back(prog(t,t0,0.45))); a2=clamp(ease_out_back(prog(t,t0+0.25,0.45)))
            put(b,R,W/2-(1-a)*400,360,alpha=a); put(b,WHO,W/2+(1-a2)*500,520,alpha=a2); put(b,DS,W/2+(1-a2)*500,600,alpha=a2)
        return b
    encode(name,gen,n,OUT)
OUT='/home/claude/rockstar/top3'; os.makedirs(OUT,exist_ok=True)
#seg('t3','squanch',20.5,9.4,3,'SquanchCommunitY','Au-dessus de la mer, depuis un pont cassé',hook=True)
#seg('t2','eggz',8.0,7.8,2,'EggzBennie','Le pick-up qui vole au-dessus de l\'eau')
seg('t1','mro',2.0,9.6,1,'ItssMrO','Le saut le plus fou de Vice City',outro=True)
assemble(['t3','t2','t1'],OUT,'/home/claude/gta6hubfr_top3_stunts.mp4')

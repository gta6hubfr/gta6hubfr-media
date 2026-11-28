import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/pol/jetcrash.mp4'
CRED='Gameplay : @GAMErHyNas (YouTube)  ·  Page fan, non officielle'
def frames(ss,dur,slow=1.0):
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-vf',f'scale=1080:1920,setpts={slow}*PTS,fps=30','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait(); return out
def scene(name,fr,lab,lines,col=RED,fg=WHITE):
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,760,225)
        bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
        g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
        put(b,chip(lab,col,fg,size=38),W/2,102)
        kit2.bottom_fade(b,0.9,190); put(b,text_layer(CRED,28,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1860)
        for L,y,st in lines:
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.4)))
            put(b,L,W/2+(1-a)*500,y,alpha=a)
        return b
    encode(name,gen,len(fr),OUT)
OUT='/home/claude/rockstar/jetski'; os.makedirs(OUT,exist_ok=True)
B=lambda s,z=60,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
scene('j1',frames(6.9,7.5),'FAIL DU JOUR',[(text_layer('JET SKI',170,WHITE),330,None),(grad_text('VS PONTON.',160),500,None),(B('Plein gaz vers le quai de Vice City…'),630,1.0),(grad_text('…AÏE.',150),760,5.3)])
scene('j2',frames(11.0,2.2,2.0),'REPLAY  ×0,5',[(text_layer('AU RALENTI',140,WHITE),340,0.0),(B('Le ponton n\'a pas bougé.'),480,0.8)],col=YEL,fg=INK)
scene('j3',frames(14.5,4.0),'FAIL DU JOUR',[(text_layer('IL FINIT',140,WHITE),330,0.0),(grad_text('À LA NAGE.',150),480,0.3),(B('Tu aurais fait mieux ? Dis-le en commentaire'),610,1.0),(B('ABONNE-TOI @GTA6HUBFR_',58,YEL),700,1.4)])
assemble(['j1','j2','j3'],OUT,'/home/claude/gta6hubfr_jetski_fail.mp4')

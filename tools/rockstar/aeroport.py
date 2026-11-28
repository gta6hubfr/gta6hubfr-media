import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_cubic, ease_out_back, ease_in_cubic, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/brut.mp4'
CRED='Gameplay : @Hazardous (YouTube)  ·  Page fan, non officielle'
def frames(ss,dur,slow=1.0):
    vf=f'crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setpts={slow}*PTS,fps=30'
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait(); return out
def common(b,lab,col=RED,fg=WHITE):
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    put(b,chip(lab,col,fg,size=38),W/2,102)
    kit2.bottom_fade(b,0.9,190); put(b,text_layer(CRED,28,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1860)
def scene(name,fr,lab,lines,col=RED,fg=WHITE,timed=None,dark=0):
    # lines: list of (layer, y, start)
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,760,225)
        if dark: b.alpha_composite(Image.new('RGBA',(W,H),INK+(dark,)))
        common(b,lab,col,fg)
        for L,y,st in lines:
            a=ease_out_back(prog(t,st,0.45)) if st is not None else 1
            put(b,L,W/2+(1-clamp(a))*500,y,alpha=clamp(a))
        return b
    encode(name,gen,len(fr),OUT)
OUT='/home/claude/rockstar/aeroport'; os.makedirs(OUT,exist_ok=True)
B=lambda s,z=60: text_layer(s,z,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf')
# 1 hook + approche (même plan continu 348.4-360.7)
fr=frames(354.6,6.0)
scene('a1',fr,'STUNT DU JOUR',[(text_layer('CE SAUT',150,WHITE),330,None),(grad_text('DEPUIS LE TOIT…',130),480,None),(B('Plein gaz sur le parking de l\'aéroport'),600,1.2)])
# 2 le saut complet (changement d'angle au décollage, puis vol + atterrissage dans un seul plan)
fr=frames(360.6,5.4)
scene('a2',fr,'STUNT DU JOUR',[(grad_text('…ET ÇA DÉCOLLE.',140),360,0.0)])
# 3 replay ralenti, prise 2 (plan continu 390.25-395.33)
fr=frames(390.3,4.0,2.0)
scene('a3',fr,'REPLAY  ×0,5',[(text_layer('AU RALENTI',140,WHITE),340,0.0),(B('La réception est parfaite'),480,1.0)],col=YEL,fg=INK)
# 4 bonus rampe au-dessus de l'eau (plan continu 84.37-95.63)
fr=frames(84.45,6.6)
scene('a4',fr,'BONUS',[(text_layer('ET CELLE-LÀ,',130,WHITE),330,0.0),(grad_text('TU LA PASSES ?',140),480,0.3)])
# 5 info + CTA sur la fin du même plan
fr=frames(343.0,4.5)
scene('a5',fr,'À SAVOIR',[(grad_text('130 STUNT JUMPS',140),330,0.0),(text_layer('+ 25 BASE JUMPS À TROUVER',80,WHITE),470,0.3),(B('Carte > Stunt Spots  ·  Source : Showgamer',44),570,0.6),(text_layer('ABONNE-TOI POUR LE GUIDE',64,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),680,1.2)],dark=60)
assemble(['a1','a2','a3','a4','a5'],OUT,'/home/claude/gta6hubfr_saut_aeroport.mp4')

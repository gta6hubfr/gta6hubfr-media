import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/shorts/drifty.mp4'
CRED='Gameplay : Drifty (YouTube)  ·  Page fan, non officielle'
def frames(ss,dur,slow=1.0):
    vf=f'crop=1080:1280:0:640,scale=1620:1920,crop=1080:1920:270:0,setpts={slow}*PTS,fps=30'
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait(); return out
B=lambda s,z=56,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
def scene(name,fr,lab,lines,col=RED,fg=WHITE):
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,800,235)
        bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
        g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
        put(b,chip(lab,col,fg,size=38),W/2,102)
        kit2.bottom_fade(b,0.9,190); put(b,text_layer(CRED,28,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1860)
        for L,y,st,en in lines:
            if en is not None and t>en: continue
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.35)))
            put(b,L,W/2+(1-a)*500,y,alpha=a)
        return b
    encode(name,gen,len(fr),OUT)
OUT='/home/claude/rockstar/pont'; os.makedirs(OUT,exist_ok=True)
scene('p1',frames(12.9,4.05),'STUNT DU JOUR',[(text_layer('LE PONT CASSÉ',140,WHITE),330,None,None),(grad_text('ÇA PASSE OU PAS ?',130),480,None,None),(B('Saut n°1 : plein gaz…'),600,1.2,None)])
scene('p2',frames(16.99,2.8),'SAUT N°1',[(text_layer('…AU-DESSUS',150,WHITE),340,None,1.4),(text_layer('DE L\'EAU',150,WHITE),480,None,1.4),(grad_text('ÇA PASSE.',180),360,1.4,None),(B('Réception sur l\'autre rive',56),520,1.6,None)])
scene('p3',frames(19.85,5.35),'SAUT N°2',[(text_layer('ENCORE PLUS LOIN',130,WHITE),330,0,3.3),(B('Deuxième pont cassé, même délire',56),470,0.3,3.3),(grad_text('VALIDÉ.',190),360,3.3,None),(B('Stunt jump réussi : 2 sur 130',56),520,3.5,None)])
scene('p4',frames(22.4,1.4,2.0),'REPLAY  ×0,5',[(text_layer('AU RALENTI',140,WHITE),330,0,None),(B('130 stunt jumps dans le jeu.',52),470,0.6,None),(B('Tu en es à combien ?',58,YEL),545,1.0,None)],col=YEL,fg=INK)
assemble(['p1','p2','p3','p4'],OUT,'/home/claude/gta6hubfr_pont_casse.mp4')

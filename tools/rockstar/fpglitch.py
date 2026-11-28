import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/fp/fp.mp4'
CRED='Glitch : Kackalack · Vidéo : oneboyler (YouTube)  ·  Page fan, non officielle'
def frames(ss,dur):
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-vf','crop=608:1080:656:0,scale=1080:1920:flags=lanczos,fps=30','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait(); return out
B=lambda s,z=56,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
def scene(name,fr,lab,lines):
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); ImageDraw.Draw(b).rectangle((0,0,W,370),fill=INK+(255,)); kit2.top_fade(b,900,245)
        bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
        g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
        put(b,chip(lab,RED,size=38),W/2,102)
        kit2.bottom_fade(b,0.9,200); put(b,text_layer(CRED,26,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1860)
        for L,y,st,en in lines:
            if en is not None and t>en: continue
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.4)))
            put(b,L,W/2+(1-a)*500,y,alpha=a)
        return b
    encode(name,gen,len(fr),OUT)
OUT='/home/claude/rockstar/fpglitch'; os.makedirs(OUT,exist_ok=True)
scene('g1',frames(73.0,3.2),'GLITCH DU JOUR',[(text_layer('GTA 6 EN VUE',130,WHITE),330,None,None),(grad_text('1ÈRE PERSONNE ?!',140),480,None,None),(B('Le glitch qui affole les joueurs'),610,None,None)])
scene('g2',frames(25.0,3.2),'LE GLITCH EN 3 ÉTAPES',[(grad_text('ÉTAPE 1',130),330,0,None),(B('Réglages manette : passe le pavé',58),470,0.2,None),(B('tactile de « Carte » à « Caméra »',58),545,0.2,None)])
scene('g3',frames(44.9,5.2),'LE GLITCH EN 3 ÉTAPES',[(grad_text('ÉTAPE 2',130),330,0,2.5),(B('Au volant, sors ton téléphone',58),470,0.2,2.5),(B('(haut sur la croix)',50),545,0.2,2.5),(grad_text('ÉTAPE 3',130),330,2.5,None),(B('Range-le (rond) et spamme',58),470,2.7,None),(B('le pavé tactile juste après',58),545,2.7,None)])
scene('g4',frames(76.0,5.0),'RÉSULTAT',[(text_layer('ET VOILÀ.',150,WHITE),330,0,2.8),(B('Xbox : B, puis spamme Back',52),470,0.3,2.8),(text_layer('TU VAS TESTER ?',120,WHITE),330,2.8,None),(B('Pas de vrai mode 1ère personne au lancement :',46),460,3.0,None),(B('ce glitch est la seule façon.',46),520,3.0,None),(B('ABONNE-TOI @GTA6HUBFR_',54,YEL),610,3.2,None)])
assemble(['g1','g2','g3','g4'],OUT,'/home/claude/gta6hubfr_glitch_1ere_personne.mp4')

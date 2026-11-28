import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/ps5/ps5_comet_s2.mp4'
CRED1='Gameplay : capture PS5 GTA6 Hub FR  ·  Infos : GTABase, GTABoom'
CRED2='Page fan, non officielle'
COVER=lambda cx: f'fps=30,crop=608:1080:{cx}:0,scale=1080:1920:flags=lanczos'
PANEL=lambda x,y,w,h,py: (f'fps=30,split[a][b];[a]crop=608:1080:656:0,scale=1080:1920,boxblur=24:2,eq=brightness=-0.25[bg];'
                         f'[b]crop={w}:{h}:{x}:{y},scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:{py}')
def frames(shots):
    out=[]
    for ss,dur,vf in shots:
        p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-filter_complex',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        while True:
            b=p.stdout.read(W*H*3)
            if len(b)<W*H*3: break
            out.append(Image.frombytes('RGB',(W,H),b))
        p.stdout.close(); p.wait()
    return out
B=lambda s,z=54,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
BADGE=Image.new('RGBA',(84,84),(0,0,0,0)); ImageDraw.Draw(BADGE).rounded_rectangle((0,0,83,83),16,fill=YEL)
_g=text_layer('G6',56,INK); BADGE.alpha_composite(_g,((84-_g.width)//2,(84-_g.height)//2-2))
C1=text_layer(CRED1,27,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf'); C2=text_layer(CRED2,27,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
def scene(name,shots,lab,idx,lines,out,dim=0):
    fr=frames(shots); L=chip(lab,RED,size=38); I=text_layer(idx,36,(255,255,255,215),'BarlowCondensed-ExtraBoldItalic.ttf') if idx else None
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,900,235)
        if dim: b.alpha_composite(Image.new('RGBA',(W,H),INK+(dim,)))
        b.alpha_composite(BADGE,(60,60)); put(b,L,W/2,102)
        if I: put(b,I,1020,102,'rm')
        kit2.bottom_fade(b,0.88,215); put(b,C1,W/2,1832); put(b,C2,W/2,1870)
        for Lx,y,st in lines:
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.4)))
            put(b,Lx,W/2+(1-a)*500,y,alpha=a)
        return b
    encode(name,gen,len(fr),out)
OUT='/home/claude/rockstar/ps5voit'; os.makedirs(OUT,exist_ok=True)
S={
 'v0':([(140.0,2.3,COVER(656))],'TU SAVAIS ?',None,[(text_layer('CE QUE PERSONNE',118,WHITE),330,None),(grad_text('NE TE DIT PAS',140),475,None),(B('sur les voitures de GTA 6',60),605,None)],0),
 'v1':([(3.0,2.6,PANEL(440,20,1080,300,800)),(7.0,2.4,PANEL(440,20,1080,300,800))],'DÉTAIL N°1','1 / 5',[(grad_text('UN MENU CACHÉ',125),330,0),(B('Radio, toit, phares, warning…'),465,0.2),(B('tout se règle depuis le volant'),530,0.2)],0),
 'v2':([(12.0,4.8,PANEL(1300,620,620,440,790))],'DÉTAIL N°2','2 / 5',[(grad_text('LA FICHE SECRÈTE',118),330,0),(B('Accès, sécurité, traceur : tout est dans le menu',48),465,0.2),(B('Un traceur peut balancer ta voiture volée aux flics',44,YEL),530,0.5)],0),
 'v3':([(52.4,4.4,COVER(656))],'DÉTAIL N°3','3 / 5',[(grad_text('LE TOIT SE REPLIE',118),330,0),(B('Un vrai cabriolet, animation complète'),465,0.2),(B('« Ouvrir le toit » dans le menu véhicule',50,YEL),530,0.5)],0),
 'v4':([(108.5,4.3,COVER(520))],'DÉTAIL N°4','4 / 5',[(grad_text('DRIFT SUR LA PLAGE',115),330,0),(B('Le sable vole et les passants'),465,0.2),(B('s\'écartent en catastrophe'),530,0.2)],0),
 'v5':([(161.6,1.0,COVER(560)),(162.6,4.6,COVER(400))],'DÉTAIL N°5','5 / 5',[(grad_text('LE CARJACKING',125),330,0),(B('Voiture garée : il te faut des outils'),465,0.2),(B('Avec un conducteur : tu le sors, point.',52,YEL),530,0.5)],0),
 'v6':([(172.5,2.5,COVER(656))],'À TOI',None,[(text_layer('TU ROULES EN',112,WHITE),330,0),(grad_text('QUOI ?',160),480,0.1),(B('Ta caisse préférée en commentaire'),605,0.3),(B('ABONNE-TOI @GTA6HUBFR_',56,YEL),675,0.5)],60),
}
ORDER=['v0','v1','v2','v3','v4','v5','v6']
if __name__=='__main__':
    todo=sys.argv[1:] or ORDER
    for n in todo:
        shots,lab,idx,lines,dim=S[n]; scene(n,shots,lab,idx,lines,OUT,dim)
    if not sys.argv[1:]: assemble(ORDER,OUT,'/home/claude/gta6hubfr_voitures_secrets.mp4')

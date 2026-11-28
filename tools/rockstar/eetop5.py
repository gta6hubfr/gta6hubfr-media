import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, ease_out_cubic, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/eastereggs/ee.mp4'
CRED1='Vidéo : ZacCoxTV (YouTube)  ·  Trouvailles : xGarbett, TheTruthHurts, nfxce'
CRED2='Page fan, non officielle'
def frames(shots):
    out=[]
    for ss,dur,cx in shots:
        if isinstance(cx,str):  # 'fit:<x>' : plan 16:9 entier en panneau, fond flouté
            fx=int(cx.split(':')[1])
            vf=(f'fps=30,split[a][b];[a]crop=608:1080:656:0,scale=1080:1920,boxblur=24:2,eq=brightness=-0.22[bg];'
                f'[b]scale=1242:699:flags=lanczos,crop=1080:699:{fx}:0[fg];[bg][fg]overlay=0:745')
        else:
            vf=f'fps=30,crop=608:1080:{cx}:0,scale=1080:1920:flags=lanczos'
        p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-filter_complex' if isinstance(cx,str) else '-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        while True:
            b=p.stdout.read(W*H*3)
            if len(b)<W*H*3: break
            out.append(Image.frombytes('RGB',(W,H),b))
        p.stdout.close(); p.wait()
    return out
B=lambda s,z=54,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
def badge():
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); return bd
BADGE=badge()
C1=text_layer(CRED1,27,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf'); C2=text_layer(CRED2,27,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
def scene(name,shots,lab,idx,lines,out):
    fr=frames(shots); L=chip(lab,RED,size=38); I=text_layer(idx,36,(255,255,255,215),'BarlowCondensed-ExtraBoldItalic.ttf') if idx else None
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,900,235)
        if name=='e6': b.alpha_composite(Image.new('RGBA',(W,H),INK+(95,)))
        b.alpha_composite(BADGE,(60,60)); put(b,L,W/2,102)
        if I: put(b,I,1020,102,'rm')
        kit2.bottom_fade(b,0.88,215); put(b,C1,W/2,1832); put(b,C2,W/2,1870)
        for Lx,y,st,en in lines:
            if en is not None and t>en: continue
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.4)))
            put(b,Lx,W/2+(1-a)*500,y,alpha=a)
        return b
    encode(name,gen,len(fr),out)
OUT='/home/claude/rockstar/eetop5'; os.makedirs(OUT,exist_ok=True)
S={
 'e0':([(380.2,1.65,560),(381.95,0.75,600)],'EASTER EGGS',None,[(text_layer('5 SECRETS FOUS',130,WHITE),330,None,None),(grad_text('DÉJÀ TROUVÉS',140),480,None,None),(B('dans GTA 6  ·  le n°1 va te choquer',58),610,None,None)]),
 'e5':([(501.0,4.2,600)],'SECRET N°5','5 / 5',[(grad_text("L'APPART",130),330,0,None),(text_layer('DE DEXTER',115,WHITE),470,0.1,None),(B('Washington Island : son kit de tueur'),590,0.3,None),(B('caché sur le toit'),655,0.3,None)]),
 'e4':([(519.0,4.2,656)],'SECRET N°4','4 / 5',[(grad_text('MONT KALAGA',130),330,0,None),(text_layer('LE NOUVEAU CHILIAD ?',96,WHITE),470,0.1,None),(B('Un cercle de pierres mystérieux'),590,0.3,None),(B('tout au sommet'),655,0.3,None)]),
 'e3':([(277.5,4.8,560)],'SECRET N°3','3 / 5',[(grad_text('ENLEVÉ PAR',130),330,0,None),(text_layer('UN OVNI',115,WHITE),470,0.1,None),(B('Près de Port Gellhorn, après 2 h du matin'),590,0.3,None),(B('= trophée secret « The Truth Is Out There »',48,YEL),655,0.5,None)]),
 'e2':([(579.3,4.05,640),(583.45,1.4,656)],'SECRET N°2','2 / 5',[(grad_text('UN VRAI ŒUF',130),330,0,None),(text_layer('DE PÂQUES',115,WHITE),470,0.1,None),(B('Au sommet de la plus haute tour'),590,0.3,None),(B('Lance-le : cinématique secrète',54,YEL),655,0.5,None)]),
 'e1':([(362.9,2.5,600),(386.75,3.7,'fit:60')],'SECRET N°1','1 / 5',[(grad_text('LIBÈRE',140),330,0,None),(text_layer('UN ALIEN',120,WHITE),475,0.1,None),(B('Labo secret : tape le code 2314,'),595,0.3,None),(B('puis récupère le verre de lait'),660,0.3,None)]),
 'e6':([(530.5,2.3,656)],'À TOI',None,[(text_layer('TU EN AS TROUVÉ',112,WHITE),330,0,None),(grad_text('COMBIEN ?',150),480,0.1,None),(B('Dis-le en commentaire'),600,0.3,None),(B('ABONNE-TOI @GTA6HUBFR_',56,YEL),670,0.5,None)]),
}
ORDER=['e0','e5','e4','e3','e2','e1','e6']
if __name__=='__main__':
    todo=sys.argv[1:] or ORDER
    for n in todo:
        shots,lab,idx,lines=S[n]; scene(n,shots,lab,idx,lines,OUT)
    if not sys.argv[1:]: assemble(ORDER,OUT,'/home/claude/gta6hubfr_top5_secrets.mp4')

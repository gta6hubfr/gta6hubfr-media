import sys; sys.path.insert(0,'/home/claude/rockstar')
import kit2; kit2.LIB='/home/claude/rockstar/lib2/'
from visages import *
from brief import chip, RED
SRC='Sources : PowerPyx · MetaForge · TheGamesWiki'
def bg(name,t,d,zin,pan,dim=80):
    b=kit2.kenburns(name,min(1,t/d),zin,pan); b.alpha_composite(Image.new('RGBA',(W,H),INK+(dim,)))
    kit2.top_fade(b,420,170); bottom_fade(b,0.42,250); return b
ALERT=chip('ALERTE',RED,size=44)
SPOIL=chip('PETIT SPOIL · CHAPITRE 1',YEL,fg=INK,size=44)
ROW=Image.new('RGBA',(ALERT.width+16+SPOIL.width,max(ALERT.height,SPOIL.height)),(0,0,0,0)); ROW.alpha_composite(ALERT,(0,0)); ROW.alpha_composite(SPOIL,(ALERT.width+16,0))
def hook(out):
    d=3.0
    l1=text_layer('ARRÊTE DE FARMER',128,WHITE); l2=grad_text('AU CHAPITRE 1',150)
    l3=text_layer('Tout ton argent va disparaître',60,YEL,'BarlowCondensed-ExtraBoldItalic.ttf')
    def gen(k):
        t=k/30; b=bg('jason_and_lucia_15',t,d,True,0.5,70); corner(b,None)
        if int(t*4)%2==0: b.alpha_composite(Image.new('RGBA',(W,H),(235,50,70,28)))
        s=1+0.06*(1-ease_out_cubic(prog(t,0,0.35)))
        put(b,ROW,W/2,1060)
        for L,y in ((l1,1180),(l2,1325),(l3,1455)):
            Ls=L.resize((int(L.width*s),int(L.height*s))) if s>1.001 else L
            put(b,Ls,W/2,y)
        return b
    encode('f0',gen,int(d*30),out)
def card(name,i,top,big,body,out,zin,pan,d=4.6):
    t1=text_layer(top,112,WHITE); t2=grad_text(big,132)
    ds=[text_layer(l,52,(240,240,245),'BarlowCondensed-SemiBoldItalic.ttf') for l in body]
    src=text_layer(SRC,26,(200,200,210,170),'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=bg(name,t,d,zin,pan); corner(b,f'{i} / 2')
        a1=ease_out_cubic(prog(t,0.0,0.35)); a2=ease_out_back(prog(t,0.12,0.45)); a3=ease_out_cubic(prog(t,0.45,0.5))
        put(b,t1,W/2-(1-a1)*500,1150,alpha=a1); put(b,t2,W/2+(1-clamp(a2))*600,1285,alpha=clamp(a2))
        for j,dl in enumerate(ds): put(b,dl,W/2,1420+j*64+(1-a3)*20,alpha=a3)
        put(b,src,W/2,1660,alpha=a3)
        return b
    encode(f'f{i}',gen,int(d*30),out)
def outro(out):
    d=2.9
    def gen(k):
        t=k/30; b=bg('jason_and_lucia_11',t,d,False,0.5,120); corner(b,None)
        a1=ease_out_back(prog(t,0.0,0.4)); a2=ease_out_cubic(prog(t,0.3,0.5))
        put(b,grad_text('ENREGISTRE',170),W/2,1150,alpha=clamp(a1))
        put(b,text_layer("pour ne pas l'oublier",64,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1300,alpha=a2)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',56,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1400,alpha=a2)
        return b
    encode('f3',gen,int(d*30),out)
if __name__=='__main__':
    out='/home/claude/rockstar/farm'; os.makedirs(out,exist_ok=True)
    hook(out)
    card('raul_bautista_02',1,'À LA FIN DU CHAPITRE 1,','TON CASH EST PERDU',["Tout ce que tu as farmé disparaît.","Joue juste l'histoire."],out,True,0.5)
    card('lucia_caminos_14',2,'ENSUITE :','DÉPOSE TOUT',["Si tu meurs ou si tu te fais arrêter,","le cash sur toi est perdu.","Dépose-le sur BuckMe, au distributeur."],out,False,0.85)
    outro(out)
    assemble(['f0','f1','f2','f3'],out,'/home/claude/gta6hubfr_farm_chapitre1.mp4')

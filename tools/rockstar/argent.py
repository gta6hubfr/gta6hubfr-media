import sys; sys.path.insert(0,'/home/claude/rockstar')
from visages import *
import math
T=[('ambrosia_03','LE COFFRE','SECRET.',['Après la livraison de rhum pour Shirley,','retourne au magasin d\'alcool :','le perroquet révèle ~2 700 $ cachés.'],True,0.5),
   ('grassrivers_01','LES PLONGÉES','DE KENTON.',['Les sites violets au large des Keys :','environ 1 400 $ par épave,','presque sans risque.'],False,0.45),
   ('mount_kalaga_03','VOLE LES','FOURGONS.',['Un van chargé (ex : Weazel News)','se revend plus de 1 000 $.','Dès le chapitre 2, vends chez Moses.'],True,0.5),
   ('grassrivers_06','LES BANQUES,','PLUS TARD.',['Les gros coffres : jusqu\'à 205 000 $.','Mais ça ne s\'ouvre','qu\'à la fin du chapitre 4.'],False,0.55)]
D=5.0
SRC='SOURCES : GUIDES OUTPUTLAG · DUALSHOCKERS · GADGETBRIDGE · BOOSTINGFACTORY'
def tip(i,out):
    img,l1,l2,body,zin,pan=T[i]
    t1=text_layer(l1,124,WHITE); t2=grad_text(l2,140 if len(l2)<12 else 116)
    num=text_layer(f'0{i+1}',420,(255,255,255,40),'Anton-Regular.ttf')
    ds=[text_layer(l,48,(235,235,240),'BarlowCondensed-SemiBoldItalic.ttf') for l in body]
    src=text_layer(SRC,26,(200,200,210,170),'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=kenburns(img,t/D,zin,pan); bottom_fade(b,0.36,248); corner(b,f'{i+1} / 4')
        an=ease_out_cubic(prog(t,0.0,1.0)); a1=ease_out_cubic(prog(t,0.2,0.7)); a2=ease_out_back(prog(t,0.4,0.8)); a3=ease_out_cubic(prog(t,0.85,0.6))
        e=ease_in_cubic(prog(t,D-0.3,0.3))
        put(b,num,W/2+180-(1-an)*120,960,alpha=an*(1-e))
        put(b,t1,W/2-(1-a1)*600-e*1200,1180,alpha=a1); put(b,t2,W/2+(1-clamp(a2))*700-e*1200,1315,alpha=clamp(a2))
        for j,dl in enumerate(ds): put(b,dl,W/2,1450+j*60+(1-a3)*25,alpha=a3*(1-e))
        put(b,src,W/2,1660,alpha=a3*(1-e))
        return b
    encode(f'm{i}',gen,int(D*30),out)
def m_intro(out):
    d=3.4
    def gen(k):
        t=k/30; b=kenburns('ambrosia_06',t/d,True,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(110,))); bottom_fade(b,0.35,240); corner(b,None)
        a1=ease_out_cubic(prog(t,0.1,0.7)); a2=ease_out_back(prog(t,0.35,0.8)); a3=ease_out_cubic(prog(t,0.9,0.6))
        put(b,text_layer('FAIS DU CASH',160,WHITE),W/2-(1-a1)*700,1170,alpha=a1)
        put(b,grad_text('DÈS LE DÉBUT.',140),W/2+(1-clamp(a2))*800,1320,alpha=clamp(a2))
        put(b,text_layer('4 plans pour remplir ton compte dans GTA 6',56,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1450,alpha=a3)
        return b
    encode('m_intro',gen,int(d*30),out)
def m_outro(out):
    d=3.6
    big=text_layer('$',900,(255,255,255,22),'Anton-Regular.ttf')
    def gen(k):
        t=k/30; b=Image.new('RGBA',(W,H),INK+(255,))
        g=Image.new('RGBA',(W,H),(0,0,0,0)); dr=ImageDraw.Draw(g)
        for r,c in [(700,(240,70,140,60)),(500,(255,150,60,60))]:
            cx=W/2+math.sin(t*0.8+r)*150; cy=H*0.45+math.cos(t*0.6+r)*120; dr.ellipse((cx-r,cy-r,cx+r,cy+r),fill=c)
        g=g.filter(ImageFilter.GaussianBlur(160)); b.alpha_composite(g); put(b,big,W/2,H*0.42); corner(b,None)
        a1=ease_out_cubic(prog(t,0.1,0.7)); a2=ease_out_back(prog(t,0.35,0.8)); a3=ease_out_cubic(prog(t,0.9,0.6))
        put(b,text_layer('TON PREMIER',150,WHITE),W/2-(1-a1)*700,820,alpha=a1)
        put(b,grad_text('ACHAT ?',180),W/2+(1-clamp(a2))*800,990,alpha=clamp(a2))
        put(b,text_layer('Voiture, maison, armes... dis-le en commentaire',52,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1160,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',54,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1250,alpha=a3)
        return b
    encode('m_outro',gen,int(d*30),out)
if __name__=='__main__':
    out='/home/claude/rockstar/argent'; os.makedirs(out,exist_ok=True)
    m_intro(out)
    for i in range(4): tip(i,out)
    m_outro(out)
    assemble(['m_intro']+[f'm{i}' for i in range(4)]+['m_outro'],out,'/home/claude/gta6hubfr_cash.mp4')

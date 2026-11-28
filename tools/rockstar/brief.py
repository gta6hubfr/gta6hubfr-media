import sys, math; sys.path.insert(0,'/home/claude/rockstar')
import kit2; kit2.LIB='/home/claude/rockstar/lib2/'
from visages import *
RED=(235,50,70)
C=[('jason_and_lucia_01',True,0.5,'RECORD','24,6 M','D\'EXEMPLAIRES',['vendus en moins de 24 h,','pour 2,36 milliards de dollars.'],'SOURCE : SENSOR TOWER VIA DEADLINE'),
   ('jason_duval_04',False,0.55,'HISTOIRE','x2,25','GTA V EST BATTU',['Environ 2,25 fois les recettes','du lancement de GTA V (2013).'],'SOURCE : SENSOR TOWER VIA FOX 5'),
   ('lucia_caminos_08',True,0.5,'BON PLAN','60 €','AU LIEU DE 79,99 €',['Code en boîte chez Leclerc et Carrefour,','selon les stocks.'],'SOURCES : CNEWS · DEALABS'),
   ('jason_duval_07',False,0.5,'ÇA BLOQUE ?','MAJ PS5','+ PATCH DE 602 MO',['Le jeu ne se lance pas ? Mets à jour','la console, puis le jeu.'],'SOURCES : PALAIS DES GOODIES · HAPPYGAMER')]
D=4.2
def chip(txt,col,fg=WHITE,size=40):
    t=text_layer(txt,size,fg,'BarlowCondensed-ExtraBoldItalic.ttf'); w,h=t.width+44,t.height+18
    L=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(L).rounded_rectangle((0,0,w-1,h-1),10,fill=col); L.alpha_composite(t,(22,9)); return L
TICK=text_layer('  ·  '.join(['LE BRIEF GTA 6','NEWS','BONS PLANS','ASTUCES','@GTA6HUBFR_',''])*3,34,INK,'BarlowCondensed-ExtraBoldItalic.ttf')
def frame_common(b,t,idx):
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    put(b,chip('LE BRIEF  ·  VEN. 20 NOV.',RED,size=36),W/2,102)
    if idx: put(b,text_layer(idx,36,(255,255,255,210),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    band=Image.new('RGBA',(W,64),YEL+(255,)); x=-int(t*140)%(TICK.width//3); band.alpha_composite(TICK,(-x,(64-TICK.height)//2)); b.alpha_composite(band,(0,1740))
    put(b,text_layer('Images : @RockstarGames  ·  Page fan, non officielle',28,(255,255,255,130),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1850)
def bgimg(name,t,dur,zin,pan):
    b=kit2.kenburns(name,min(1,t/dur),zin,pan); b.alpha_composite(Image.new('RGBA',(W,H),INK+(60,))); kit2.top_fade(b,380,160); kit2.bottom_fade(b,0.32,250); return b
def card(i,out):
    img,zin,pan,lab,big,sub,body,src=C[i]
    BIG=grad_text(big,300 if len(big)<6 else 230); S=text_layer(sub,96,WHITE); L=chip(lab,YEL,INK,46)
    ds=[text_layer(x,50,(240,240,245),'BarlowCondensed-SemiBoldItalic.ttf') for x in body]; sr=text_layer(src,26,(200,200,210,170),'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=bgimg(img,t,D,zin,pan); frame_common(b,t,f'{i+1} / 4')
        a0=ease_out_back(prog(t,0,0.4)); a1=ease_out_cubic(prog(t,0.1,0.45)); a2=ease_out_cubic(prog(t,0.25,0.45)); a3=ease_out_cubic(prog(t,0.5,0.4)); e=ease_in_cubic(prog(t,D-0.25,0.25))
        put(b,L,W/2-(1-clamp(a0))*400,1000,alpha=clamp(a0)*(1-e))
        z=0.85+0.15*clamp(a1)+0.03*t/D; put(b,BIG.resize((max(1,int(BIG.width*z)),max(1,int(BIG.height*z)))),W/2,1180,alpha=a1*(1-e))
        put(b,S,W/2+(1-a2)*500-e*1100,1355,alpha=a2)
        for j,x in enumerate(ds): put(b,x,W/2,1470+j*60+(1-a3)*20,alpha=a3*(1-e))
        put(b,sr,W/2,1665,alpha=a3*(1-e))
        return b
    encode(f'b{i}',gen,int(D*30),out)
def hook(out):
    d=1.6; t1=text_layer('GTA 6 :',150,WHITE); t2=grad_text('24 H DE FOLIE.',150); s=text_layer('Records, bon plan et galère du lancement',56,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'); L=chip('BREAKING',RED,size=48)
    def gen(k):
        t=k/30; b=bgimg('jason_and_lucia_04',t,d,True,0.5); frame_common(b,t,None)
        put(b,L,W/2,1040); z=1+0.05*t; put(b,t1,W/2,1190); put(b,t2.resize((int(t2.width*z),int(t2.height*z))),W/2,1350); put(b,s,W/2,1490)
        return b
    encode('b_hook',gen,int(d*30),out)
def outro(out):
    d=2.6
    def gen(k):
        t=k/30; b=bgimg('jason_and_lucia_16',t,d,True,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(90,))); frame_common(b,t,None)
        a1=ease_out_cubic(prog(t,0,0.4)); a2=ease_out_back(prog(t,0.15,0.5)); a3=ease_out_cubic(prog(t,0.4,0.4))
        put(b,text_layer('TU L\'AS EU',150,WHITE),W/2-(1-a1)*600,1130,alpha=a1)
        put(b,grad_text('À COMBIEN ?',160),W/2+(1-clamp(a2))*700,1290,alpha=clamp(a2))
        put(b,text_layer('Dis ton prix en commentaire  ·  Le brief chaque jour',50,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1440,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',54,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1530,alpha=a3)
        return b
    encode('b_out',gen,int(d*30),out)
if __name__=='__main__':
    out='/home/claude/rockstar/brief'; os.makedirs(out,exist_ok=True)
    if sys.argv[1:]==['test']:
        D2=D
        for i in (0,2):
            img,zin,pan,lab,big,sub,body,src=C[i]
        hook(out); card(2,out)
    else:
        hook(out); [card(i,out) for i in range(4)]; outro(out)
        assemble(['b_hook','b0','b1','b2','b3','b_out'],out,'/home/claude/gta6hubfr_brief_20nov.mp4')

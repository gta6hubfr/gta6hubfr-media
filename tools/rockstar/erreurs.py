import sys, math; sys.path.insert(0,'/home/claude/rockstar')
from visages import *
from PIL import ImageFilter
E3=[('ACTIVER','LES CODES.',['Codes de triche activés =','adieu les trophées.']),
    ('GONFLER TON','PROFIL CRIMINEL.',['Il est permanent :','réfléchis avant de tout faire.']),
    ('FUIR AVEC','TA VOITURE PERSO.',['La police peut la mettre en fourrière.','Prends une voiture de fuite.'])]
PAL=[[(240,70,140),(255,150,60)],[(170,70,220),(240,70,140)],[(255,120,70),(170,70,220)]]
def corner(b,idx):
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    if idx: put(b,text_layer(idx,36,(255,255,255,210),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    put(b,text_layer('Images : @RockstarGames  ·  Page fan, non officielle',28,(255,255,255,130),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1830)
SRC='SOURCES : GUIDES EGAMERS · GAMINGPROMAX'
def bg(t,pal,seed):
    b=Image.new('RGBA',(W,H),INK+(255,)); g=Image.new('RGBA',(W//4,H//4),(0,0,0,0)); d=ImageDraw.Draw(g)
    for j,(r,c) in enumerate([(190,pal[0]),(140,pal[1])]):
        cx=W/8+math.sin(t*0.9+seed+j*2)*70; cy=H/8*(0.8+0.5*j)+math.cos(t*0.7+seed+j)*60
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=c+(110,))
    g=g.filter(ImageFilter.GaussianBlur(45)).resize((W,H)); b.alpha_composite(g)
    s=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(s); off=int(t*40)%80
    for x in range(-H,W,80): sd.line((x+off,0,x+off+H,H),fill=(255,255,255,10),width=18)
    b.alpha_composite(s); return b
def pill(b,a):
    p=text_layer('TU AS FAIT LAQUELLE ?',40,INK,'BarlowCondensed-ExtraBoldItalic.ttf')
    w,h=p.width+56,p.height+22; L=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(L).rounded_rectangle((0,0,w-1,h-1),h//2,fill=YEL)
    L.alpha_composite(p,(28,11)); put(b,L,W/2,250,alpha=a)
def cross(size,a):
    L=Image.new('RGBA',(size,size),(0,0,0,0)); d=ImageDraw.Draw(L); d.ellipse((0,0,size-1,size-1),fill=(230,40,60,int(235*a)))
    m=size*0.3; w=int(size*0.11); d.line((m,m,size-m,size-m),fill=(255,255,255,int(255*a)),width=w); d.line((size-m,m,m,size-m),fill=(255,255,255,int(255*a)),width=w); return L
def hook(out):
    d=1.4; t1=text_layer('3 ERREURS',190,WHITE); t2=grad_text('QUE TU FAIS DÉJÀ.',120); s=text_layer('dans GTA 6',64,WHITE,'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=bg(t,PAL[0],0); corner(b,None); pill(b,1)
        z=1+0.04*t; put(b,t1.resize((int(t1.width*z),int(t1.height*z))),W/2,820); put(b,t2,W/2,980); put(b,s,W/2,1100)
        return b
    encode('e_hook',gen,int(d*30),out)
def err(i,out):
    d=4.4; l1,l2,body=E3[i]; t1=text_layer(l1,120,WHITE); t2=grad_text(l2,120 if len(l2)<14 else 100)
    num=text_layer(f'0{i+1}',890,(255,255,255,28),'Anton-Regular.ttf'); ds=[text_layer(x,52,(240,240,245),'BarlowCondensed-SemiBoldItalic.ttf') for x in body]
    src=text_layer(SRC,26,(200,200,210,160),'BarlowCondensed-SemiBoldItalic.ttf'); ne=text_layer('ERREUR',44,(255,255,255,200),'BarlowCondensed-ExtraBoldItalic.ttf')
    def gen(k):
        t=k/30; b=bg(t,PAL[i],i*3); corner(b,f'{i+1} / 3'); pill(b,1)
        a0=ease_out_cubic(prog(t,0,0.35)); a1=ease_out_cubic(prog(t,0.05,0.4)); a2=ease_out_back(prog(t,0.15,0.5)); a3=ease_out_cubic(prog(t,0.45,0.4)); ac=ease_out_back(prog(t,0.3,0.45))
        e=ease_in_cubic(prog(t,d-0.25,0.25))
        put(b,num,W/2+(1-a0)*200,1090,alpha=a0*(1-e))
        put(b,ne,W/2,890,alpha=a1*(1-e))
        cs=max(2,int(170*clamp(ac))); put(b,cross(cs,1-e),W/2,1030)
        put(b,t1,W/2-(1-a1)*500-e*1200,1260,alpha=a1); put(b,t2,W/2+(1-clamp(a2))*600-e*1200,1395,alpha=clamp(a2))
        for j,x in enumerate(ds): put(b,x,W/2,1530+j*62+(1-a3)*20,alpha=a3*(1-e))
        put(b,src,W/2,1690,alpha=a3*(1-e))
        return b
    encode(f'e{i}',gen,int(d*30),out)
def outro(out):
    d=2.6
    def gen(k):
        t=k/30; b=bg(t,PAL[1],9); corner(b,None)
        a1=ease_out_cubic(prog(t,0,0.4)); a2=ease_out_back(prog(t,0.15,0.5)); a3=ease_out_cubic(prog(t,0.4,0.4))
        put(b,text_layer('TU AS FAIT',150,WHITE),W/2-(1-a1)*600,1150,alpha=a1)
        put(b,grad_text('LAQUELLE ?',170),W/2+(1-clamp(a2))*700,1315,alpha=clamp(a2))
        put(b,text_layer('Avoue en commentaire',60,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1470,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_ POUR LA SUITE',50,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1560,alpha=a3)
        return b
    encode('e_out',gen,int(d*30),out)
if __name__=='__main__':
    out='/home/claude/rockstar/erreurs'; os.makedirs(out,exist_ok=True)
    hook(out); [err(i,out) for i in range(3)]; outro(out)
    assemble(['e_hook','e0','e1','e2','e_out'],out,'/home/claude/gta6hubfr_3_erreurs.mp4')

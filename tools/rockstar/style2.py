import sys, os; sys.path.insert(0,'/home/claude/rockstar')
from kit2 import *
from PIL import Image, ImageDraw, ImageFont
GRAD=[(255,190,60),(255,120,70),(240,70,140),(170,70,220)]
def grad_text(txt,size,fname='BarlowCondensed-BlackItalic.ttf'):
    m=text_layer(txt,size,WHITE,fname).split()[3]
    w,h=m.size; g=Image.new('RGBA',(w,h))
    px=g.load()
    for x in range(w):
        t=x/max(1,w-1)*(len(GRAD)-1); i=min(int(t),len(GRAD)-2); f=t-i
        c=tuple(int(GRAD[i][k]*(1-f)+GRAD[i+1][k]*f) for k in range(3))
        for y in range(h): px[x,y]=c+(255,)
    g.putalpha(m); return g
def tracked(txt,size,fill,fname='BarlowCondensed-SemiBoldItalic.ttf',sp=6):
    return text_layer(' '.join(txt) if sp else txt,size,fill,fname)
def slide(bg,l1,l2,body,src,out,idx=None,total=None):
    b=kenburns(bg,0.5,True,0.5)
    # deep fade from 45%
    bottom_fade(b,0.38,250)
    put(b,text_layer(l1,128,WHITE),W/2,1205)
    put(b,grad_text(l2,128),W/2,1330)
    for j,l in enumerate(body): put(b,text_layer(l,50,(235,235,240),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1460+j*62)
    if src: put(b,text_layer(src.upper(),30,(255,255,255,150),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1640)
    # small corner mark
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    if idx: put(b,text_layer(f'{idx} / {total}',36,(255,255,255,200),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    put(b,text_layer('Images : @RockstarGames  ·  Page fan, non officielle',28,(255,255,255,120),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1830)
    b.convert('RGB').save(out,quality=93)
def end_slide(bg,l1,l2,cta,out):
    b=kenburns(bg,0.5,False,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(185,)))
    put(b,text_layer(l1,150,WHITE),W/2,820); put(b,grad_text(l2,150),W/2,970)
    bd=Image.new('RGBA',(220,220),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,219,219),40,fill=YEL)
    g=text_layer('G6',150,INK); bd.alpha_composite(g,((220-g.width)//2,(220-g.height)//2-6)); put(b,bd,W/2,1250)
    for x0,x1 in [(140,400),(680,940)]: b.alpha_composite(Image.new('RGBA',(x1-x0,4),YEL+(255,)),(x0,1248))
    for j,c in enumerate(cta.split('  ·  ')): put(b,text_layer(c,56 if j==0 else 46,WHITE if j==0 else YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1440+j*80)
    put(b,text_layer('Images : @RockstarGames  ·  Page fan, non officielle',28,(255,255,255,120),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1830)
    b.convert('RGB').save(out,quality=93)

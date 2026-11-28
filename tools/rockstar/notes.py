import sys; sys.path.insert(0,'/home/claude/rockstar')
from kit2 import *
def s_open(t,d):
    b=kenburns('vice_city_11',t/d,True,0.5); top_fade(b); bottom_fade(b,0.42); header(b,1.0)
    a0=ease_out_cubic(prog(t,0.1,0.6))
    tag=yellow_box(300,70); put(b,tag,90+150,1080,'mm',a0); put(b,text_layer('NEWS',60,INK),240,1076,'mm',a0)
    a1=ease_out_cubic(prog(t,0.3,0.8)); a2=ease_out_back(prog(t,0.6,0.8))
    put(b,text_layer('GTA 6 : LES',180,WHITE),W/2-(1-a1)*700,1260,alpha=a1)
    box=yellow_box(900,200); x2=W/2+(1-clamp(a2))*900
    put(b,box,x2,1450,alpha=clamp(a2)); put(b,text_layer('PREMIÈRES NOTES',138,INK),x2,1442,alpha=clamp(a2))
    a3=ease_out_cubic(prog(t,1.2,0.7))
    put(b,text_layer('Les tests sont tombés ce midi',62,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1610+(1-a3)*30,alpha=a3)
    credit(b); return b
def s_meta(t,d):
    b=kenburns('mount_kalaga_02',t/d,False,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(150,))); header(b,1.0)
    n=int(round(99*ease_out_cubic(prog(t,0.2,1.6))))
    a=ease_out_cubic(prog(t,0.1,0.5))
    put(b,text_layer(str(n),560,YEL,'Anton-Regular.ttf'),W/2,820,alpha=a)
    put(b,text_layer('SUR METACRITIC',130,WHITE),W/2,1150,alpha=ease_out_cubic(prog(t,0.5,0.6)))
    a2=ease_out_cubic(prog(t,1.4,0.7))
    put(b,text_layer('Record absolu, à égalité avec',62,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1290,alpha=a2)
    put(b,text_layer('Zelda : Ocarina of Time',62,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1365,alpha=a2)
    credit(b); return b
ROWS=[('IGN','10/10'),('GAMESPOT','10/10'),('GAME INFORMER','10/10'),('JEUXVIDEO.COM','19/20'),('GAMESRADAR+','5/5')]
def s_rows(t,d):
    b=kenburns('leonida_keys_02',t/d,True,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(165,))); header(b,1.0)
    put(b,text_layer('LA PRESSE DIT…',120,WHITE),90,460,'lm',ease_out_cubic(prog(t,0,0.5)))
    for i,(m,s) in enumerate(ROWS):
        a=ease_out_cubic(prog(t,0.35+i*0.35,0.55)); y=650+i*190
        if a<=0: continue
        off=(1-a)*(700 if i%2==0 else -700)
        row=Image.new('RGBA',(900,150),(255,255,255,28)); b.alpha_composite(row,(int(90+off),y-75))
        b.alpha_composite(Image.new('RGBA',(12,150),YEL+(255,)),(int(90+off),y-75))
        put(b,text_layer(m,80,WHITE),130+off,y,'lm',a)
        put(b,text_layer(s,110,YEL,'Anton-Regular.ttf'),960+off,y,'rm',a)
    credit(b); return b
def s_end(t,d):
    b=kenburns('vice_city_26',t/d,False,0.5); top_fade(b); bottom_fade(b,0.4); header(b,1.0)
    a1=ease_out_cubic(prog(t,0.2,0.7)); a2=ease_out_back(prog(t,0.5,0.8))
    put(b,text_layer('ET TOI,',190,WHITE),W/2+(1-a1)*700,1230,alpha=a1)
    box=yellow_box(940,170); x2=W/2-(1-clamp(a2))*900
    put(b,box,x2,1420,alpha=clamp(a2)); put(b,text_layer('TU LUI METS COMBIEN ?',112,INK),x2,1412,alpha=clamp(a2))
    a3=ease_out_cubic(prog(t,1.1,0.7))
    put(b,text_layer('Ta note en commentaire',62,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1570,alpha=a3)
    put(b,text_layer('Sources : Metacritic, IGN, GameSpot, Game Informer, JV.com, GamesRadar+',32,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1720)
    credit(b); return b
SC=[('n_open',s_open,4.0),('n_meta',s_meta,4.2),('n_rows',s_rows,5.5),('n_end',s_end,4.0)]
out='/home/claude/rockstar/notes'; os.makedirs(out,exist_ok=True)
if sys.argv[1]=='stills':
    from PIL import Image as I
    s=I.new('RGB',(360*4,640))
    for i,(n,f,d) in enumerate(SC): s.paste(f(d*0.8,d).convert('RGB').resize((360,640)),(i*360,0))
    s.save('/home/claude/rockstar/notes_sheet.jpg')
else:
    for n,f,d in SC: render_scene(n,f,d,out)
    assemble([n for n,_,_ in SC],out,'/home/claude/gta6hubfr_premieres_notes.mp4')

import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, text_layer, grad_text, put, W, H, YEL, INK, WHITE, Image, ImageDraw, os
SRC='/home/claude/opus/lasalle'; OUT='/home/claude/rockstar/lasalle'; os.makedirs(OUT,exist_ok=True)
CLIPS=[  # fichier, début, fin (None = jusqu'au bout), ligne blanche, ligne dégradé
 ('c01',0,None,'« DANS GTA 5,','ÇA LE FAISAIT PAS »'),
 ('c02',16.4,None,'« LA CONDUITE','EST TROP LOURDE »'),
 ('c06',0,None,'LA CARTE','EST INCROYABLE'),
 ('c08',0,None,'ENFIN DES','CLIGNOTANTS !'),
 ('c11',0,None,'LE TÉLÉPHONE PASSE','EN 1RE PERSONNE'),
]
def fit(fn,s,size,maxw=1000,**kw):
    while True:
        L=fn(s,size,**kw) if kw else fn(s,size)
        if L.width<=maxw or size<60: return L
        size-=6
def overlay(i,l1,l2):
    b=Image.new('RGBA',(W,H),(0,0,0,0))
    g=Image.new('L',(1,620)); g.putdata([int(225*(1-(y/620))**1.4) for y in range(620)])
    b.paste(Image.new('RGBA',(W,620),INK+(255,)),(0,0),g.resize((W,620)))
    g2=Image.new('L',(1,240)); g2.putdata([int(200*(y/240)**1.5) for y in range(240)])
    b.paste(Image.new('RGBA',(W,240),INK+(255,)),(0,H-240),g2.resize((W,240)))
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); ImageDraw.Draw(bd).rounded_rectangle((0,0,83,83),16,fill=YEL)
    t=text_layer('G6',56,INK,'BarlowCondensed-ExtraBoldItalic.ttf'); bd.alpha_composite(t,((84-t.width)//2,(84-t.height)//2-2)); b.alpha_composite(bd,(60,60))
    put(b,chip('LASALLE DÉCOUVRE GTA 6',RED,size=36),W/2,102)
    put(b,text_layer(f'{i}/5',38,(255,255,255,225),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    put(b,fit(text_layer,l1,104,color=WHITE) if False else fit(lambda s,z: text_layer(s,z,WHITE),l1,104),W/2,300)
    put(b,fit(grad_text,l2,124),W/2,430)
    put(b,text_layer('Vidéo : LaSalle (YouTube)  ·  Page fan, non officielle',27,(255,255,255,185),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1868)
    p=f'{OUT}/ov{i}.png'; b.save(p); return p
for i,(f,a,e,l1,l2) in enumerate(CLIPS,1):
    ov=overlay(i,l1,l2); src=f'{SRC}/{f}.mp4'; dst=f'/home/claude/gta6hubfr_lasalle_{i}_5.mp4'
    cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-i',src,'-i',ov,'-filter_complex','[0:v][1:v]overlay=0:0,format=yuv420p',
         '-c:v','libx264','-preset','veryfast','-crf','19','-c:a','aac','-b:a','160k','-movflags','+faststart',dst+'.tmp.mp4']
    subprocess.run(cmd,check=True); os.replace(dst+'.tmp.mp4',dst); print(dst)

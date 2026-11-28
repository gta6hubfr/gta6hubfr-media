import sys; sys.path.insert(0,'/home/claude/rockstar')
from kit2 import *
out='/home/claude/carrousel_vice_city_nuit'; os.makedirs(out, exist_ok=True)
slides=[('vice_city_22','LES NÉONS','Station-service, 2 h du matin.'),
        ('vice_city_13','LES CLUBS','La ville se réveille quand le soleil se couche.'),
        ('vice_city_17','LES QUARTIERS','Gyrophares et palmiers.'),
        ('vice_city_27','LA SKYLINE','Vice City, vue d\'en haut.')]
def still(key, zi=True): return kenburns(key, 0.5, zi, 0.5)
# cover
b=still('vice_city_22'); top_fade(b); bottom_fade(b,0.42); header(b,1.0)
put(b,text_layer('VICE CITY',220,WHITE),W/2,1270)
box=yellow_box(700,210); put(b,box,W/2,1470); put(b,text_layer('LA NUIT',200,INK),W/2,1462)
put(b,text_layer('Images officielles  ·  GLISSE >>',56,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1640)
credit(b); b.convert('RGB').save(f'{out}/01_couverture.jpg',quality=93)
for i,(k,t1,t2) in enumerate(slides[1:],start=2):
    b=still(k); top_fade(b); bottom_fade(b,0.55); header(b,1.0)
    b.alpha_composite(Image.new('RGBA',(140,10),YEL+(255,)),(90,1395))
    put(b,text_layer(f'{i-1:02d} / 03',46,(255,255,255,190),'BarlowCondensed-ExtraBoldItalic.ttf'),990,1395,'rm')
    put(b,text_layer(t1,150,YEL),100,1510,'lm'); put(b,text_layer(t1,150,WHITE),90,1500,'lm')
    put(b,text_layer(t2,58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),90,1630,'lm')
    credit(b); b.convert('RGB').save(f'{out}/{i:02d}_{k}.jpg',quality=93)
# CTA
b=still('vice_city_03',False); b.alpha_composite(Image.new('RGBA',(W,H),INK+(170,))); header(b,1.0)
put(b,text_layer('TA PRÉFÉRÉE ?',190,WHITE),W/2,820)
for j,lab in enumerate(['1  LES CLUBS','2  LES QUARTIERS','3  LA SKYLINE']):
    put(b,text_layer(lab,84,YEL if j%2==0 else WHITE),W/2,1020+j*130)
put(b,text_layer('Réponds avec un chiffre en commentaire',58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1600)
credit(b); b.convert('RGB').save(f'{out}/05_question.jpg',quality=93)
from PIL import Image as I; import glob
fs=sorted(glob.glob(out+'/*.jpg')); s=I.new('RGB',(300*len(fs),533))
for i,f in enumerate(fs): s.paste(I.open(f).resize((300,533)),(i*300,0))
s.save('/home/claude/rockstar/car_sheet.jpg')
print(fs)

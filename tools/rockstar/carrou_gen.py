import sys, json; sys.path.insert(0,'/home/claude/rockstar')
from kit2 import *
def still(k): return kenburns(k,0.5,True,0.5)
def build(out, cover, ctitle, cbox, csub, slides, cta):
    os.makedirs(out, exist_ok=True)
    b=still(cover); top_fade(b); bottom_fade(b,0.4); header(b,1.0)
    tag=yellow_box(300,70); put(b,tag,240,1000); put(b,text_layer('TESTS',60,INK),240,996)
    put(b,text_layer(ctitle,170,WHITE),W/2,1170)
    bw=min(980, text_layer(cbox,150,INK).width+60)
    put(b,yellow_box(bw,190),W/2,1360); put(b,text_layer(cbox,150,INK),W/2,1352)
    put(b,text_layer(csub,58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1520)
    put(b,text_layer('GLISSE >>',54,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1610)
    credit(b); b.convert('RGB').save(f'{out}/01_couverture.jpg',quality=93)
    for i,(k,t,lines,src) in enumerate(slides,start=1):
        b=still(k); top_fade(b); bottom_fade(b,0.42,245); header(b,1.0)
        put(b,text_layer(f'0{i}',300,(0,0,0,0),'Anton-Regular.ttf',stroke=4,stroke_fill=YEL+(230,)),90,1130,'lm')
        sz=120 if len(t)<=18 else 100
        put(b,text_layer(t,sz,YEL),98,1338,'lm'); put(b,text_layer(t,sz,WHITE),90,1330,'lm')
        for j,l in enumerate(lines): put(b,text_layer(l,60,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),90,1450+j*70,'lm')
        put(b,text_layer(f'Source : {src}',40,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),90,1640,'lm')
        credit(b); b.convert('RGB').save(f'{out}/{i+1:02d}_{k}.jpg',quality=93)
    k,l1,l2,l3=cta
    b=still(k); b.alpha_composite(Image.new('RGBA',(W,H),INK+(175,))); header(b,1.0)
    put(b,text_layer(l1,190,WHITE),W/2,880)
    bw=text_layer(l2,170,INK).width+70
    put(b,yellow_box(bw,200),W/2,1080); put(b,text_layer(l2,170,INK),W/2,1072)
    put(b,text_layer(l3,62,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1280)
    credit(b); b.convert('RGB').save(f'{out}/{len(slides)+2:02d}_question.jpg',quality=93)
    return [cover]+[s[0] for s in slides]+[k]

used_a=build('/home/claude/carrousel_presse_reproche','grassrivers_08','CE QUE LA','PRESSE REPROCHE','à GTA 6, d\'après les premiers tests',
 [('port_gellhorn_06','30 IMAGES/S',['Testé verrouillé à 30 FPS','sur console.'],'Wccftech'),
  ('ambrosia_04','UNE HISTOIRE DISPERSÉE',['Le récit principal se perd','parfois en route.'],'TheSixthAxis'),
  ('grassrivers_02','UN RYTHME INÉGAL',['Des passages plus lents','dans l\'histoire.'],'Noisy Pixel'),
  ('mount_kalaga_05','PERFS EN FIN DE JEU',['Les performances sont au plus bas','vers la fin de l\'aventure.'],'Noisy Pixel'),
  ('ambrosia_02','UN SKIP DISCUTABLE',['Mourir 3 fois au même endroit','permet de sauter le passage.'],'Noisy Pixel')],
 ('leonida_keys_06','ÇA TE GÊNE ?','OUI OU NON','Réponds en commentaire'))
used_b=build('/home/claude/carrousel_presse_adore','vice_city_02','CE QUE LA','PRESSE ADORE','dans GTA 6, d\'après les premiers tests',
 [('vice_city_25','UN MONDE ULTRA DENSE',['Le monde virtuel le plus dense','jamais créé, selon le test.'],'Playday'),
  ('vice_city_21','L\'ÉCRITURE',['Parmi les meilleures','de tout le jeu vidéo.'],'RPGamer'),
  ('vice_city_14','JASON & LUCIA',['Un duo et une relation','qui marquent les testeurs.'],'Noisy Pixel'),
  ('grassrivers_05','167 DISTRIBUTEURS',['167 distributeurs de billets','qu\'on peut arracher et remorquer.'],'Wccftech'),
  ('vice_city_16','LA BANDE-SON',['Bande-son et doublage','salués par la critique.'],'Wccftech')],
 ('mount_kalaga_06','TU L\'AS','PRÉCOMMANDÉ ?','Réponds en commentaire'))
u=json.load(open('used_visuals.json'))
u['videos']['carrousel_presse_reproche']=used_a; u['videos']['carrousel_presse_adore']=used_b
u['used']=sorted(set(u['used']+used_a+used_b)); json.dump(u,open('used_visuals.json','w'),indent=1)
from PIL import Image as I; import glob
for name in ['presse_reproche','presse_adore']:
    fs=sorted(glob.glob(f'/home/claude/carrousel_{name}/*.jpg')); s=I.new('RGB',(225*len(fs),400))
    for i,f in enumerate(fs): s.paste(I.open(f).resize((225,400)),(i*225,0))
    s.save(f'/home/claude/rockstar/sheet_{name}.jpg')

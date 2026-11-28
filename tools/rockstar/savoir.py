import sys; sys.path.insert(0,'/home/claude/rockstar')
from kit2 import *
out='/home/claude/carrousel_6_choses'; os.makedirs(out, exist_ok=True)
S=[('vice_city_10','DÉBLOCAGE À MINUIT',['Heure locale, sur PS5 et Xbox Series X|S.','En France : cette nuit, 00h00.'],'Rockstar Games'),
   ('leonida_keys_05','212 GO À PRÉVOIR',['Le pré-téléchargement demande','jusqu\'à 212 Go selon la console.'],'Rockstar Newswire'),
   ('grassrivers_04','SOLO AU LANCEMENT',['Aucun mode en ligne annoncé','par Rockstar pour l\'instant.'],'Rockstar Games'),
   ('port_gellhorn_01','PAS DE GAME PASS',['GTA 6 ne sera pas dans','le Xbox Game Pass au lancement.'],'Gulf News'),
   ('vice_city_24','UN BONUS À SAISIR',['Vintage Vice City Pack offert','pour tout achat avant le 20 novembre.'],'Gulf News'),
   ('ambrosia_01','PAS DE VERSION PC',['Aucune date PC annoncée.','Consoles uniquement pour l\'instant.'],'Rockstar Games')]
def still(k): return kenburns(k,0.5,True,0.5)
b=still('vice_city_05'); top_fade(b); bottom_fade(b,0.4); header(b,1.0)
put(b,text_layer('6 CHOSES',220,WHITE),W/2,1150)
box=yellow_box(860,210); put(b,box,W/2,1350); put(b,text_layer('À SAVOIR',200,INK),W/2,1342)
put(b,text_layer('avant de lancer GTA 6 cette nuit',66,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1520)
put(b,text_layer('GLISSE >>',56,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1620)
credit(b); b.convert('RGB').save(f'{out}/01_couverture.jpg',quality=93)
for i,(k,t,lines,src) in enumerate(S,start=1):
    b=still(k); top_fade(b); bottom_fade(b,0.42,245); header(b,1.0)
    put(b,text_layer(f'0{i}',300,(0,0,0,0),'Anton-Regular.ttf',stroke=4,stroke_fill=YEL+(230,)),90,1130,'lm')
    put(b,text_layer(t,120,YEL),98,1338,'lm'); put(b,text_layer(t,120,WHITE),90,1330,'lm')
    for j,l in enumerate(lines): put(b,text_layer(l,62,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),90,1450+j*72,'lm')
    put(b,text_layer(f'Source : {src}',40,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),90,1640,'lm')
    credit(b); b.convert('RGB').save(f'{out}/{i+1:02d}_{k}.jpg',quality=93)
b=still('vice_city_09'); b.alpha_composite(Image.new('RGBA',(W,H),INK+(175,))); header(b,1.0)
put(b,text_layer('TU JOUES',200,WHITE),W/2,860)
box=yellow_box(760,210); put(b,box,W/2,1060); put(b,text_layer('À MINUIT ?',190,INK),W/2,1052)
put(b,text_layer('OUI  ou  DEMAIN MATIN',90,YEL),W/2,1260)
put(b,text_layer('Réponds en commentaire  ·  Enregistre ce post',58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1420)
credit(b); b.convert('RGB').save(f'{out}/08_question.jpg',quality=93)
from PIL import Image as I; import glob
fs=sorted(glob.glob(out+'/*.jpg')); s=I.new('RGB',(225*len(fs),400))
for i,f in enumerate(fs): s.paste(I.open(f).resize((225,400)),(i*225,0))
s.save('/home/claude/rockstar/savoir_sheet.jpg')

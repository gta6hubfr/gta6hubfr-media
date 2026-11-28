import sys; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, text_layer, grad_text, put, W, H, YEL, INK, WHITE, Image, ImageDraw, os
OUT='/home/claude/patch'; os.makedirs(OUT,exist_ok=True)
B=lambda s,z=54,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
SB=lambda s,z=46,c=(235,235,240): text_layer(s,z,c,'BarlowCondensed-SemiBoldItalic.ttf')
from logo import badge; BADGE=badge(104)
CR1=SB('Sources : Rockstar Support, Push Square, Wccftech',28,(255,255,255,185)); CR2=SB('Images : @RockstarGames  ·  Page fan, non officielle',28,(255,255,255,185))
def bg(name,dim=150,focus=0.5):
    im=Image.open(f'/home/claude/rockstar/lib2/{name}.jpg').convert('RGB'); s=max(W/im.width,H/im.height)
    im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS); x=int((im.width-W)*focus); im=im.crop((x,(im.height-H)//2,x+W,(im.height-H)//2+H))
    b=im.convert('RGBA'); b.alpha_composite(Image.new('RGBA',(W,H),INK+(dim,))); kit2.top_fade(b,760,235); kit2.bottom_fade(b,0.5,245); return b
def frame(b,lab,idx):
    b.alpha_composite(BADGE,(50,50)); put(b,chip(lab,RED,size=40),W/2,102); put(b,text_layer(idx,36,(255,255,255,215),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    put(b,CR1,W/2,1838); put(b,CR2,W/2,1876)
def check(b,x,y,s=56):
    d=ImageDraw.Draw(b); d.rounded_rectangle((x,y,x+s,y+s),12,fill=YEL)
    d.line([(x+13,y+s*0.52),(x+s*0.42,y+s-15),(x+s-11,y+13)],fill=INK,width=9,joint='curve')
# slide 1
b=bg('jason_and_lucia_06',120); frame(b,'PATCH NOTE · 23 NOV.','1 / 3')
put(b,text_layer('MISE À JOUR',150,WHITE),W/2,330); put(b,grad_text('GTA 6 DISPO',150),W/2,490)
put(b,B('Version 01.002.002 · 7 bugs corrigés',60,YEL),W/2,630)
for i,(k,v) in enumerate([('PS5','603 Mo'),('XBOX SERIES','1,6 Go')]):
    x=W/2+(i*2-1)*250; d=ImageDraw.Draw(b); d.rounded_rectangle((x-220,1380,x+220,1560),28,fill=(11,6,20,215),outline=YEL,width=4)
    put(b,B(k,48,(220,220,230)),x,1430); put(b,text_layer(v,92,WHITE),x,1505)
put(b,B('Swipe pour la liste complète  »',52,WHITE),W/2,1680)
b.convert('RGB').save(f'{OUT}/patch_1.jpg',quality=94)
# slide 2
b=bg('lucia_caminos_09',175); frame(b,'CE QUI EST CORRIGÉ','2 / 3')
put(b,grad_text('7 BUGS EN MOINS',130),W/2,300)
L=[('Plusieurs crashs du jeu',None),('La météo qui restait bloquée',"pendant très longtemps"),('La sauvegarde auto',"qui ne marchait pas bien"),('Les appels qui ne venaient pas',"et bloquaient l'histoire ou des missions"),('Les étoiles impossibles à perdre',"niveau de recherche bloqué"),('La barre de soulevé de terre',"inutilisable à la salle de sport"),('Les partenaires qui gardaient les sacs',"impossibles à revendre au receleur")]
y=450
for t,s in L:
    check(b,70,y-4); tl=B(t,54); b.alpha_composite(tl,(150,y-14))
    if s: b.alpha_composite(SB(s,40,(200,200,210)),(152,y+52)); y+=168
    else: y+=120
b.convert('RGB').save(f'{OUT}/patch_2.jpg',quality=94)
# slide 3
b=bg('jason_duval_07',150); frame(b,'TU NE L’AS PAS ENCORE ?','3 / 3')
put(b,text_layer('PAS DE MAJ ?',140,WHITE),W/2,330); put(b,grad_text('C’EST NORMAL',150),W/2,490)
for i,(t,s) in enumerate([("Elle arrive par vagues","un tiers des joueurs à la fois"),("Jusqu'à 6 h d'attente","pour certains joueurs"),("Redémarre ta console","et relance la recherche de MAJ")]):
    y=760+i*210; check(b,90,y,64); b.alpha_composite(B(t,62),(180,y-14)); b.alpha_composite(SB(s,44,(205,205,215)),(182,y+62))
put(b,B('Quel bug t’a le plus saoulé ? 👇'.replace(' 👇',''),58,YEL),W/2,1470)
put(b,B('Dis-le en commentaire · Abonne-toi pour les prochaines MAJ',42,WHITE),W/2,1545)
b.convert('RGB').save(f'{OUT}/patch_3.jpg',quality=94)

import sys; sys.path.insert(0,'/home/claude/rockstar')
import brief as B
from brief import *
B.C=[('ue_edition_01',True,0.5,'LE PRIX','+20 €','POUR 16 BONUS',['Véhicules, armes, tenues, boutiques','et activités en plus de l\'histoire.'],'SOURCE : VICE'),
   ('ue_grotti_cheetah_02',False,0.45,'LA STAR','CHEETAH','LA \'95 DE GROTTI',['Mais elle ne se débloque qu\'au chapitre 5,','soit environ 60 h de jeu.'],'SOURCES : VICE · DOTESPORTS'),
   ('ue_wyman_car_collection_01',True,0.5,'LE + RARE','WYMAN','DES MISSIONS EN PLUS',['Retrouver des épaves pour les restaurer :','du vrai contenu, pas que du cosmétique.'],'SOURCES : TOM\'S HARDWARE · GAMES.GG'),
   ('ue_safehouse_vehicles_03',False,0.5,'ATTENTION','CHAP. 1','CERTAINS BONUS EXPIRENT',['L\'Enduro, le kayak de Jason et le Ganado Retro','ne servent qu\'au chapitre 1.'],'SOURCE : DOTESPORTS')]
def hook(out):
    d=1.6; t1=text_layer('L\'ULTIMATE À 99,99 €',120,WHITE); t2=grad_text('ÇA VAUT LE COUP ?',128); s=text_layer('Le verdict en 20 secondes',56,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'); L=chip('LE BRIEF : ACHAT',RED,size=46)
    def gen(k):
        t=k/30; b=bgimg('ue_grotti_cheetah_01',t,d,True,0.5); frame_common(b,t,None)
        put(b,L,W/2,1040); z=1+0.05*t; put(b,t1,W/2,1185); put(b,t2.resize((int(t2.width*z),int(t2.height*z))),W/2,1345); put(b,s,W/2,1490)
        return b
    encode('u_hook',gen,int(d*30),out)
def outro(out):
    d=3.0
    def gen(k):
        t=k/30; b=bgimg('ue_squalo_01',t,d,True,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(90,))); frame_common(b,t,None)
        a1=ease_out_cubic(prog(t,0,0.4)); a2=ease_out_back(prog(t,0.15,0.5)); a3=ease_out_cubic(prog(t,0.4,0.4))
        put(b,chip('VERDICT',YEL,INK,50),W/2,1000,alpha=a1)
        put(b,text_layer('OUI, SI TU JOUES',130,WHITE),W/2-(1-a1)*600,1150,alpha=a1)
        put(b,grad_text('SUR LA DURÉE.',150),W/2+(1-clamp(a2))*700,1300,alpha=clamp(a2))
        put(b,text_layer('Standard ou Ultimate : tu as pris laquelle ?',50,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1440,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',54,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1530,alpha=a3)
        return b
    encode('u_out',gen,int(d*30),out)
if __name__=='__main__':
    out='/home/claude/rockstar/ultimate'; os.makedirs(out,exist_ok=True)
    hook(out)
    for i in range(4): B.card(i,out)
    outro(out)
    assemble(['u_hook','b0','b1','b2','b3','u_out'],out,'/home/claude/gta6hubfr_ultimate.mp4')

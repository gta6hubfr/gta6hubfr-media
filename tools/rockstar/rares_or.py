import sys; sys.path.insert(0,'/home/claude/rockstar')
from rares2 import *
OUT='/home/claude/rockstar/rares_or'; os.makedirs(OUT,exist_ok=True)
M=lambda: MAP(360,95,1200,900,640)
KEY='Il te faut le cloneur de clé (chapitre 3)'
S={
 'h0':([(221.25,0.95,CAR(420,580)),(234.3,1.35,CAR(560,580))],'VOITURES RARES · PARTIE 1',None,
       [(text_layer('LES 2 LAMBO',120,WHITE),300,None),(grad_text('EN OR',190),462,None),(B('cachées dans GTA 6 (et où les trouver)',54),600,None)],0),
 'c1':([(232.3,1.9,CAR(470,580)),(235.0,1.7,CAR(520,580))],'VOITURE N°1','1 / 2',
       [(grad_text("L'URUS EN OR",132),330,0),(B('Pegassi Lustrous Toros',56),462,0.15)],0),
 'm1':([(222.3,1.9,M()),(224.3,2.3,M())],'OÙ LA TROUVER','1 / 2',
       [(pin('CASANOVA ISLAND'),300,0),(B('Dans le garage de la grande villa',52),410,0.2),(B("côté sud de l'île",52),470,0.2),(B(KEY,50,YEL),1530,0.9)],0),
 'c2':([(277.0,3.2,CAR(380,580))],'VOITURE N°2','2 / 2',
       [(grad_text('LA HURACÁN EN OR',118),330,0),(B('Pegassi Gold Rush Tempesta',56),462,0.15)],0),
 'm2':([(271.5,1.9,MAP(460,290,1000,750,640)),(273.9,2.3,M())],'OÙ LA TROUVER','2 / 2',
       [(pin('CRIMSON PALMS'),300,0),(B('Le parking couvert de la résidence',52),410,0.2),(B('au bord de la plage',52),470,0.2),(B(KEY,50,YEL),1530,0.9)],0),
 'k':([(281.0,2.3,CAR(380,580))],"L'ASTUCE",None,
       [(grad_text('CLONE LA CLÉ',140),330,0),(B('Pas besoin de casser la vitre',54),465,0.15)],0),
 'o':([(285.4,1.15,CAR(380,580)),(287.45,1.1,CAR(380,580))],'À TOI',None,
       [(text_layer('TU PRENDS',120,WHITE),300,0),(grad_text('LAQUELLE ?',170),455,0.1),(B('Urus ou Huracán : dis-le en commentaire',50),590,0.3),(B('PARTIE 2 DEMAIN : LA FERRARI ET LA K2000',48,YEL),655,0.5),(B('Abonne-toi pour ne pas la rater',46),712,0.7)],70),
}
ORDER=['h0','c1','m1','c2','m2','k','o']
if __name__=='__main__':
    todo=sys.argv[1:] or ORDER
    for n in todo:
        shots,lab,idx,lines,dim=S[n]; scene(n,shots,lab,idx,lines,OUT,dim,hold=0.75 if n=='o' else 0)
    assemble(ORDER,OUT,'/home/claude/gta6hubfr_lambos_or.mp4')

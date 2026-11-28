import sys; sys.path.insert(0,'/home/claude/rockstar')
from rares2 import *
OUT='/home/claude/rockstar/rares_fk'; os.makedirs(OUT,exist_ok=True)
M=lambda: MAP(360,95,1200,900,640)
S={
 'h0':([(169.0,1.3,CAR(560,580)),(64.25,1.2,CAR(340,580))],'VOITURES RARES · PARTIE 2',None,
       [(text_layer('LA FERRARI ET',112,WHITE),300,None),(grad_text('LA K2000',180),462,None),(B('cachées dans GTA 6 (et où les trouver)',54),600,None)],0),
 'c1':([(180.7,2.0,CAR(500,580))],'VOITURE N°1','1 / 2',
       [(grad_text('LA FERRARI DE GTA 6',112),330,0),(B('Grotti Itali RSX, inspirée de la SF90',54),460,0.15)],0),
 'f1':([(184.3,2.4,PANEL(480,0,1440,1080,640))],'SA FICHE','1 / 2',
       [(grad_text('CLÉ CLONÉE',140),330,0),(B('Alarme + traceur avancé',56),462,0.15),(B('Ne ralentis pas, sinon la police arrive',50,YEL),1530,0.6)],0),
 'm1':([(172.1,1.9,M()),(174.7,2.3,M())],'OÙ LA TROUVER','1 / 2',
       [(pin('VESPUCCI ISLAND'),300,0),(B("Dans un garage de l'île",52),410,0.2),(B('Il te faut le cloneur de clé (chapitre 3)',50,YEL),1530,0.9)],0),
 'c2':([(59.8,2.0,CAR(500,580)),(62.65,1.5,CAR(800,580))],'VOITURE N°2','2 / 2',
       [(grad_text('LA K2000 DE GTA 6',118),330,0),(B('Imponte Ruiner Turbo : compresseur + nitro',50),460,0.15)],0),
 'm2':([(55.3,1.85,M()),(57.2,2.5,M())],'OÙ LA TROUVER','2 / 2',
       [(pin('KEY LENTO'),300,0),(B("Surfside Dr, dans l'allée d'une maison",52),410,0.2),(B('à une minute de chez Jason',52),470,0.2),(B('Pas besoin de cloneur : casse la vitre',50,YEL),1530,0.9)],0),
 'o':([(182.85,1.4,CAR(500,580)),(65.45,1.05,CAR(340,580))],'À TOI',None,
       [(text_layer('TU PRENDS',120,WHITE),300,0),(grad_text('LAQUELLE ?',170),455,0.1),(B('Ferrari ou K2000 : dis-le en commentaire',50),590,0.3),(B('ABONNE-TOI @GTA6HUBFR_',54,YEL),655,0.5)],70),
}
ORDER=['h0','c1','f1','m1','c2','m2','o']
if __name__=='__main__':
    todo=sys.argv[1:] or ORDER
    for n in todo:
        shots,lab,idx,lines,dim=S[n]; scene(n,shots,lab,idx,lines,OUT,dim,hold=0.45 if n=='o' else 0)
    assemble(ORDER,OUT,'/home/claude/gta6hubfr_ferrari_k2000.mp4')

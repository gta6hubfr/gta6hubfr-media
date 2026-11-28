import sys; sys.path.insert(0,'/home/claude/rockstar')
from style2 import *
out='/home/claude/carrousel_presse_adore'; import shutil; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
S=[('vice_city_02','CE QUE LA PRESSE','ADORE DANS GTA 6.',['Les 5 points qui reviennent','dans les premiers tests.'],None),
   ('vice_city_25','UN MONDE','ULTRA DENSE.',['Le monde virtuel le plus dense','jamais créé, selon Playday.'],'Playday · 18 nov. 2026'),
   ('vice_city_21','UNE ÉCRITURE','AU SOMMET.',['Parmi les meilleures de tout','le jeu vidéo, d\'après RPGamer.'],'RPGamer · 18 nov. 2026'),
   ('vice_city_14','JASON & LUCIA,','LE DUO QUI MARQUE.',['Leur relation est l\'un des','points forts salués par Noisy Pixel.'],'Noisy Pixel · 18 nov. 2026'),
   ('grassrivers_05','167 DISTRIBUTEURS','À REMORQUER.',['Wccftech en a compté 167 qu\'on','peut arracher et emporter.'],'Wccftech · 18 nov. 2026'),
   ('vice_city_16','UNE BANDE-SON','DE HAUT VOL.',['Musique et doublage','salués par la critique.'],'Wccftech · 18 nov. 2026')]
for i,(bg,a,b,body,src) in enumerate(S):
    slide(bg,a,b,body,src,f'{out}/{i+1:02d}.jpg',i+1 if i else None,7)
end_slide('mount_kalaga_06','TU L\'AS','PRÉCOMMANDÉ ?','RÉPONDS EN COMMENTAIRE  ·  ABONNE-TOI @GTA6HUBFR_',f'{out}/07.jpg')
from PIL import Image as I; import glob
fs=sorted(glob.glob(out+'/*.jpg')); s=I.new('RGB',(240*len(fs),427))
for i,f in enumerate(fs): s.paste(I.open(f).resize((240,427)),(i*240,0))
s.save('/home/claude/apercu_presse_adore_v2.jpg',quality=88)

import sys; sys.path.insert(0,'/home/claude/rockstar')
from style2 import *
out='/home/claude/carrousel_presse_reproche'; import shutil; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
S=[('grassrivers_08','CE QUE LA PRESSE','REPROCHE À GTA 6.',['Les 5 bémols relevés','dans les premiers tests.'],None),
   ('port_gellhorn_06','30 IMAGES','PAR SECONDE.',['Testé verrouillé à 30 FPS','sur console par Wccftech.'],'Wccftech · 18 nov. 2026'),
   ('ambrosia_04','UNE HISTOIRE','QUI S\'ÉPARPILLE.',['Le récit principal se perd','parfois en route, selon TheSixthAxis.'],'TheSixthAxis · 18 nov. 2026'),
   ('grassrivers_02','UN RYTHME','INÉGAL.',['Des passages plus lents','dans l\'histoire, note Noisy Pixel.'],'Noisy Pixel · 18 nov. 2026'),
   ('mount_kalaga_05','DES PERFS','EN BAISSE À LA FIN.',['Les performances sont au plus bas','vers la fin de l\'aventure.'],'Noisy Pixel · 18 nov. 2026'),
   ('ambrosia_02','UN SKIP','DISCUTABLE.',['Mourir 3 fois au même endroit','permet de sauter le passage.'],'Noisy Pixel · 18 nov. 2026')]
for i,(bg,a,b,body,src) in enumerate(S):
    slide(bg,a,b,body,src,f'{out}/{i+1:02d}.jpg',i+1 if i else None,7)
end_slide('leonida_keys_06','ÇA TE','GÊNE ?','OUI OU NON EN COMMENTAIRE  ·  ABONNE-TOI @GTA6HUBFR_',f'{out}/07.jpg')
from PIL import Image as I; import glob
fs=sorted(glob.glob(out+'/*.jpg')); s=I.new('RGB',(240*len(fs),427))
for i,f in enumerate(fs): s.paste(I.open(f).resize((240,427)),(i*240,0))
s.save('/home/claude/apercu_presse_reproche_v2.jpg',quality=88)

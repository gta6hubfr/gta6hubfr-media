import sys; sys.path.insert(0,'/home/claude/rockstar')
import kit2; kit2.LIB='/home/claude/rockstar/lib2/'
import erreurs as E
from erreurs import *
IMG={100:('jason_and_lucia_09',True,0.55),0:('jason_duval_11',False,0.5),3:('lucia_caminos_05',True,0.42),6:('jason_and_lucia_06',False,0.62),9:('jason_and_lucia_08',True,0.5)}
D_HOOK=0
def bg(t,pal,seed):
    name,zin,pan=IMG.get(seed,('jason_and_lucia_08',True,0.5))
    dur={100:1.6,9:2.6}.get(seed,4.4)
    b=kit2.kenburns(name,min(1,t/dur),zin,pan)
    b.alpha_composite(Image.new('RGBA',(W,H),INK+(70,)))
    kit2.top_fade(b,400,170)
    kit2.bottom_fade(b,0.3,250); return b
E.bg=bg
# hook: text lower so faces stay visible
def hook(out):
    d=1.6; t1=text_layer('3 ERREURS',190,WHITE); t2=grad_text('QUE TU FAIS DÉJÀ.',120); s=text_layer('dans GTA 6',64,WHITE,'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=bg(t,None,100); E.corner(b,None); E.pill(b,1)
        z=1+0.04*t; put(b,t1.resize((int(t1.width*z),int(t1.height*z))),W/2,1220); put(b,t2,W/2,1380); put(b,s,W/2,1500)
        return b
    encode('e_hook',gen,int(d*30),out)
E.hook=hook
if __name__=='__main__':
    out='/home/claude/rockstar/erreurs2'; os.makedirs(out,exist_ok=True)
    # shift error text block lower to free faces
    src=open('erreurs.py').read()
    hook(out)
    for i in range(3): E.err(i,out)
    E.outro(out)
    assemble(['e_hook','e0','e1','e2','e_out'],out,'/home/claude/gta6hubfr_3_erreurs.mp4')

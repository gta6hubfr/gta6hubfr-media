import sys, os, subprocess, numpy as np; sys.path.insert(0,'/home/claude/rockstar')
from style2 import *
C='/home/claude/clips_raw/'
CH=[('Jason_Duval','JASON DUVAL','LE PROTAGONISTE.',['Il rêve d\'une vie facile,','mais tout se complique.']),
    ('Lucia_Caminos','LUCIA CAMINOS','LA PROTAGONISTE.',['Partenaire de Jason dans un coup','qui tourne mal.']),
    ('Cal_Hampton','CAL HAMPTON','L\'AMI DE JASON.',['Il préfère écouter la radio','des garde-côtes depuis chez lui.']),
    ('Boobie_Ike','BOOBIE IKE','LA LÉGENDE LOCALE.',['Immobilier, club, studio :','un empire à Vice City.']),
    ('DreQuan_Priest','DRE\'QUAN PRIEST','LE PATRON DE LABEL.',['Il vient de signer Real Dimez','sur Only Raw Records.']),
    ('Real_Dimez','REAL DIMEZ','LE DUO DE RAP.',['Bae-Luxe et Roxy, la nouvelle','signature du label.']),
    ('Raul_Bautista','RAUL BAUTISTA','LE BRAQUEUR.',['Un vétéran des banques qui','recrute pour les gros coups.']),
    ('Brian_Heder','BRIAN HEDER','LE VIEUX CONTREBANDIER.',['Il loge Jason gratuitement,','en échange de petits services.'])]
DUR=3.4
def frames(clip, dur, slow):
    cmd=['ffmpeg','-loglevel','error','-i',C+clip,'-vf',f'scale=-2:1920,crop=1080:1920,setpts={slow}*PTS,minterpolate=fps=30:mi_mode=blend,eq=brightness=-0.02',
         '-t',str(dur),'-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE); n=int(dur*30); out=[]
    last=None
    for i in range(n):
        buf=p.stdout.read(W*H*3)
        if len(buf)<W*H*3: break
        last=Image.frombytes('RGB',(W,H),buf); out.append(last)
    p.stdout.close(); p.wait()
    while len(out)<n: out.append(last)
    return out
def encode(name, gen, n, outdir):
    tmp=f'{outdir}/{name}.tmp.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(gen(k).convert('RGB').tobytes())
    p.stdin.close(); assert p.wait()==0; os.replace(tmp,f'{outdir}/{name}.mp4')
def corner(b,idx):
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    if idx: put(b,text_layer(idx,36,(255,255,255,210),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    put(b,text_layer('Images : @RockstarGames  ·  Page fan, non officielle',28,(255,255,255,130),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1830)
L1={}; 
def char_scene(i,outdir):
    key,name,role,desc=CH[i]; fr=frames(key+'_Video_Clip.mp4',DUR,3.2)
    t1=text_layer(name,124,WHITE); t2=grad_text(role,110 if len(role)<18 else 92)
    ds=[text_layer(l,50,(235,235,240),'BarlowCondensed-SemiBoldItalic.ttf') for l in desc]
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); bottom_fade(b,0.42,245); corner(b,f'{i+1} / 8')
        a1=ease_out_cubic(prog(t,0.15,0.7)); a2=ease_out_cubic(prog(t,0.3,0.7)); a3=ease_out_cubic(prog(t,0.7,0.6))
        e=ease_in_cubic(prog(t,DUR-0.3,0.3))
        put(b,t1,W/2-(1-a1)*600-e*1200,1240,alpha=a1); put(b,t2,W/2+(1-a2)*600-e*1200,1365,alpha=a2)
        for j,dl in enumerate(ds): put(b,dl,W/2,1480+j*62+(1-a3)*25,alpha=a3*(1-e))
        return b
    encode(f'v{i}',gen,int(DUR*30),outdir)
def intro(outdir):
    d=3.2; fr=frames('Lucia_Caminos_Video_Clip.mp4',d,3.6)
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); b.alpha_composite(Image.new('RGBA',(W,H),INK+(120,))); bottom_fade(b,0.35,240); corner(b,None)
        a1=ease_out_cubic(prog(t,0.1,0.7)); a2=ease_out_back(prog(t,0.35,0.8)); a3=ease_out_cubic(prog(t,0.9,0.6))
        put(b,text_layer('LES 8 VISAGES',150,WHITE),W/2-(1-a1)*700,1180,alpha=a1)
        put(b,grad_text('DE GTA 6.',190),W/2+(1-clamp(a2))*800,1340,alpha=clamp(a2))
        put(b,text_layer('Les personnages officiels à connaître',56,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1480,alpha=a3)
        return b
    encode('v_intro',gen,int(d*30),outdir)
def outro(outdir):
    d=3.4; bg=kenburns('vice_city_04',0.5,False,0.5) if os.path.exists(LIB+'vice_city_04.jpg') else None
    def gen(k):
        t=k/30; b=kenburns('vice_city_04',t/d,False,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(185,))); corner(b,None)
        a1=ease_out_cubic(prog(t,0.1,0.7)); a2=ease_out_back(prog(t,0.35,0.8)); a3=ease_out_cubic(prog(t,0.9,0.6))
        put(b,text_layer('TON PERSO',160,WHITE),W/2-(1-a1)*700,840,alpha=a1)
        put(b,grad_text('PRÉFÉRÉ ?',170),W/2+(1-clamp(a2))*800,1000,alpha=clamp(a2))
        put(b,text_layer('Dis-le en commentaire',60,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1180,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',50,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1270,alpha=a3)
        return b
    encode('v_outro',gen,int(d*30),outdir)
if __name__=='__main__':
    out='/home/claude/rockstar/visages'; os.makedirs(out,exist_ok=True)
    if sys.argv[1]=='test':
        key,name,role,desc=CH[2]; fr=frames(key+'_Video_Clip.mp4',DUR,3.2)
        b=fr[60].convert('RGBA'); bottom_fade(b,0.42,245); corner(b,'3 / 8')
        put(b,text_layer(name,124,WHITE),W/2,1240); put(b,grad_text(role,110),W/2,1365)
        for j,l in enumerate(desc): put(b,text_layer(l,50,(235,235,240),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1480+j*62)
        b.convert('RGB').resize((540,960)).save('/home/claude/rockstar/vis_test.jpg'); print(len(fr))
    else:
        intro(out)
        for i in range(8): char_scene(i,out)
        outro(out)
        assemble(['v_intro']+[f'v{i}' for i in range(8)]+['v_outro'],out,'/home/claude/gta6hubfr_8_visages.mp4')

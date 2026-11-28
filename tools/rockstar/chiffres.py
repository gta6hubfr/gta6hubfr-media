import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_cubic, ease_out_back, ease_in_cubic, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
D='/home/claude/opus/drive/'
CRED='Gameplay : @VicePeek (YouTube)  ·  Page fan, non officielle'
def frames(f,ss,dur):
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-i',D+f,'-t',str(dur),'-vf','fps=30','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[];n=int(round(dur*30))
    while len(out)<n:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait()
    while len(out)<n: out.append(out[-1])
    return out
DARK=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(DARK)
dd.rectangle((0,0,W,553),fill=INK+(185,)); dd.rectangle((0,1366,W,H),fill=INK+(200,))
dd.rectangle((0,551,W,557),fill=YEL+(255,)); dd.rectangle((0,1363,W,1369),fill=YEL+(255,))
def base(fr,idx):
    b=fr.convert('RGBA'); b.alpha_composite(DARK)
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    put(b,chip('GTA 6 EN CHIFFRES',RED,size=36),W/2,102)
    if idx: put(b,text_layer(idx,36,(255,255,255,210),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    put(b,text_layer(CRED,28,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1860)
    return b
C=[('bridge.mp4',3,4.2,'212 GO','À TÉLÉCHARGER',['Fais de la place sur ta console','avant d\'installer le jeu.'],'SOURCES : TECH TIMES · SIXWANTED'),
   ('catalan.mp4',1,4.2,'99/100','SUR METACRITIC',['Le record absolu, à égalité avec','Zelda : Ocarina of Time.'],'SOURCE : METACRITIC'),
   ('exit.mp4',3,4.2,'24,6 M','VENDUS EN 24 H',['Pour 2,36 milliards de dollars :','le plus gros lancement de l\'histoire.'],'SOURCE : SENSOR TOWER VIA DEADLINE'),
   ('palms.mp4',4,4.2,'75 %','SUR PLAYSTATION',['Les 25 % restants','sur Xbox Series.'],'SOURCE : SENSOR TOWER VIA DEADLINE'),
   ('sunset.mp4',12,4.2,'3,29 M','SUR TWITCH',['Spectateurs en même temps :','record pour un jeu sur la plateforme.'],'SOURCE : UA NEWS')]
def card(i,out):
    f,ss,d,big,sub,body,src=C[i]; fr=frames(f,ss,d)
    BIG=grad_text(big,260); S=text_layer(sub,92,WHITE); ds=[text_layer(x,52,(240,240,245),'BarlowCondensed-SemiBoldItalic.ttf') for x in body]; sr=text_layer(src,28,(200,200,210,190),'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=base(fr[k],f'{i+1} / 5')
        a1=ease_out_back(prog(t,0,0.45)); a2=ease_out_cubic(prog(t,0.2,0.45)); a3=ease_out_cubic(prog(t,0.45,0.4)); e=ease_in_cubic(prog(t,d-0.25,0.25))
        z=0.8+0.2*clamp(a1); put(b,BIG.resize((max(1,int(BIG.width*z)),max(1,int(BIG.height*z)))),W/2,300,alpha=clamp(a1)*(1-e))
        put(b,S,W/2+(1-a2)*500-e*1100,470,alpha=a2)
        for j,x in enumerate(ds): put(b,x,W/2,1480+j*66+(1-a3)*20,alpha=a3*(1-e))
        put(b,sr,W/2,1660,alpha=a3*(1-e))
        return b
    encode(f'c{i}',gen,len(fr),out)
def hook(out):
    d=1.8; fr=frames('sunset.mp4',0,d); T1=text_layer('GTA 6 :',150,WHITE); T2=grad_text('5 CHIFFRES FOUS.',140); s=text_layer('Les vrais chiffres du lancement',58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=base(fr[k],None); z=1+0.04*t
        put(b,T1,W/2,300); put(b,T2.resize((int(T2.width*z),int(T2.height*z))),W/2,455); put(b,s,W/2,1500); return b
    encode('c_hook',gen,len(fr),out)
def outro(out):
    d=3.0; fr=frames('sunset.mp4',24,d)
    def gen(k):
        t=k/30; b=base(fr[k],None)
        a1=ease_out_cubic(prog(t,0,0.4)); a2=ease_out_back(prog(t,0.15,0.5)); a3=ease_out_cubic(prog(t,0.4,0.4))
        put(b,text_layer('LEQUEL',140,WHITE),W/2-(1-a1)*600,300,alpha=a1)
        put(b,grad_text('T\'IMPRESSIONNE ?',130),W/2+(1-clamp(a2))*700,455,alpha=clamp(a2))
        put(b,text_layer('Dis-le en commentaire',60,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1490,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',56,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1590,alpha=a3)
        return b
    encode('c_out',gen,len(fr),out)
if __name__=='__main__':
    out='/home/claude/rockstar/chiffres'; os.makedirs(out,exist_ok=True)
    hook(out); [card(i,out) for i in range(5)]; outro(out)
    assemble(['c_hook']+[f'c{i}' for i in range(5)]+['c_out'],out,'/home/claude/gta6hubfr_chiffres.mp4')

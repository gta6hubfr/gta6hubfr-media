import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_cubic, ease_out_back, ease_in_cubic, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
O='/home/claude/opus/'
CRED='Gameplay : @Hazardous (YouTube)  ·  Page fan, non officielle'
def frames(f,ss,dur,raw=False):
    vf='crop=608:1080:656:0,scale=1080:1920:flags=lanczos,fps=30'
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-i',O+f,'-t',str(dur),'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[];n=int(dur*30)
    while len(out)<n:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close();p.wait()
    while len(out)<n: out.append(out[-1])
    return out
def common(b,idx):
    bd=Image.new('RGBA',(84,84),(0,0,0,0)); d=ImageDraw.Draw(bd); d.rounded_rectangle((0,0,83,83),16,fill=YEL)
    g=text_layer('G6',56,INK); bd.alpha_composite(g,((84-g.width)//2,(84-g.height)//2-2)); b.alpha_composite(bd,(60,60))
    put(b,chip('ASTUCE GAMEPLAY',RED,size=36),W/2,102)
    if idx: put(b,text_layer(idx,36,(255,255,255,210),'BarlowCondensed-ExtraBoldItalic.ttf'),1020,102,'rm')
    kit2.bottom_fade(b,0.88,200)
    put(b,text_layer(CRED,28,(255,255,255,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1860)
def prep(fr,top=True):
    b=fr.convert('RGBA')
    if top: kit2.top_fade(b,900,235)
    return b
S=[('brut.mp4',195.0,4.0,'NOUVEAU','UN ONGLET','STUNT JUMPS',['Carte > Exploration : tous tes sauts','trouvés et réussis.']),
   ('brut.mp4',84.45,6.4,'CHANGEMENT','CHAQUE SAUT','A SON DÉFI',['Passer au-dessus d\'un bateau, backflip','à travers le panneau Black Hole…']),
   ('brut.mp4',70.0,5.0,'ASTUCE','BACKFLIP :','GARDE LE STICK',['Contrairement à GTA V, la rotation','ne se termine pas toute seule.']),
   ('brut.mp4',358.0,8.0,'DÉFI','LE PARKING','DE L\'AÉROPORT',['Prends un max d\'élan sur le toit','et vise juste.'])]
def seg(i,out):
    f,ss,d,lab,l1,l2,body=S[i]; fr=frames(f,ss,d); dy=0
    L=chip(lab,YEL,INK,44); T1=text_layer(l1,120,WHITE); T2=grad_text(l2,130 if len(l2)<13 else 110)
    ds=[text_layer(x,50,(240,240,245),'BarlowCondensed-SemiBoldItalic.ttf') for x in body]
    def gen(k):
        t=k/30; b=prep(fr[k]); common(b,f'{i+1} / 4')
        a0=ease_out_back(prog(t,0,0.4)); a1=ease_out_cubic(prog(t,0.1,0.45)); a2=ease_out_back(prog(t,0.25,0.5)); a3=ease_out_cubic(prog(t,0.55,0.4)); e=ease_in_cubic(prog(t,d-0.25,0.25))
        put(b,L,W/2-(1-clamp(a0))*400,300+dy,alpha=clamp(a0)*(1-e))
        put(b,T1,W/2-(1-a1)*600-e*1200,430+dy,alpha=a1); put(b,T2,W/2+(1-clamp(a2))*700-e*1200,570+dy,alpha=clamp(a2))
        for j,x in enumerate(ds): put(b,x,W/2,690+dy+j*60+(1-a3)*20,alpha=a3*(1-e))
        return b
    encode(f's{i}',gen,len(fr),out)
def hook(out):
    d=2.0; fr=frames('brut.mp4',342.5,d); T1=text_layer('STUNT JUMPS :',150,WHITE); T2=grad_text('TOUT A CHANGÉ.',128); s=text_layer('4 trucs à savoir dans GTA 6',58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=prep(fr[k]); common(b,None); z=1+0.04*t
        put(b,T1,W/2,420); put(b,T2.resize((int(T2.width*z),int(T2.height*z))),W/2,580); put(b,s,W/2,710); return b
    encode('s_hook',gen,len(fr),out)
def outro(out):
    d=5.0; fr=frames('brut.mp4',385.1,d)
    def gen(k):
        t=k/30; b=prep(fr[k]); b.alpha_composite(Image.new('RGBA',(W,H),INK+(90,))); common(b,None)
        a1=ease_out_cubic(prog(t,0,0.4)); a2=ease_out_back(prog(t,0.15,0.5)); a3=ease_out_cubic(prog(t,0.4,0.4))
        put(b,text_layer('TU EN AS RÉUSSI',130,WHITE),W/2-(1-a1)*600,430,alpha=a1)
        put(b,grad_text('COMBIEN ?',170),W/2+(1-clamp(a2))*700,590,alpha=clamp(a2))
        put(b,text_layer('Dis-le en commentaire  ·  Enregistre pour ta session',50,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,730,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',54,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,820,alpha=a3)
        return b
    encode('s_out',gen,len(fr),out)
if __name__=='__main__':
    out='/home/claude/rockstar/stunts'; os.makedirs(out,exist_ok=True)
    hook(out); [seg(i,out) for i in range(4)]; outro(out)
    assemble(['s_hook','s0','s1','s2','s3','s_out'],out,'/home/claude/gta6hubfr_stunts.mp4')

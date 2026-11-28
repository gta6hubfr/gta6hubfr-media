import sys, subprocess; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, grad_text, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os, assemble
SRC='/home/claude/opus/dasbro/rares16.mp4'
CRED1='Gameplay : DaSbro Tutorial (YouTube)  ·  Infos : JV.com, Sportskeeda, Game8'
CRED2='Images : @RockstarGames  ·  Page fan, non officielle'
LOOK='eq=contrast=1.18:brightness=0.02:saturation=1.35:gamma=1.18'
def PANEL(x,y,w,h,py,bgx=None):
    bgx=x+(w-608)//2 if bgx is None else bgx; bgx=max(0,min(1920-608,bgx))
    return (f'fps=30,{LOOK},split[a][b];[a]crop=608:1080:{bgx}:0,scale=1080:1920,boxblur=28:2,eq=brightness=-0.3[bg];'
            f'[b]crop={w}:{h}:{x}:{y},scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:{py}')
CAR=lambda x,py=520: PANEL(x,0,864,1080,py)          # 4:5 -> 1080x1350
MAP=lambda x,y,w=1280,h=960,py=620: PANEL(x,y,w,h,py)  # 4:3 -> 1080x810
def frames(shots):
    out=[]
    for ss,dur,vf in shots:
        p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur),'-i',SRC,'-filter_complex',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        n=0
        while n<round(dur*30):
            b=p.stdout.read(W*H*3)
            if len(b)<W*H*3: break
            out.append(Image.frombytes('RGB',(W,H),b)); n+=1
        p.stdout.close(); p.wait()
    return out
B=lambda s,z=54,c=WHITE: text_layer(s,z,c,'BarlowCondensed-ExtraBoldItalic.ttf')
from logo import badge; BADGE=badge(104)
C1=text_layer(CRED1,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf'); C2=text_layer(CRED2,26,(255,255,255,175),'BarlowCondensed-SemiBoldItalic.ttf')
def pin(txt,size=60):
    t=B(txt,size,INK); w,h=t.width+70,t.height+20
    L=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(L); d.rounded_rectangle((0,0,w-1,h-1),14,fill=YEL)
    cx,cy=30,h//2; d.ellipse((cx-13,cy-17,cx+13,cy+9),fill=INK); d.polygon([(cx-11,cy-1),(cx+11,cy-1),(cx,cy+19)],fill=INK); d.ellipse((cx-5,cy-10,cx+5,cy),fill=YEL)
    L.alpha_composite(t,(56,10)); return L
def scene(name,shots,lab,idx,lines,out,dim=0,flash=False,hold=0):
    fr=frames(shots); fr+= [fr[-1]]*int(hold*30); L=chip(lab,RED,size=38); I=text_layer(idx,36,(255,255,255,215),'BarlowCondensed-ExtraBoldItalic.ttf') if idx else None
    def gen(k):
        t=k/30; b=fr[k].convert('RGBA'); kit2.top_fade(b,720,235)
        if dim: b.alpha_composite(Image.new('RGBA',(W,H),INK+(dim,)))
        b.alpha_composite(BADGE,(50,50)); put(b,L,W/2,102)
        if I: put(b,I,1020,102,'rm')
        kit2.bottom_fade(b,0.16,200); put(b,C1,W/2,1838); put(b,C2,W/2,1874)
        for Lx,y,st in lines:
            a=1 if st is None else clamp(ease_out_back(prog(t,st,0.35)))
            put(b,Lx,W/2+(1-a)*500,y,alpha=a)
        return b
    encode(name,gen,len(fr),out)

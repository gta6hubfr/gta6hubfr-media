import sys, subprocess, re, json; sys.path.insert(0,'/home/claude/rockstar')
import kit2
from brief import chip, RED, encode, text_layer, put, ease_out_back, prog, clamp, W, H, YEL, INK, WHITE, Image, ImageDraw, os
SRC='/home/claude/opus/ps5/ps5_comet_s2.mp4'
OUT='/home/claude/rockstar/vovoit'; os.makedirs(OUT,exist_ok=True)
COVER=lambda cx: f'fps=30,crop=608:1080:{cx}:0,scale=1080:1920:flags=lanczos'
def PANEL(x,y,w,h,pw,py):
    px=(1080-pw)//2
    return (f'fps=30,split[a][b];[a]crop=608:1080:656:0,scale=1080:1920,boxblur=24:2,eq=brightness=-0.25[bg];'
            f'[b]crop={w}:{h}:{x}:{y},scale={pw}:-2:flags=lanczos[fg];[bg][fg]overlay={px}:{py}')
# (texte, début s, durée s) donnés par vidIQ ; plan gameplay associé
LINES=[
 ("Cinq trucs que personne ne te dit sur les voitures de GTA 6.",0,3.787755,(140.0,COVER(656))),
 ("Un. En roulant, t'as un menu véhicule complet.",3.787755,3.004082,(3.0,PANEL(440,20,1080,300,1080,1090))),
 ("Radio, phares, warning, toit : tout se règle sans descendre.",6.791837,4.597551,(7.0,PANEL(440,20,1080,300,1080,1090))),
 ("Deux. Chaque voiture a sa fiche : accès, sécurité, et surtout le traceur.",11.389388,5.720816,(9.5,PANEL(1300,620,620,440,900,1030))),
 ("S'il y en a un, il peut signaler la voiture volée aux flics, même si personne ne t'a vu.",17.110204,4.597551,(59.0,COVER(656))),
 ("Trois. Sur une décapotable, le toit se replie pour de vrai.",21.707755,3.866122,(52.4,COVER(656))),
 ("Quatre. Le sable de la plage, c'est un terrain de drift.",25.573878,3.63102,(104.5,COVER(600))),
 ("Et les passants s'écartent en catastrophe.",29.204898,2.429388,(108.6,COVER(520))),
 ("Cinq. Une voiture garée, selon sa sécurité, il te faut des outils pour la voler.",31.634286,5.067755,(155.5,COVER(600))),
 ("Mais si quelqu'un est au volant, tu le sors, et c'est réglé.",36.702041,3.239184,(163.6,COVER(400))),
 ("Abonne-toi, et dis-moi en commentaire ta caisse préférée.",39.941224,3.082449,(171.0,COVER(656))),
]
TAIL=0.45
NUMS={'UN','DEUX','TROIS','QUATRE','CINQ'}
TIPS={1,3,5,6,8}
SPEECH=json.load(open(OUT+'/speech.json')) if os.path.exists(OUT+'/speech.json') else None
def word_times():
    """Découpe chaque ligne en mots ; temps proportionnels aux lettres, pauses aux ponctuations.
    Si speech.json existe (segments de parole détectés dans l'audio), on cale les phrases dessus."""
    out=[]
    for li,(txt,s,d,_) in enumerate(LINES):
        toks=txt.replace('GTA 6','GTA\u00a06').split(' ')
        def w(tok):
            core=re.sub(r'[^\wÀ-ÿ\']','',tok); p=2.5 if tok[-1] in ',' else (4 if tok[-1] in '.:;?!' else 0)
            return len(core)+1.5, p
        segs=None
        if SPEECH: segs=[x for x in SPEECH if x[0]<s+d-0.02 and x[1]>s+0.02]
        a,b=s+0.06,s+d-0.22
        if segs: a,b=max(segs[0][0],s),min(segs[-1][1],s+d)
        ws=[w(t) for t in toks]; tot=sum(x+p for x,p in ws)-ws[-1][1]
        t=a
        for tok,(x,p) in zip(toks,ws):
            dur=(b-a)*x/tot; out.append([tok,t,li]); t+=dur+(b-a)*p/tot
    return out
def chunks():
    ws=word_times(); res=[]; i=0
    while i<len(ws):
        tok,t,li=ws[i]; up=re.sub(r'[.,:;!?]','',tok).upper()
        isnum = up in NUMS and li in TIPS and (i==0 or ws[i-1][2]!=li)
        grp=[tok]; j=i+1
        if not isnum:
            while j<len(ws) and len(grp)<2 and ws[j][2]==li:
                if len(' '.join(grp+[ws[j][0]]))>14 or tok[-1] in '.,:;!?': break
                grp.append(ws[j][0]); tok=ws[j][0]; j+=1
        res.append((' '.join(grp),t,isnum)); i=j
    end=LINES[-1][1]+LINES[-1][2]+TAIL
    return [(c,t,(res[k+1][1] if k+1<len(res) else end),n) for k,(c,t,n) in enumerate(res)]
CH=chunks()
_cache={}
def cap(txt,num):
    k=(txt,num)
    if k not in _cache:
        s=re.sub(r'[.,:;!?]','',txt).upper()
        if num: s='#'+{'UN':'1','DEUX':'2','TROIS':'3','QUATRE':'4','CINQ':'5'}[s]
        _cache[k]=text_layer(s,150 if num else 118,YEL if num else WHITE,'BarlowCondensed-ExtraBoldItalic.ttf',stroke=9,stroke_fill=(0,0,0,255))
    return _cache[k]
BADGE=Image.new('RGBA',(84,84),(0,0,0,0)); ImageDraw.Draw(BADGE).rounded_rectangle((0,0,83,83),16,fill=YEL)
_g=text_layer('G6',56,INK,'BarlowCondensed-ExtraBoldItalic.ttf'); BADGE.alpha_composite(_g,((84-_g.width)//2,(84-_g.height)//2-2))
C1=text_layer('Gameplay : capture PS5 GTA6 Hub FR  ·  Infos : GTABase, GTABoom  ·  Page fan, non officielle',26,(255,255,255,180),'BarlowCondensed-SemiBoldItalic.ttf')
def frames(ss,dur,vf):
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(ss),'-t',str(dur+0.1),'-i',SRC,'-filter_complex',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]; n=round(dur*30)
    while len(out)<n:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(Image.frombytes('RGB',(W,H),b))
    p.stdout.close(); p.wait()
    while len(out)<n: out.append(out[-1])
    return out
def scene(i):
    txt,s,d,(ss,vf)=LINES[i]
    if i==len(LINES)-1: d+=TAIL
    t0=round(s*30)/30; n=round((s+d)*30)-round(s*30)
    fr=frames(ss,n/30,vf)
    def gen(k):
        t=t0+k/30; b=fr[k].convert('RGBA')
        kit2.bottom_fade(b,0.9,200); b.alpha_composite(BADGE,(60,60)); put(b,C1,W/2,1868)
        for c,a,e,num in CH:
            if a<=t<e:
                L=cap(c,num); sc=0.86+0.14*clamp(ease_out_back(prog(t,a,0.12)))
                if sc<0.999: L=L.resize((max(1,int(L.width*sc)),max(1,int(L.height*sc))))
                put(b,L,W/2,880)
        return b
    encode(f'l{i:02d}',gen,n,OUT)
if __name__=='__main__':
    todo=[int(x) for x in sys.argv[1:]] or range(len(LINES))
    for i in todo: scene(i)

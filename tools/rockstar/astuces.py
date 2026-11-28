import sys; sys.path.insert(0,'/home/claude/rockstar')
from visages import *
T=[('vice_city_12','CACHE TON','CASH.',['Mort ou arrêté, tu perds ton liquide.','Planque-le sous le plancher chez Jason.'],True,0.55),
   ('leonida_keys_04','SAUVEGARDE','À LA MAIN.',['Pas de rejeu de mission :','sauvegarde avant chaque gros coup.'],False,0.4),
   ('vice_city_19','CHANGE DE','TENUE.',['La police retient tes habits et ta voiture.','Change les deux pour la semer.'],True,0.45),
   ('leonida_keys_03','UTILISE LE','FOCUS.',['Vise une porte avant d\'entrer :','blanc = OK, rouge = alarme.'],False,0.5),
   ('grassrivers_07','NOURRIS','DOLORES.',['Une souris pour le serpent de Jason','= bonus de Focus.'],True,0.35),
   ('grassrivers_03','LUCIA ARRIVE','PLUS TARD.',['Switch libre au chapitre 2 (mission Coffee Break) :','croix droite + R1 / RB.'],False,0.5)]
D=4.6
def tip(i,out):
    img,l1,l2,body,zin,pan=T[i]
    t1=text_layer(l1,128,WHITE); t2=grad_text(l2,150 if len(l2)<12 else 120)
    num=text_layer(f'0{i+1}',420,(255,255,255,40),'Anton-Regular.ttf')
    ds=[text_layer(l,50 if len(l)<40 else 44,(235,235,240),'BarlowCondensed-SemiBoldItalic.ttf') for l in body]
    src=text_layer('SOURCES : GUIDES METAFORGE · TALKESPORT · POWERPYX',28,(200,200,210,170),'BarlowCondensed-SemiBoldItalic.ttf')
    def gen(k):
        t=k/30; b=kenburns(img,t/D,zin,pan); bottom_fade(b,0.38,245); corner(b,f'{i+1} / 6')
        an=ease_out_cubic(prog(t,0.0,1.0)); a1=ease_out_cubic(prog(t,0.2,0.7)); a2=ease_out_back(prog(t,0.4,0.8)); a3=ease_out_cubic(prog(t,0.85,0.6))
        e=ease_in_cubic(prog(t,D-0.3,0.3))
        put(b,num,W/2+180-(1-an)*120,1000,alpha=an*(1-e))
        put(b,t1,W/2-(1-a1)*600-e*1200,1220,alpha=a1); put(b,t2,W/2+(1-clamp(a2))*700-e*1200,1360,alpha=clamp(a2))
        for j,dl in enumerate(ds): put(b,dl,W/2,1500+j*62+(1-a3)*25,alpha=a3*(1-e))
        put(b,src,W/2,1660,alpha=a3*(1-e))
        return b
    encode(f'a{i}',gen,int(D*30),out)
def a_intro(out):
    d=3.4
    def gen(k):
        t=k/30; b=kenburns('mount_kalaga_01',t/d,True,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(110,))); bottom_fade(b,0.35,240); corner(b,None)
        a1=ease_out_cubic(prog(t,0.1,0.7)); a2=ease_out_back(prog(t,0.35,0.8)); a3=ease_out_cubic(prog(t,0.9,0.6))
        put(b,text_layer('6 ASTUCES',170,WHITE),W/2-(1-a1)*700,1170,alpha=a1)
        put(b,grad_text('POUR BIEN DÉBUTER.',120),W/2+(1-clamp(a2))*800,1320,alpha=clamp(a2))
        put(b,text_layer('Ce que le jeu ne te dit pas',58,WHITE,'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1450,alpha=a3)
        return b
    encode('a_intro',gen,int(d*30),out)
def a_outro(out):
    d=3.6
    def gen(k):
        t=k/30; b=kenburns('leonida_keys_07',t/d,False,0.5); b.alpha_composite(Image.new('RGBA',(W,H),INK+(170,))); corner(b,None)
        a1=ease_out_cubic(prog(t,0.1,0.7)); a2=ease_out_back(prog(t,0.35,0.8)); a3=ease_out_cubic(prog(t,0.9,0.6))
        put(b,text_layer('LAQUELLE TU',150,WHITE),W/2-(1-a1)*700,840,alpha=a1)
        put(b,grad_text('CONNAISSAIS PAS ?',120),W/2+(1-clamp(a2))*800,990,alpha=clamp(a2))
        put(b,text_layer('Dis-le en commentaire  ·  Enregistre pour plus tard',52,WHITE,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1150,alpha=a3)
        put(b,text_layer('ABONNE-TOI @GTA6HUBFR_',54,YEL,'BarlowCondensed-ExtraBoldItalic.ttf'),W/2,1240,alpha=a3)
        return b
    encode('a_outro',gen,int(d*30),out)
if __name__=='__main__':
    out='/home/claude/rockstar/astuces'; os.makedirs(out,exist_ok=True)
    if sys.argv[1]=='test':
        import types
        for i in (0,5):
            img,l1,l2,body,zin,pan=T[i]; b=kenburns(img,0.6,zin,pan); bottom_fade(b,0.38,245); corner(b,f'{i+1} / 6')
            put(b,text_layer(f'0{i+1}',420,(255,255,255,40),'Anton-Regular.ttf'),W/2+180,1000)
            put(b,text_layer(l1,128,WHITE),W/2,1220); put(b,grad_text(l2,150 if len(l2)<12 else 120),W/2,1360)
            for j,l in enumerate(body): put(b,text_layer(l,50 if len(l)<40 else 44,(235,235,240),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1500+j*62)
            put(b,text_layer('SOURCES : GUIDES METAFORGE · TALKESPORT · POWERPYX',28,(200,200,210,170),'BarlowCondensed-SemiBoldItalic.ttf'),W/2,1660)
            b.convert('RGB').resize((540,960)).save(f'ast_test{i}.jpg')
    else:
        a_intro(out)
        for i in range(6): tip(i,out)
        a_outro(out)
        assemble(['a_intro']+[f'a{i}' for i in range(6)]+['a_outro'],out,'/home/claude/gta6hubfr_6_astuces.mp4')

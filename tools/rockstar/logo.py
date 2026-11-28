from PIL import Image, ImageDraw
def badge(size=96):
    im=Image.open('/home/claude/pdp/pdp_2.png').convert('RGBA').resize((size*4,size*4),Image.LANCZOS)
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse((0,0,im.width-1,im.height-1),fill=255); im.putalpha(m)
    return im.resize((size,size),Image.LANCZOS)

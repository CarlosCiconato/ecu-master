# zoom.py board out.png x0 y0 x1 y1 net1,net2,... : zoomed view, pads + tracks + straight lines for the given nets
import pcbnew,sys
from PIL import Image,ImageDraw,ImageFont
T=pcbnew.ToMM
b=pcbnew.LoadBoard(sys.argv[1]); out=sys.argv[2]; x0,y0,x1,y1=map(float,sys.argv[3:7]); nets=set(sys.argv[7].split(',')) if len(sys.argv)>7 else set()
S=12; im=Image.new('RGB',(int((x1-x0)*S),int((y1-y0)*S)),(15,40,28)); d=ImageDraw.Draw(im)
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
P=lambda x,y:((T(x)-x0)*S,(T(y)-y0)*S)
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA':
        q=P(t.GetPosition().x,t.GetPosition().y); r=T(t.GetWidth())*S/2; d.ellipse([q[0]-r,q[1]-r,q[0]+r,q[1]+r],fill=(200,200,200)); continue
    c={pcbnew.F_Cu:(200,70,50),pcbnew.B_Cu:(50,100,210)}.get(t.GetLayer(),(150,150,50))
    if t.GetNetname() in nets: c=(255,255,0)
    d.line([P(t.GetStart().x,t.GetStart().y),P(t.GetEnd().x,t.GetEnd().y)],fill=c,width=max(1,int(T(t.GetWidth())*S)))
ends={}
for f in b.GetFootprints():
    for p in f.Pads():
        bb=p.GetBoundingBox(); c=(255,255,0) if p.GetNetname() in nets else (160,160,160)
        d.rectangle([P(bb.GetX(),bb.GetY()),P(bb.GetRight(),bb.GetBottom())],outline=c)
        if p.GetNetname() in nets: ends.setdefault(p.GetNetname(),[]).append(P(p.GetPosition().x,p.GetPosition().y))
for n,ps in ends.items():
    for a in ps[1:]: d.line([ps[0],a],fill=(255,0,255),width=1)
    d.text(ps[0],n,fill=(255,255,255),font=fnt)
im.save(out); print('ok')

# render.py board.kicad_pcb out.png [title] : PIL drawing of the board (top view)
import pcbnew,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
T=pcbnew.ToMM
b=pcbnew.LoadBoard(sys.argv[1]); out=sys.argv[2]; title=sys.argv[3] if len(sys.argv)>3 else ''
S=6; W,H=200,130
im=Image.new('RGB',(W*S+20,H*S+60),(20,24,28)); d=ImageDraw.Draw(im)
try: fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13); big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
except: fnt=big=None
P=lambda x,y:(10+T(x)*S,50+T(y)*S)
d.rectangle([P(0,0),P(pcbnew.FromMM(W),pcbnew.FromMM(H))],fill=(18,60,40),outline=(230,230,120))
t=ET.parse('/tmp/claude-0/sch/net6.xml'); sp={c.get('ref'):c.find('sheetpath').get('names') for c in t.iter('comp')}
core={l.split('"')[1] for l in open('/home/claude/placa/core_refs.txt')} if False else set(open('/home/claude/placa/core_refs.txt').read().split())
pal=[(230,120,60),(90,170,250),(250,90,160),(140,230,110),(240,200,60),(180,120,250),(60,220,210),(250,150,150),(150,250,200),(250,250,250),(200,160,90),(120,140,250)]
cols={}
for tr in b.GetTracks():
    if tr.GetClass()=='PCB_VIA': continue
    c={pcbnew.F_Cu:(200,80,60),pcbnew.B_Cu:(60,110,200)}.get(tr.GetLayer(),(150,150,60))
    if not tr.IsLocked(): c=(255,230,0) if tr.GetLayer()==pcbnew.F_Cu else (0,220,255)
    d.line([P(tr.GetStart().x,tr.GetStart().y),P(tr.GetEnd().x,tr.GetEnd().y)],fill=c,width=max(1,int(T(tr.GetWidth())*S)))
for f in b.GetFootprints():
    r=f.GetReference()
    if r.startswith('SV'): continue
    bb=f.GetBoundingBox(False,False)
    if r in core or r in ('J101','J102','J103','J104'): fill=None; ol=(170,170,170)
    else:
        s=sp.get(r,'?'); cols.setdefault(s,pal[len(cols)%len(pal)]); ol=cols[s]; fill=None
    d.rectangle([P(bb.GetX(),bb.GetY()),P(bb.GetRight(),bb.GetBottom())],outline=ol,width=2 if r not in core else 1)
for r in ('J101','J102','J103','J104'):
    f=b.FindFootprintByReference(r); bb=f.GetBoundingBox(False,False)
    d.text(P(bb.GetX()+pcbnew.FromMM(2),bb.GetBottom()-pcbnew.FromMM(8)),r+' '+f.GetValue().split('·')[-1],fill=(255,255,255),font=fnt)
d.text((10,8),title,fill=(255,255,255),font=big)
y=30;x=10
for s,c in cols.items():
    d.rectangle([x,y,x+12,y+12],fill=c); d.text((x+16,y-1),s.strip('/'),fill=c,font=fnt); x+=16+int(d.textlength(s,font=fnt))+14 if fnt else 150
im.save(out); print('ok',out)

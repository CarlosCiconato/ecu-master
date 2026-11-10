# pcb_update.py net.xml : sync footprints + pad nets from netlist; new footprints placed at a target box
import pcbnew,sys,re,xml.etree.ElementTree as ET
P='/home/claude/placa/'; mm=pcbnew.FromMM; V=pcbnew.VECTOR2I; T=pcbnew.ToMM
t=ET.parse(sys.argv[1])
b=pcbnew.LoadBoard(P+'nossa-ecu.kicad_pcb')
pinnet={}
for n in t.iter('net'):
    for nd in n.iter('node'): pinnet[(nd.get('ref'),nd.get('pin'))]=n.get('name')
def net(name):
    ni=b.FindNet(name)
    if ni is None: ni=pcbnew.NETINFO_ITEM(b,name); b.Add(ni)
    return ni
have={f.GetReference():f for f in b.GetFootprints()}
new=[]; changed=set()
for c in t.iter('comp'):
    r=c.get('ref'); f=have.get(r)
    if f is None:
        lib,name=c.findtext('footprint').split(':',1)
        f=pcbnew.FootprintLoad(f'/usr/share/kicad/footprints/{lib}.pretty',name)
        f.SetReference(r); f.SetValue(c.findtext('value') or ''); b.Add(f); new.append(f)
    for pad in f.Pads():
        nm=pinnet.get((r,pad.GetNumber()),'')
        if pad.GetNetname()!=nm:
            changed.add(pad.GetNetname()); pad.SetNet(net(nm) if nm else b.FindNet(''))
            if not nm: pad.SetNetCode(0)
print('new',[f.GetReference() for f in new],'nets changed',changed)
# drop non-Proteus tracks on changed nets (re-route later)
p=pcbnew.LoadBoard(P+'proteus.kicad_pcb')
a=p.FindFootprintByReference('U1').GetPosition(); c=b.FindFootprintByReference('U1').GetPosition(); dx,dy=c.x-a.x,c.y-a.y
orig={(x.GetStart().x+dx,x.GetStart().y+dy,x.GetEnd().x+dx,x.GetEnd().y+dy) for x in p.GetTracks()}
rm=[x for x in b.GetTracks() if x.GetNetname() in changed-{'GND'} and (x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y) not in orig]
for x in rm: b.Delete(x)
print('removed tracks',len(rm))
# place new parts: simple row packing in box
x0,y0,x1,y1=map(float,sys.argv[2:6]); x,y,rowh=x0,y0,0
for f in sorted(new,key=lambda f:-f.GetBoundingBox(False,False).GetArea()):
    bb=f.GetBoundingBox(False,False); w=T(bb.GetWidth())+0.6; h=T(bb.GetHeight())+0.6
    if x+w>x1: x=x0; y+=rowh; rowh=0
    f.Move(V(mm(x)-bb.GetX(),mm(y)-bb.GetY())); x+=w; rowh=max(rowh,h)
print('placed to y',round(y+rowh,1),'(limit',y1,')')
b.Save(P+'nossa-ecu.kicad_pcb')

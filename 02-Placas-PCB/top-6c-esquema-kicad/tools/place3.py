# place3.py: re-place board (etapa 2). Connectors housings overhang the bottom edge (footprint marks "PCB EDGE"),
# core shifted down DY, new blocks put next to the connectors / circuits they serve.
import pcbnew,collections,xml.etree.ElementTree as ET
P='/home/claude/placa/'; mm=pcbnew.FromMM; T=pcbnew.ToMM; V=pcbnew.VECTOR2I
W,H,DY=200.0,130.0,8.0
b=pcbnew.LoadBoard(P+'nossa-ecu.kicad_pcb')
t=ET.parse('/tmp/claude-0/sch/net6.xml'); sp={c.get('ref'):c.find('sheetpath').get('names') for c in t.iter('comp')}
core=set(open(P+'core_refs.txt').read().split())
for z in list(b.Zones()): b.Delete(z)
for d in [d for d in b.GetDrawings() if d.GetLayer()==pcbnew.Edge_Cuts]: b.Delete(d)
# 1) core down
for f in b.GetFootprints():
    r=f.GetReference()
    if r in core or r.startswith('SV'): f.Move(V(0,mm(DY)))
for tr in b.GetTracks(): tr.Move(V(0,mm(DY)))
for d in b.GetDrawings(): d.Move(V(0,mm(DY)))
# 2) outline
pts=[(0,0),(W,0),(W,H),(0,H)]
for i in range(4):
    s=pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1))
    a,c=pts[i],pts[(i+1)%4]; s.SetStart(V(mm(a[0]),mm(a[1]))); s.SetEnd(V(mm(c[0]),mm(c[1]))); b.Add(s)
# 3) connectors: orientation 0, "PCB EDGE" line (User.Comments) on the board edge, same x span as before
for r in ('J101','J102','J103','J104'):
    f=b.FindFootprintByReference(r); cx=f.GetBoundingBox(False,False).GetCenter().x
    f.SetOrientationDegrees(0)
    e=[g for g in f.GraphicalItems() if g.GetLayer()==pcbnew.Cmts_User and g.GetClass()!='PCB_TEXT']
    ey=sum(g.GetBoundingBox().GetCenter().y for g in e)//len(e)
    f.Move(V(cx-f.GetBoundingBox(False,False).GetCenter().x, mm(H)-ey))
    ys=[T(p.GetPosition().y) for p in f.Pads() if p.GetNumber()]
    print(r,'pins y',round(min(ys),1),round(max(ys),1))
# 4) new blocks -> target top-left corner (mm), optional rotation
tgt={'/Sonda larga 2/':(169.5,1.0),'/Sonda larga 1/':(169.5,32.5),
     '/botoes2/':(169.5,64.5),'/lowside_quad5 (nitro/arrancada)/':(185.0,64.5),'/botoes1/':(169.5,83.0),
     '/pullup_hall1/':(96,1.5),'/pullup_hall2/':(106,1.5),'/pullup_hall3/':(116,1.5),'/led_status/':(128,1.0),
     '/analog5/':(20,82),'/vr3/':(151,96.5)}
rot={'/vr3/':90}
g=collections.defaultdict(list)
for f in b.GetFootprints():
    r=f.GetReference()
    if r in core or r.startswith('SV') or r in ('J101','J102','J103','J104'): continue
    g[sp.get(r,'?')].append(f)
for s,fs in g.items():
    if s not in tgt: print('NO TARGET',s,[f.GetReference() for f in fs]); continue
    bb=pcbnew.BOX2I(); [bb.Merge(f.GetBoundingBox(False,False)) for f in fs]
    if s in rot:
        c=bb.GetCenter()
        for f in fs: f.Rotate(c,pcbnew.EDA_ANGLE(rot[s],pcbnew.DEGREES_T))
        bb=pcbnew.BOX2I(); [bb.Merge(f.GetBoundingBox(False,False)) for f in fs]
    x,y=tgt[s]
    for f in fs: f.Move(V(mm(x)-bb.GetX(),mm(y)-bb.GetY()))
    bb=pcbnew.BOX2I(); [bb.Merge(f.GetBoundingBox(False,False)) for f in fs]
    print(f'{s:36s} {T(bb.GetX()):.1f},{T(bb.GetY()):.1f}-{T(bb.GetRight()):.1f},{T(bb.GetBottom()):.1f}')
# 5) GND planes inner + bottom
gnd=b.FindNet('GND')
for lay in (pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu):
    z=pcbnew.ZONE(b); z.SetLayer(lay); z.SetNet(gnd); o=z.Outline(); o.NewOutline()
    for x,y in ((0.5,0.5),(W-0.5,0.5),(W-0.5,H-0.5),(0.5,H-0.5)): o.Append(mm(x),mm(y))
    z.SetLocalClearance(mm(0.3)); z.SetMinThickness(mm(0.25)); z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); b.Add(z)
b.Save(P+'nossa-ecu.kicad_pcb'); print('saved')

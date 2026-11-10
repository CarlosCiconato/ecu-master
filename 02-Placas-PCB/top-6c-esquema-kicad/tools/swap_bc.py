# swap_bc.py: J103 (26p) to slot 2, J102 (34p) to slot 3 so sensors sit under the core's analog inputs.
# Deletes non-Proteus tracks of nets touching J102/J103 or analog5; moves analog5 into the channel above J102.
import pcbnew,xml.etree.ElementTree as ET
P='/home/claude/placa/'; mm=pcbnew.FromMM; T=pcbnew.ToMM; V=pcbnew.VECTOR2I
b=pcbnew.LoadBoard(P+'nossa-ecu.kicad_pcb'); p=pcbnew.LoadBoard(P+'proteus.kicad_pcb')
a=p.FindFootprintByReference('U1').GetPosition(); c=b.FindFootprintByReference('U1').GetPosition(); dx,dy=c.x-a.x,c.y-a.y
orig={(t.GetStart().x+dx,t.GetStart().y+dy,t.GetEnd().x+dx,t.GetEnd().y+dy) for t in p.GetTracks()}
t=ET.parse('/tmp/claude-0/sch/net6.xml'); sp={x.get('ref'):x.find('sheetpath').get('names') for x in t.iter('comp')}
an=[f for f in b.GetFootprints() if sp.get(f.GetReference())=='/analog5/']
nets=set()
for r in ('J102','J103'):
    for pd in b.FindFootprintByReference(r).Pads(): nets.add(pd.GetNetname())
for f in an:
    for pd in f.Pads(): nets.add(pd.GetNetname())
nets-= {'GND',''}
rm=[x for x in b.GetTracks() if x.GetNetname() in nets and (x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y) not in orig]
for x in rm: b.Delete(x)
print('removed new tracks',len(rm))
for r,x0 in (('J103',56.5),('J102',103.6)):
    f=b.FindFootprintByReference(r); bb=f.GetBoundingBox(False,False); f.Move(V(mm(x0)-bb.GetX(),0))
    bb=f.GetBoundingBox(False,False); print(r,round(T(bb.GetX()),1),round(T(bb.GetRight()),1))
bb=pcbnew.BOX2I(); [bb.Merge(f.GetBoundingBox(False,False)) for f in an]
cen=bb.GetCenter()
for f in an: f.Rotate(cen,pcbnew.EDA_ANGLE(90,pcbnew.DEGREES_T))
bb=pcbnew.BOX2I(); [bb.Merge(f.GetBoundingBox(False,False)) for f in an]
for f in an: f.Move(V(mm(120)-bb.GetX(),mm(97)-bb.GetY()))
bb=pcbnew.BOX2I(); [bb.Merge(f.GetBoundingBox(False,False)) for f in an]
print('analog5',[round(T(v),1) for v in (bb.GetX(),bb.GetY(),bb.GetRight(),bb.GetBottom())])
g=b.FindNet('GND')
for f in b.GetFootprints():
    if f.GetReference().startswith('SV'):
        for pd in f.Pads(): pd.SetNet(g)
vs=[]
for x in list(b.GetTracks()):
    x.SetLocked(True)
    if x.GetClass()=='PCB_VIA':
        q=x.GetPosition()
        if any(abs(q.x-o.x)<20000 and abs(q.y-o.y)<20000 for o in vs): b.Delete(x)
        else: vs.append(q)
b.Save(P+'nossa-ecu.kicad_pcb'); print('saved')

# zones.py: copy Proteus internal planes (In1 GND, In2 +5V/+3V3) + small 12V_MR pours into nossa-ecu with the core offset.
# mode 'route' = only inner planes (for DSN); 'final' = also F/B GND pours over whole board
import pcbnew,sys
mm=pcbnew.FromMM; V=pcbnew.VECTOR2I
mode=sys.argv[1]; fn=sys.argv[2] if len(sys.argv)>2 else '/home/claude/placa/nossa-ecu.kicad_pcb'
b=pcbnew.LoadBoard(fn); p=pcbnew.LoadBoard('/home/claude/placa/proteus.kicad_pcb')
ref='U1' if b.FindFootprintByReference('U1') else None
a=p.FindFootprintByReference('U1').GetPosition(); c=b.FindFootprintByReference('U1').GetPosition()
d=V(c.x-a.x,c.y-a.y)
for z in list(b.Zones()): b.Delete(z)
W,H=200,130
for z in p.Zones():
    ln=p.GetLayerName(z.GetLayer()); nn=z.GetNetname()
    if ln=='In1.Cu' and nn=='GND': continue   # replaced by full-board plane
    if ln in ('F.Cu','B.Cu') and nn=='GND': continue
    nz=z.Duplicate(); nz.SetParent(b); nz.Move(d); nz.SetNet(b.FindNet(nn)); nz.UnFill() if hasattr(nz,'UnFill') else None; b.Add(nz)
layers=[pcbnew.In1_Cu]+([pcbnew.F_Cu,pcbnew.B_Cu] if mode=='final' else [])
for lay in layers:
    z=pcbnew.ZONE(b); z.SetLayer(lay); z.SetNet(b.FindNet('GND')); o=z.Outline(); o.NewOutline()
    for x,y in ((0.5,0.5),(W-0.5,0.5),(W-0.5,H-0.5),(0.5,H-0.5)): o.Append(mm(x),mm(y))
    z.SetLocalClearance(mm(0.3)); z.SetMinThickness(mm(0.25)); z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    if lay!=pcbnew.In1_Cu: z.SetAssignedPriority(0)
    b.Add(z)
b.Save(fn); print('zones',[(b.GetLayerName(z.GetLayer()),z.GetNetname()) for z in b.Zones()])

import pcbnew
T=pcbnew.ToMM
b=pcbnew.LoadBoard('/home/claude/placa/nossa-ecu.kicad_pcb')
core=set(open('/home/claude/placa/core_refs.txt').read().split())
fps=[f for f in b.GetFootprints() if not f.GetReference().startswith('SV')]
new=[f for f in fps if f.GetReference() not in core]
bad=0
tr=[t for t in b.GetTracks()]
for f in new:
    cb=f.GetBoundingBox(False,False)
    for o in fps:
        if o is not f and o.GetReference() in core and cb.Intersects(o.GetBoundingBox(False,False)): bad+=1; print('overlap',f.GetReference(),o.GetReference())
    for p in f.Pads():
        pb=p.GetBoundingBox()
        for t in tr:
            if t.GetNetCode()!=p.GetNetCode() and pb.Intersects(t.GetBoundingBox()): bad+=1; print('pad over track',f.GetReference(),p.GetNumber())
print('problems',bad)

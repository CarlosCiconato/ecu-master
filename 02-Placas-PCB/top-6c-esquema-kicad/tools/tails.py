# tails.py board : trim dead-end tails (segment end touching nothing of its net), iteratively; non-plane nets
import pcbnew,sys,collections
b=pcbnew.LoadBoard(sys.argv[1]); PL={'GND','+5V','+3V3','','/12V_MR','/12V_PROT','/12V_RAW'}
pads=collections.defaultdict(list)
for f in b.GetFootprints():
    for p in f.Pads(): pads[p.GetNetname()].append(p)
by=collections.defaultdict(list)
for t in b.GetTracks(): by[t.GetNetname()].append(t)
tot=0
for n,ts in by.items():
    if n in PL: continue
    ts=list(ts)
    while True:
        def touched(pt,lay,me):
            for p in pads[n]:
                if (lay is None or p.IsOnLayer(lay)) and p.HitTest(pt): return True
            for o in ts:
                if o is me: continue
                if o.GetClass()=='PCB_VIA':
                    if (o.GetPosition()-pt).EuclideanNorm()<=o.GetWidth()//2+2000: return True
                elif (lay is None or o.GetLayer()==lay) and o.HitTest(pt,2000): return True
            return False
        rm=[]
        for t in ts:
            if t.GetClass()=='PCB_VIA':
                if not touched(t.GetPosition(),None,t): rm.append(t)
            elif not touched(t.GetStart(),t.GetLayer(),t) or not touched(t.GetEnd(),t.GetLayer(),t): rm.append(t)
        if not rm: break
        for t in rm: ts.remove(t); b.Delete(t)
        tot+=len(rm)
b.Save(sys.argv[1]); print('tail items removed',tot)

# orphans.py board : delete track/via groups that touch no pad (leftovers), non-plane nets
import pcbnew,sys,collections
b=pcbnew.LoadBoard(sys.argv[1]); PL={'GND','+5V','+3V3','','/12V_MR'}
pads=collections.defaultdict(list)
for f in b.GetFootprints():
    for p in f.Pads(): pads[p.GetNetname()].append(p)
by=collections.defaultdict(list)
for t in b.GetTracks(): by[t.GetNetname()].append(t)
rm=[]
for n,ts in by.items():
    if n in PL: continue
    par=list(range(len(ts)))
    def fd(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    pts=[]
    for i,t in enumerate(ts):
        if t.GetClass()=='PCB_VIA': pts.append((i,t.GetPosition(),None))
        else: pts+=[(i,t.GetStart(),t.GetLayer()),(i,t.GetEnd(),t.GetLayer())]
    for i,pt,l in pts:
        for j,o in enumerate(ts):
            if j==i: continue
            if o.GetClass()=='PCB_VIA':
                if (o.GetPosition()-pt).EuclideanNorm()<=o.GetWidth()//2+2000: par[fd(i)]=fd(j)
            elif (l is None or l==o.GetLayer()) and o.HitTest(pt,2000): par[fd(i)]=fd(j)
    haspad=set()
    for i,pt,l in pts:
        if any((l is None or p.IsOnLayer(l)) and p.HitTest(pt) for p in pads[n]): haspad.add(fd(i))
    for i,t in enumerate(ts):
        if fd(i) not in haspad: rm.append(t)
for t in rm: b.Delete(t)
b.Save(sys.argv[1]); print('orphan items removed',len(rm))

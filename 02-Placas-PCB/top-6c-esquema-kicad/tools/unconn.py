# unconn.py board [nets.txt] : geometric union-find per net (pads, tracks, vias; zones ignored except GND which is skipped)
import pcbnew,sys,collections
b=pcbnew.LoadBoard(sys.argv[1])
part=set(l.strip() for l in open(sys.argv[2])) if len(sys.argv)>2 else None
SKIP={'GND','+5V','+3V3'}   # plane nets
items=collections.defaultdict(list)
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetCode()>0: items[p.GetNetname()].append(('pad',p))
for t in b.GetTracks():
    items[t.GetNetname()].append(('via' if t.GetClass()=='PCB_VIA' else 'trk',t))
bad={}
for n,its in items.items():
    if n in SKIP or (part is not None and n not in part): continue
    pads=[i for i in its if i[0]=='pad']
    if len(pads)<2: continue
    par=list(range(len(its)))
    def fd(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    def un(a,c): par[fd(a)]=fd(c)
    pts=[]   # (index, point, layerset)
    for i,(k,o) in enumerate(its):
        if k=='trk': pts+= [(i,o.GetStart(),o.GetLayer()),(i,o.GetEnd(),o.GetLayer())]
        elif k=='via': pts.append((i,o.GetPosition(),None))
    for i,(k,o) in enumerate(its):
        if k=='pad':
            for j,pt,l in pts:
                if (l is None or o.IsOnLayer(l)) and o.HitTest(pt): un(i,j)
    for a in range(len(pts)):
        ia,pa,la=pts[a]
        for c in range(a+1,len(pts)):
            ic,pc,lc=pts[c]
            if ia==ic: continue
            if (la is None or lc is None or la==lc) and abs(pa.x-pc.x)<2000 and abs(pa.y-pc.y)<2000: un(ia,ic)
            # T-junction: point on a track
    for j,pt,l in pts:
        for i,(k,o) in enumerate(its):
            if k=='trk' and i!=j and (l is None or l==o.GetLayer()) and o.HitTest(pt,1000): un(i,j)
    roots={fd(its.index(p)) for p in pads}
    if len(roots)>1: bad[n]=len(roots)-1
print('nets incomplete',len(bad),'missing links',sum(bad.values()))
print(sorted(bad.items(),key=lambda kv:-kv[1]))

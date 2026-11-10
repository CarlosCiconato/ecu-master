# fix_clear.py board drc.txt : delete unlocked tracks/vias named in clearance/short violations
import pcbnew,sys,re
b=pcbnew.LoadBoard(sys.argv[1]); t=open(sys.argv[2]).read()
pts=[]
for bl in re.split(r'\n\[',t):
    if not (bl.startswith('clearance]') or bl.startswith('shorting_items]') or bl.startswith('tracks_crossing]')): continue
    for m in re.finditer(r'@\(([\d.-]+) mm, ([\d.-]+) mm\): (Track|Via) \[([^\]]*)\]',bl): pts.append((float(m.group(1)),float(m.group(2)),m.group(4)))
rm=set()
for tr in b.GetTracks():
    if tr.IsLocked(): continue
    for x,y,n in pts:
        if tr.GetNetname()==n and tr.HitTest(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)),pcbnew.FromMM(0.05)): rm.add(tr)
for tr in rm: b.Delete(tr)
b.Save(sys.argv[1]); print('removed',len(rm))

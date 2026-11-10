# undangle.py board : repeatedly delete tracks/vias that KiCad DRC flags as dangling (non-plane nets)
import pcbnew,sys,re
fn=sys.argv[1]; tot=0
for it in range(30):
    b=pcbnew.LoadBoard(fn)
    pcbnew.WriteDRCReport(b,'/tmp/claude-0/sch/ud.txt',pcbnew.EDA_UNITS_MILLIMETRES,True)
    t=open('/tmp/claude-0/sch/ud.txt').read(); pts=[]
    for bl in re.split(r'\n\[',t):
        if bl.startswith('track_dangling]') or bl.startswith('via_dangling]'):
            m=re.search(r'@\(([\d.-]+) mm, ([\d.-]+) mm\): (Track|Via) \[([^\]]*)\]',bl)
            if m and m.group(4) not in ('GND','+5V','+3V3'): pts.append((pcbnew.FromMM(float(m.group(1))),pcbnew.FromMM(float(m.group(2))),m.group(4),m.group(3)))
    rm=set()
    for tr in b.GetTracks():
        for x,y,n,k in pts:
            if tr.GetNetname()==n and ((k=='Via')==(tr.GetClass()=='PCB_VIA')) and tr.HitTest(pcbnew.VECTOR2I(x,y),2000): rm.add(tr)
    if not rm: break
    for tr in rm: b.Delete(tr)
    tot+=len(rm); b.Save(fn)
print('removed',tot,'iterations',it)

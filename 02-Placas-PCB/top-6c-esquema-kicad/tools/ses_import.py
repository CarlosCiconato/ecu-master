# ses_import.py board.kicad_pcb in.ses nets.txt [out.kicad_pcb]: add freerouting wires/vias of listed nets to the board
import pcbnew,sys,re
fn,ses,lst=sys.argv[1:4]; out=sys.argv[4] if len(sys.argv)>4 else fn
part=set(l.strip() for l in open(lst) if l.strip())
b=pcbnew.LoadBoard(fn)
s=open(ses).read()
res=re.search(r'\(resolution\s+(\w+)\s+([\d.]+)\)',s); unit,div=res.group(1),float(res.group(2))
k={'um':1e3,'mm':1e6,'mil':25400}[unit]/div          # -> nm
def toks(t):
    for m in re.finditer(r'"[^"]*"|[()]|[^\s()]+',t): yield m.group(0)
def parse(it):
    l=[]
    for x in it:
        if x=='(': l.append(parse(it))
        elif x==')': return l
        else: l.append(x.strip('"') if x.startswith('"') else x)
    return l
tree=parse(toks(s))[0]
def find(n,name):
    return [c for c in n if isinstance(c,list) and c and c[0]==name]
routes=find(tree,'routes')[0]; netout=find(routes,'network_out')[0]
vdef={}
for ps in find(find(routes,'library_out')[0],'padstack'):
    sh=find(ps,'shape')[0][1]; vdef[ps[1]]=float(sh[2])*k
L={b.GetLayerName(l):l for l in (pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu)}
have=set()
for t in b.GetTracks():
    have.add((t.GetNetname(),t.GetStart().x//1000,t.GetStart().y//1000,t.GetEnd().x//1000,t.GetEnd().y//1000))
nt=nv=0
vpos=[t.GetPosition() for t in b.GetTracks() if t.GetClass()=='PCB_VIA']
for net in find(netout,'net'):
    name=net[1]
    if name not in part: continue
    ni=b.FindNet(name)
    for w in find(net,'wire'):
        p=find(w,'path')[0]; lay=L[p[1]]; wd=int(float(p[2])*k); c=[float(v)*k for v in p[3:]]
        pts=[(int(c[i]),int(-c[i+1])) for i in range(0,len(c),2)]
        for a,e in zip(pts,pts[1:]):
            key=(name,a[0]//1000,a[1]//1000,e[0]//1000,e[1]//1000)
            if key in have or (name,e[0]//1000,e[1]//1000,a[0]//1000,a[1]//1000) in have: continue
            t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(*a)); t.SetEnd(pcbnew.VECTOR2I(*e)); t.SetWidth(wd); t.SetLayer(lay); t.SetNet(ni); b.Add(t); nt+=1
    for v in find(net,'via'):
        x,y=int(float(v[2])*k),int(-float(v[3])*k)
        if any(abs(x-q.x)<20000 and abs(y-q.y)<20000 for q in vpos): continue
        vpos.append(pcbnew.VECTOR2I(x,y))
        vi=pcbnew.PCB_VIA(b); vi.SetPosition(pcbnew.VECTOR2I(x,y)); vi.SetWidth(int(vdef.get(v[1],600e3*1))); vi.SetDrill(pcbnew.FromMM(0.3)); vi.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); vi.SetNet(ni); b.Add(vi); nv+=1
for t in b.GetTracks(): t.SetLocked(True)
b.Save(out); print('added tracks',nt,'vias',nv)

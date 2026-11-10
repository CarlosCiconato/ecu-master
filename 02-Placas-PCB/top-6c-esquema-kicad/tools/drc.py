# drc.py board.kicad_pcb report.txt [nets.txt]: KiCad DRC; summary of violations + unconnected (optionally only part nets)
import pcbnew,sys,re,collections
b=pcbnew.LoadBoard(sys.argv[1]); rep=sys.argv[2]
part=set(l.strip() for l in open(sys.argv[3])) if len(sys.argv)>3 else None
pcbnew.WriteDRCReport(b,rep,pcbnew.EDA_UNITS_MILLIMETRES,True)
t=open(rep).read()
sec=re.split(r'\n\*\* ',t)
for s in sec:
    head=s.split('\n')[0]
    items=re.findall(r'\n\[(\w+)\]',s)
    print(head[:60], collections.Counter(items).most_common(8))
if part:
    un=re.split(r'\[unconnected_items\]',t)[1:]
    n=sum(1 for u in un if any(('['+p+']') in u.split('\n[')[0] or (' '+p+' ') in u for p in part))
    print('unconnected touching part nets ~',n)

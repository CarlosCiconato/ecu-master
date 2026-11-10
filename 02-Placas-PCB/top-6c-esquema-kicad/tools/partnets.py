# partnets.py board refs... > nets.txt  (refs may be sheet prefixes like sheet:/Sonda larga 1/)
import pcbnew,sys,xml.etree.ElementTree as ET
b=pcbnew.LoadBoard(sys.argv[1])
t=ET.parse('/tmp/claude-0/sch/net6.xml'); sp={c.get('ref'):c.find('sheetpath').get('names') for c in t.iter('comp')}
EX={'GND','+5V','+3V3','/12V_MR','/12V_RAW','/12V_PROT',''}
want=sys.argv[2:]; nets=set()
for f in b.GetFootprints():
    r=f.GetReference()
    if r in want or ('sheet:'+sp.get(r,'')) in want:
        for p in f.Pads():
            n=p.GetNetname()
            if n not in EX and not n.startswith('unconnected'): nets.add(n)
print('\n'.join(sorted(nets)))

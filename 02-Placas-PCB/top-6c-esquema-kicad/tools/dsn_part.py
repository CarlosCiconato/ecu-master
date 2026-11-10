# dsn_part.py full.dsn out.dsn nets.txt : keep only listed nets in the DSN network (other pads/wires become
# no-net obstacles), and set widths per class.
import sys,re
src,dst,lst=sys.argv[1:4]
part=set(l.strip() for l in open(lst) if l.strip())
s=open(src).read()
def q(n): return '"'+n+'"' if re.search(r'[\s()"\-]',n) or n=='' else n
def block_end(s,i):
    dep=0;k=i
    while True:
        c=s[k]
        if c=='(': dep+=1
        elif c==')':
            dep-=1
            if dep==0: return k+1
        elif c=='"': k=s.index('"',k+1)
        k+=1
i=s.index('(network'); e=block_end(s,i)
net=s[i:e]; out=[]; pos=0; kept=[]
for m in re.finditer(r'\(net ("[^"]*"|[^\s()]+)',net):
    a=m.start(); 
    if a<pos: continue
    b2=block_end(net,a); name=m.group(1).strip('"')
    out.append(net[pos:a])
    if name in part: out.append(net[a:b2]); kept.append(name)
    pos=b2
rest=net[pos:]
rest=rest[:rest.index('(class')]
POWER=re.compile(r'^/(12V_(MR|RAW|PROT)|LS\d+|HS\d+|ETB\d[+-]|.*HEATER.*)$')
MED=re.compile(r'^(\+5V|\+3V3|/5V_SENSOR_\d|/12V_SENS_\d|/IGN\d+|/VR\d[+-])$')
cls={'Power':[],'Medium':[],'Default':[]}
for n in kept: cls['Power' if POWER.match(n) else 'Medium' if MED.match(n) else 'Default'].append(n)
W={'Power':(800,250),'Medium':(400,200),'Default':(254,152.5)}
via='Via[0-3]_599.44:299.72_um'
cl=''.join(f'    (class {c} '+' '.join(q(n) for n in ns)+f'\n      (circuit (use_via {via}))\n      (rule (width {W[c][0]}) (clearance {W[c][1]}))\n    )\n' for c,ns in cls.items() if ns)
s=s[:i]+''.join(out)+rest+cl+'  )\n'+s[e:]
# wires of other nets -> no net
def fixw(m):
    n=m.group(1).strip('"')
    return m.group(0) if n in part else ''
s=re.sub(r'\(net ("[^"]*"|[^\s()]+)\)',fixw,s)
s=s.replace('(layer In2.Cu\n      (type power)','(layer In2.Cu\n      (type signal)')
open(dst,'w').write(s)
print({c:len(v) for c,v in cls.items()}, 'missing',[n for n in part if n not in kept][:5])

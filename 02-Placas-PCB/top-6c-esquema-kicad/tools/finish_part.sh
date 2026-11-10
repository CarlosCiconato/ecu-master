#!/bin/bash
# finish_part.sh X : import partX.ses into master, remove clearance offenders, report part unconnected, save master
S=/tmp/claude-0/sch; cd /home/claude/placa
python3 tools/ses_import.py nossa-ecu.kicad_pcb $S/part$1.ses $S/part$1.txt $S/$1.kicad_pcb 2>&1 | grep added
python3 tools/drc.py $S/$1.kicad_pcb $S/$1_drc.txt >/dev/null 2>&1
for i in 1 2; do python3 tools/fix_clear.py $S/$1.kicad_pcb $S/$1_drc.txt 2>&1 | grep removed; python3 tools/drc.py $S/$1.kicad_pcb $S/$1_drc.txt >/dev/null 2>&1; done
python3 tools/drc.py $S/$1.kicad_pcb $S/$1_drc.txt 2>&1 | grep Found
python3 - $1 <<'PY' 2>/dev/null
import re,collections,sys
X=sys.argv[1]; part=set(l.strip() for l in open(f'/tmp/claude-0/sch/part{X}.txt'))
t=open(f'/tmp/claude-0/sch/{X}_drc.txt').read(); c=collections.Counter()
for bl in t.split('[unconnected_items]')[1:]:
    m=re.search(r'\[([^\]]+)\]',bl)
    if m and m.group(1) in part: c[m.group(1)]+=1
print('part unconnected',sum(c.values()),dict(c))
PY
cp $S/$1.kicad_pcb nossa-ecu.kicad_pcb

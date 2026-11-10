#!/bin/bash
# chunks.sh X N passes timeout : route partX.txt in chunks of N nets (only incomplete nets)
S=/tmp/claude-0/sch; cd /home/claude/placa
python3 tools/unconn.py nossa-ecu.kicad_pcb $S/part$1.txt 2>/dev/null | sed -n 2p | python3 -c "import sys,ast;[print(n) for n,_ in ast.literal_eval(sys.stdin.read())]" > $S/todo$1.txt
split -l $2 -d $S/todo$1.txt $S/chunk$1_
for f in $S/chunk$1_*; do
  k=$(basename $f); cp $f $S/part$k.txt
  tools/run_part.sh $k $3 $4 >/dev/null 2>&1
  echo "== $k $(tr '\n' ' ' < $f)"; grep -E "Auto-routing was|^exit" $S/part$k.log | cut -c50-110
  [ -f $S/part$k.ses ] && tools/finish_part.sh $k | grep -E "added"
  rm -f $S/part$k.ses
done
python3 tools/unconn.py nossa-ecu.kicad_pcb $S/part$1.txt 2>/dev/null

#!/bin/bash
# run_part.sh X : export DSN of master, keep nets of partX.txt, start freerouting (background caller)
set -e
S=/tmp/claude-0/sch; cd /home/claude/placa
python3 -c "
import pcbnew
b=pcbnew.LoadBoard('nossa-ecu.kicad_pcb'); print(pcbnew.ExportSpecctraDSN(b,'$S/full.dsn'))" 2>/dev/null
python3 tools/dsn_part.py $S/full.dsn $S/part$1.dsn $S/part$1.txt
/home/claude/tools/fr.sh part$1.dsn part$1.ses ${2:-6} ${3:-2400}

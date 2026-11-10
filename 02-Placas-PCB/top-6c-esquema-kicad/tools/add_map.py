# add_map.py: (1) sensor GND only B26/B27, power GND C3/C4 (frees B28-B34, C5, C6)
# (2) internal MAP sensor (MPXH6400A, 4 bar abs) on AIN14 via 3-pad solder jumper (default internal; bridge 2-3 for connector pin B6)
import sys, uuid
sys.path.insert(0,'/home/claude/tools')
from gensheet import build, U, eff
from kiutils.schematic import Schematic
from kiutils.items.schitems import (HierarchicalSheet, HierarchicalPin, LocalLabel, NoConnect,
    HierarchicalSheetProjectInstance, HierarchicalSheetProjectPath)
from kiutils.items.common import Position, Property, Stroke, ColorRGBA
R='/home/claude/placa/'
r=Schematic.from_file(R+'proteus.kicad_sch'); RU=r.uuid
def near(a,b,x,y): return abs(a-x)<0.01 and abs(b-y)<0.01
free=[(477.38,479.92,y) for y in (101.12,103.66,106.2,108.74,111.28,113.82,116.36)]+[(522.38,524.92,y) for y in (42.7,45.24)]
n=0
for px,pinx,y in free:
    s=[s for s in r.schematicSymbols if s.libraryNickname=='power' and near(s.position.X,s.position.Y,px,y)]
    for x in s: r.schematicSymbols.remove(x); n+=1
    for w in [w for w in r.graphicalItems if hasattr(w,'points') and any(near(p.X,p.Y,px,y) for p in w.points)]: r.graphicalItems.remove(w)
    r.noConnects.append(NoConnect(position=Position(pinx,y),uuid=U()))
print('GND symbols removed',n)
# J102 AIN14 pin label -> AIN14_EXT
l=[l for l in r.labels if l.text=='AIN14_PIN' and near(l.position.X,l.position.Y,479.92,73.18)]
assert len(l)==1; l[0].text='AIN14_EXT'
# new sheet
X,Y,W,H=320,215,20.32,10.16; su=U()
sh=HierarchicalSheet(position=Position(X,Y),width=W,height=H,stroke=Stroke(width=0.1524),fill=ColorRGBA(),uuid=su)
sh.sheetName=Property(key='Sheetname',value='map_interno',position=Position(X,Y-0.7,0),effects=eff())
sh.fileName=Property(key='Sheetfile',value='map_interno.kicad_sch',position=Position(X,Y+H+0.6,0),effects=eff()); sh.fileName.id=1
for k,(pn,net) in enumerate((('VS','5V_SENSOR_2'),('EXT','AIN14_EXT'),('OUT','AIN14_PIN'))):
    y=Y+2.54+k*2.54
    sh.pins.append(HierarchicalPin(name=pn,connectionType='bidirectional',position=Position(X,y,180),effects=eff('left'),uuid=U()))
    r.labels.append(LocalLabel(text=net,position=Position(X,y,180),effects=eff('right'),uuid=U()))
sh.instances=[HierarchicalSheetProjectInstance(name='proteus',paths=[HierarchicalSheetProjectPath(sheetInstancePath='/'+RU,page='40')])]
r.sheets.append(sh); r.to_file(R+'proteus.kicad_sch')
R08='Resistor_SMD:R_0805_2012Metric'; C06='Capacitor_SMD:C_0603_1608Metric'
build(R+'map_interno.kicad_sch',[
 dict(ref='U1',lib='Sensor_Pressure:MPXH6115A',value='MPXH6400A (4 bar abs)',fp='Sensor_Pressure:Freescale_98ARH99066A',
      pins={'1':None,'2':'VS','3':'GND','4':'VOUT','5':None,'6':None,'7':None,'8':None}),
 dict(ref='C1',lib='Device:C',value='1uF',fp=C06,pins={'1':'VS','2':'GND'}),
 dict(ref='C2',lib='Device:C',value='10nF',fp=C06,pins={'1':'VS','2':'GND'}),
 dict(ref='C3',lib='Device:C',value='470pF',fp=C06,pins={'1':'VOUT','2':'GND'}),
 dict(ref='R1',lib='Device:R',value='1k',fp=R08,pins={'1':'VOUT','2':'MAPF'}),
 dict(ref='C4',lib='Device:C',value='100nF',fp=C06,pins={'1':'MAPF','2':'GND'}),
 dict(ref='JP1',lib='Jumper:SolderJumper_3_Bridged12',value='MAP int(1-2)/ext(2-3)',fp='Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm',
      pins={'1':'MAPF','2':'OUT','3':'EXT'}),
],hier=('VS','EXT','OUT'),inst_paths=[(f'/{RU}/{su}',3600)])
print('ok')

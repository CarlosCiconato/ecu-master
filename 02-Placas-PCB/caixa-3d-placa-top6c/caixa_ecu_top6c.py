# -*- coding: utf-8 -*-
"""
Caixa impressa em 3D para a placa top 6 camadas (200 x 90 mm, rascunho 7).
Fonte editável em CadQuery (Python). Todas as medidas em mm.

Coordenadas: X igual ao KiCad; Y = 90 - Y_KiCad (o lado dos conectores fica em Y=0,
o lado do USB-C fica em Y=90). Z=0 é a face de baixo da placa, Z=1.6 a de cima.

Montagem: a placa apoia nos 5 pilares da BASE; a TAMPA desce por cima, os conectores
Superseal passam pelos rasgos abertos embaixo da parede da tampa. 5 parafusos M3 entram
por baixo da base, atravessam a placa e prendem em insertos de latão M3 na tampa.

Rodar:  python3 caixa_ecu_top6c.py   -> gera base.stl, tampa.stl, caixa.step
"""
import cadquery as cq
import math, sys, os

# ---------------- parâmetros principais ----------------
PCB_W, PCB_H, PCB_T = 200.0, 90.0, 1.6
WALL   = 2.6     # espessura das paredes
FLOOR  = 2.4     # fundo da base
ROOF   = 2.4     # teto da tampa
GAP    = 0.6     # folga placa-parede (lados esquerdo/direito)
GAP_USB = 0.8    # folga do lado do USB (o USB-C passa 0,63 mm da borda)
CONN_FACE_KY = 90.5   # Y KiCad da face interna da parede dos conectores (flange do Superseal em 90,4)
UNDER  = 6.0     # espaço livre embaixo da placa (bateria CR2032 ~4,6; corte os pinos THT a 2 mm)
ABOVE  = 29.5    # espaço livre em cima da placa na parte ALTA (Superseal: 27,9 de altura total, catálogo TE)
ABOVE_LOW = 13.5 # espaço livre na parte BAIXA (eletrolíticos 8 mm até 12 mm de altura)
STEP_KY = 68.5   # Y KiCad onde a parte alta começa (corpo dos conectores começa em 69,9)
R_CORNER = 4.0

LIP_T, LIP_H, LIP_CLR = 1.2, 2.5, 0.2   # encaixe base/tampa

# Superseal 1.0 (medir na peça real e ajustar!)
SHROUD_W = {34: 34.5, 26: 28.5}  # largura da "boca" que fica fora da caixa
SHROUD_H = 23.0                  # altura da boca acima da placa (catálogo TE: 23,0)
SHROUD_Z0 = PCB_T                # onde começa a boca (assumido: na face de cima da placa)
SHROUD_CLR = 0.4                 # folga em volta da boca
CONNECTORS = [  # (nome, x KiCad, vias)
    ("A", 26.525, 34), ("C", 76.525, 26), ("B", 126.625, 34), ("D", 176.675, 26)]

# furos de fixação da placa (KiCad)
HOLES = {"H1": (4.5, 4.5), "H2": (195.5, 4.5), "H3": (53.0, 80.0),
         "H4": (153.0, 80.0), "H5": (100.0, 82.0)}
STANDOFF_D = 7.0     # pilar da base
POST_D = 6.4         # pilar da tampa (H2 tem o Q2600 a 3,6 mm; conectores a 3,4 mm)
USE_INSERTS = True   # True: furo para inserto M3 (Ø4,0 x 6); False: furo Ø2,6 para parafuso direto
SCREW_HOLE = 3.4
CBORE_D, CBORE_DEPTH = 6.5, 3.0

# USB-C (HRO TYPE-C-31-M-12), centro em X=78, altura 3,26 sobre a placa
USB_X, USB_W, USB_H = 78.0, 13.0, 7.6
USB_ZC = PCB_T + 1.63

# MAP (MPXH6400A) em KiCad (12, 16.17): bico para mangueira de vácuo no teto
MAP_X, MAP_KY = 12.0, 16.1667
MAP_PORT_TOP = 10.0   # altura do topo do bico do sensor sobre a placa (conferir na peça)
MAP_STUB_GAP = 1.5    # espaço entre o teto (bossa) e o bico do sensor (liga com mangueira de silicone)
MAP_BOSS_D = 9.0                            # reforço no teto, por dentro
MAP_THREAD_HOLE, MAP_THREAD_DEPTH = 4.2, 4.5  # furo para rosca M5 (espigão de latão)

# Antena Wi-Fi: furo para SMA de painel na parede do lado do USB, acima do U.FL do ESP32
SMA_X, SMA_D = 132.8, 6.6
SMA_ZC = PCB_T + 7.0
UFL_CHANNEL_W, UFL_CHANNEL_D = 3.2, 1.4   # canal para o cabo do U.FL passar pela borda da placa

# orelhas de fixação no carro (M5)
EARS_Y = (18.0, 72.0)
EAR_LEN, EAR_W, EAR_T, EAR_SLOT_D, EAR_SLOT_L = 13.0, 15.0, 4.0, 5.5, 8.0

# ---------------- geometria derivada ----------------
def Y(ky): return PCB_H - ky
X0, X1 = -GAP, PCB_W + GAP
Y0 = Y(CONN_FACE_KY)          # face interna da parede dos conectores
Y1 = PCB_H + GAP_USB          # face interna da parede do USB
OX0, OX1, OY0, OY1 = X0 - WALL, X1 + WALL, Y0 - WALL, Y1 + WALL
Z_FLOOR_TOP = -UNDER
Z_BOT = Z_FLOOR_TOP - FLOOR
Z_SPLIT = PCB_T
Z_CEIL = PCB_T + ABOVE
Z_TOP = Z_CEIL + ROOF
Z_CEIL_LOW = PCB_T + ABOVE_LOW
Z_TOP_LOW = Z_CEIL_LOW + ROOF
Y_STEP_IN = Y(STEP_KY)          # fim da parte alta, por dentro
Y_STEP_OUT = Y_STEP_IN + WALL   # fim da parte alta, por fora
def ceil_at(y): return Z_CEIL if y < Y_STEP_IN else Z_CEIL_LOW

def rbox(x0, y0, x1, y1, z0, z1, r):
    return (cq.Workplane("XY").workplane(offset=z0)
            .center((x0 + x1) / 2, (y0 + y1) / 2)
            .rect(x1 - x0, y1 - y0).extrude(z1 - z0)
            .edges("|Z").fillet(r))

def box(x0, y0, x1, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def cyl(x, y, z0, z1, d):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2).extrude(z1 - z0)

def openings():
    """Recortes que atravessam base e tampa (conectores, USB, SMA)."""
    cut = None
    def add(s):
        nonlocal cut
        cut = s if cut is None else cut.union(s)
    for _, kx, n in CONNECTORS:
        w = SHROUD_W[n] + 2 * SHROUD_CLR
        add(box(kx - w / 2, OY0 - 1, kx + w / 2, Y0 + 0.01,
                SHROUD_Z0 - SHROUD_CLR, SHROUD_Z0 + SHROUD_H + SHROUD_CLR))
    usb = (cq.Workplane("XZ").workplane(offset=-(Y1 - 0.01))
           .center(USB_X, USB_ZC).rect(USB_W, USB_H).extrude(-(WALL + 2))
           .edges("|Y").fillet(2.0))
    add(usb)
    sma = cq.Workplane("XZ").workplane(offset=-(Y1 - 0.01)).center(SMA_X, SMA_ZC).circle(SMA_D / 2).extrude(-(WALL + 2))
    add(sma)
    return cut

def make_base():
    outer = rbox(OX0, OY0, OX1, OY1, Z_BOT, Z_SPLIT, R_CORNER)
    inner = rbox(X0, Y0, X1, Y1, Z_FLOOR_TOP, Z_SPLIT + 1, max(R_CORNER - WALL, 0.8))
    base = outer.cut(inner)
    # lábio de encaixe (faixa interna da parede, sobe acima do plano de divisão)
    lip_o = rbox(X0 - LIP_T, Y0 - LIP_T, X1 + LIP_T, Y1 + LIP_T, Z_SPLIT, Z_SPLIT + LIP_H, max(R_CORNER - WALL + LIP_T, 1))
    lip_i = rbox(X0, Y0, X1, Y1, Z_SPLIT - 1, Z_SPLIT + LIP_H + 1, max(R_CORNER - WALL, 0.8))
    base = base.union(lip_o.cut(lip_i))
    # pilares + parafusos
    for _, (kx, ky) in HOLES.items():
        x, y = kx, Y(ky)
        base = base.union(cyl(x, y, Z_FLOOR_TOP - 0.1, 0.0, STANDOFF_D))
        base = base.cut(cyl(x, y, Z_BOT - 1, 0.0 + 0.1, SCREW_HOLE))
        base = base.cut(cyl(x, y, Z_BOT - 1, Z_BOT + CBORE_DEPTH, CBORE_D))
    # canal do cabo da antena (U.FL embaixo da placa -> SMA na tampa)
    base = base.cut(box(SMA_X - UFL_CHANNEL_W / 2, Y1 - 0.01, SMA_X + UFL_CHANNEL_W / 2, Y1 + UFL_CHANNEL_D,
                        Z_FLOOR_TOP, Z_SPLIT + LIP_H + 1))
    # orelhas
    for side in (-1, 1):
        for ey in EARS_Y:
            xw = OX0 if side < 0 else OX1
            xa = xw - EAR_LEN if side < 0 else xw - 1
            ear = (box(xa, ey - EAR_W / 2, xa + EAR_LEN + 1, ey + EAR_W / 2, Z_BOT, Z_BOT + EAR_T)
                   .edges("|Z").fillet(3.0))
            base = base.union(ear)
            sx = xw - EAR_LEN / 2 - 0.5 if side < 0 else xw + EAR_LEN / 2 - 0.5
            slot = (cq.Workplane("XY").workplane(offset=Z_BOT - 1).center(sx, ey)
                    .slot2D(EAR_SLOT_L + EAR_SLOT_D, EAR_SLOT_D, 0).extrude(EAR_T + 2))
            base = base.cut(slot)
    base = base.cut(openings())
    return base

def make_lid():
    # tampa em degrau: alta só na faixa dos conectores, baixa no resto
    low = rbox(OX0, OY0, OX1, OY1, Z_SPLIT, Z_TOP_LOW, R_CORNER).faces(">Z").edges().fillet(1.5)
    high = rbox(OX0, OY0, OX1, Y_STEP_OUT, Z_SPLIT, Z_TOP, R_CORNER).faces(">Z").edges().fillet(1.5)
    outer = low.union(high)
    r_in = max(R_CORNER - WALL, 0.8)
    inner = rbox(X0, Y0, X1, Y1, Z_SPLIT - 1, Z_CEIL_LOW, r_in).union(
            rbox(X0, Y0, X1, Y_STEP_IN, Z_SPLIT - 1, Z_CEIL, r_in))
    lid = outer.cut(inner)
    # rebaixo que recebe o lábio da base
    reb = rbox(X0 - LIP_T - LIP_CLR, Y0 - LIP_T - LIP_CLR, X1 + LIP_T + LIP_CLR, Y1 + LIP_T + LIP_CLR,
               Z_SPLIT - 1, Z_SPLIT + LIP_H + LIP_CLR, max(R_CORNER - WALL + LIP_T, 1))
    lid = lid.cut(reb)
    # pilares com inserto
    for _, (kx, ky) in HOLES.items():
        x, y = kx, Y(ky)
        lid = lid.union(cyl(x, y, Z_SPLIT, ceil_at(y) + 0.1, POST_D))
        if USE_INSERTS:
            lid = lid.cut(cyl(x, y, Z_SPLIT - 1, Z_SPLIT + 6.0, 4.0))
        else:
            lid = lid.cut(cyl(x, y, Z_SPLIT - 1, Z_SPLIT + 10.0, 2.6))
    # MAP: bossa no teto com furo para espigão de latão M5 (pneumático, mangueira 4 mm),
    # rosqueado direto no plástico (ou com macho M5). Por dentro, um tubo desce até perto
    # do bico do sensor; um pedaço de mangueira de silicone 3 mm liga o tubo ao sensor.
    mx, my = MAP_X, Y(MAP_KY)
    z_stub = min(PCB_T + MAP_PORT_TOP + MAP_STUB_GAP, Z_CEIL_LOW - 0.5)
    lid = lid.union(cyl(mx, my, z_stub, Z_CEIL_LOW + 0.1, MAP_BOSS_D))
    lid = lid.cut(cyl(mx, my, Z_TOP_LOW - MAP_THREAD_DEPTH, Z_TOP_LOW + 1, MAP_THREAD_HOLE))
    lid = lid.cut(cyl(mx, my, z_stub - 1, Z_TOP_LOW, 2.4))
    # texto no teto
    txt = (cq.Workplane("XY").workplane(offset=Z_TOP_LOW - 0.6)
           .center((OX0 + OX1) / 2, (Y_STEP_OUT + OY1) / 2)
           .text("ECU TOP 6C", 9, 1.0, kind="bold", halign="center", valign="center"))
    lid = lid.cut(txt)
    for name, kx, n in CONNECTORS:
        t = (cq.Workplane("XY").workplane(offset=Z_TOP - 0.6).center(kx, (OY0 + Y_STEP_OUT) / 2)
             .text(name, 7, 1.0, kind="bold", halign="center", valign="center"))
        lid = lid.cut(t)
    m = (cq.Workplane("XY").workplane(offset=Z_TOP_LOW - 0.6).center(mx + 7, my)
         .text("MAP", 5, 1.0, kind="bold", halign="left", valign="center"))
    lid = lid.cut(m)
    lid = lid.cut(openings())
    return lid

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    base, lid = make_base(), make_lid()
    cq.exporters.export(base.translate((0, 0, -Z_BOT)), os.path.join(out, "base.stl"), tolerance=0.02, angularTolerance=0.1)
    # a tampa sai no STL já virada para imprimir (teto alto na mesa; ligar suporte só na mesa embaixo do teto baixo)
    lid_print = lid.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, Z_TOP))
    cq.exporters.export(lid_print, os.path.join(out, "tampa.stl"), tolerance=0.02, angularTolerance=0.1)
    asm = cq.Assembly().add(base, name="base").add(lid, name="tampa")
    asm.save(os.path.join(out, "caixa.step"))
    print("ok", OX1 - OX0, OY1 - OY0, Z_TOP - Z_BOT, Z_TOP_LOW - Z_BOT, Y_STEP_OUT - OY0)

def export_viewer(out):
    """STLs na posição montada (para o visualizador)."""
    cq.exporters.export(make_base(), os.path.join(out, "v-base.stl"), tolerance=0.05, angularTolerance=0.2)
    cq.exporters.export(make_lid(), os.path.join(out, "v-tampa.stl"), tolerance=0.05, angularTolerance=0.2)

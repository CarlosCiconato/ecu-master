# Placa top 6 camadas (rascunho 5) · como cotar na JLC

Arquivos: gerber-top6c-r5.zip, bom-jlc-top6c-r5.csv, cpl-jlc-top6c-r5.csv.
Placa: 200 x 90 mm, 6 camadas, 0 ligações abertas (DRC 2026-11-09).

## Placa (PCB)
- Layers: 6 · Dimensões: 200 x 90 mm · Material FR-4 · Espessura 1,6 mm
- Ordem das camadas: F.Cu (gtl), In1 (g1, GND), In2 (g2, sinal), In3 (g3, +5V/+3V3), In4 (g4, sinal), B.Cu (gbl). A JLC reconhece pelos nomes.
- Stackup: o padrão da JLC para 6 camadas serve.
- Cobre externo: 1 oz (mais barato) ou 2 oz. As duas passam: a placa usa trilha mínima 0,20 mm e distância mínima 0,15 mm, e o limite da JLC com 2 oz em multicamada é 0,15/0,15 mm. Interno: 0,5 oz (padrão).
- Vias: 0,6/0,3 e 0,5/0,25 mm. Tem vias dentro do pad térmico dos TLE9201 (U10/U11): escolher "Epoxy Filled & Capped" (POFV) se a JLC oferecer grátis para 6 camadas; senão "Tented".
- Remove Order Number: "Specify a location" ou "Yes" (se pagar).

## Montagem (PCBA)
- Montagem dos DOIS lados: 306 peças em cima, 219 embaixo (525 no total, 98 linhas na BOM).
- Subir bom-jlc-top6c-r5.csv e cpl-jlc-top6c-r5.csv. Conferir a rotação das peças na prévia da JLC (principalmente CIs, diodos, MCU, ESP32).

## Soldar à mão (não vão na JLC)
- J101, J102, J103, J104: conectores Superseal (comprar fora)
- C17, C1001: capacitores 56 µF THT (EEH-AZF1H560B ou EEU-FR1H560)
- U3601: MAP MPXH6400AC6T1 (sem estoque na JLC; Mouser/DigiKey)
- J4 (Tag-Connect) e J105/J107/J108 (pontos de teste) não levam peça.

## Atenção
- Q2600 encosta no contorno do furo H2 (canto superior direito): confirmar que o parafuso não pega no transistor.
- Firmware: pinos do MCU mudaram, ver pinos-mcu-mudancas.md.

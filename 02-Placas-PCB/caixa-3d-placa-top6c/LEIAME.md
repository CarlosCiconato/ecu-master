# Caixa 3D da placa top 6 camadas (rascunho 7)

Versão 2, em degrau (estilo EMU PRO): a tampa é alta só na faixa dos conectores e baixa no resto. A primeira versão, de altura única, ficou em `v1-reta/`.

Arquivos:
- `base.stl`: fundo da caixa, já na posição de imprimir (fundo na mesa).
- `tampa.stl`: tampa, já virada para imprimir (teto alto na mesa). Precisa de suporte "só na mesa" (árvore), que fica só embaixo do teto baixo.
- `caixa.step`: as duas peças montadas, para abrir no Fusion, FreeCAD ou KiCad.
- `caixa_ecu_top6c.py`: o desenho editável (CadQuery). Todas as medidas ficam no topo do arquivo.
  Para gerar de novo: `pip install cadquery` e depois `python3 caixa_ecu_top6c.py saida`.
- `placa-fantasma.stl`: a placa com as peças em blocos de altura estimada, só para conferir.

## Medidas
- Externa 206,4 × 96,5 mm (232,4 mm com as orelhas). Altura 41,9 mm na faixa dos conectores (27,2 mm de profundidade) e 25,9 mm no resto.
- Parede 2,6 mm, fundo e teto 2,4 mm. 6 mm livres embaixo da placa (corte os pinos THT a 2 mm). Em cima: 29,5 mm na parte alta e 13,5 mm na baixa.
- A divisão entre base e tampa fica na face de cima da placa. A base tem um lábio de 2,5 mm que encaixa na tampa.
- Conferido no computador: nenhuma peça da placa (com as alturas estimadas) encosta na caixa.

## Como monta
1. Prenda os 5 insertos de latão M3 nos pilares da tampa com o ferro de solda.
2. Ponha a placa na base, apoiada nos 5 pilares (H1 a H5).
3. Desça a tampa por cima. Os quatro Superseal (A, C, B, D) passam pelos rasgos da parede, e a flange de cada um encosta por dentro.
4. Aperte os 5 parafusos M3 × 12 por baixo.

## Ferragens
- 5 parafusos M3 × 12 e 5 insertos M3 (Ø4 × 5,7 mm).
- MAP: espigão de latão M5 para mangueira de 4 mm, rosqueado no teto baixo, logo acima do sensor (furo de 4,2 mm; passe um macho M5 ou rosqueie direto, com veda-rosca). Sobram 1,5 mm entre o teto e o bico do sensor: um anelzinho de mangueira de silicone fecha essa folga.
- Wi-Fi: conector SMA fêmea de painel (furo de 6,6 mm na parede do lado do USB) e cabo U.FL–SMA de 10 a 15 cm. O cabo desce pelo canal da base, ao lado da placa, até o U.FL do ESP32, que fica embaixo.
- Fixação no carro: 4 orelhas com rasgo para M5.

## Impressão
ASA é o melhor para o cofre do motor (aguenta calor e sol). PETG também serve se a caixa ficar fora do motor. Bico 0,4, camada 0,2, 4 perímetros, 30 % de preenchimento.

## Conferir antes de imprimir (medidas que eu estimei)
- **Superseal 1.0:** usei o catálogo da TE: boca de 23 mm de altura, 27,9 mm no total, boca com 34,5 mm (34 vias) e 28,5 mm (26 vias) de largura. Meça a peça real e mude `SHROUD_H` e `SHROUD_W` no topo do .py.
- **Bico do MPXH6400A:** usei 10 mm de altura sobre a placa (`MAP_PORT_TOP`).
- **Capacitores eletrolíticos de 8 mm (C17, C1001):** a parte baixa aceita até 12 mm. Deitando os dois, dá para baixar a tampa uns 5 mm (`ABOVE_LOW`).
- Dica: imprima primeiro só uma tira da parede dos conectores, para testar o encaixe antes de gastar o material da caixa toda.

## Vedação
A caixa não é à prova d'água. Para o cofre do motor dá para pôr cordão de silicone no encaixe base/tampa e em volta das bocas dos Superseal. Se quiser, faço uma junta de TPU para imprimir.

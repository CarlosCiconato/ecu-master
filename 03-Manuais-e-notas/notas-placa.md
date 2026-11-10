# Notas para o projeto da placa (ECU própria com rusEFI)

Atualizado em 26/10/2026. Objetivo: decidir depois o que é viável, mantendo o custo baixo.

## 1. O que vimos nas referência (fotos do Carlos)

Nomes de chip lidos nas fotos; onde não dava para ler, está marcado como estimativa.

### módulo de referência (placa "módulo de referência A 1.6")
- Duas placas: frente (tela/botões) + trás (ECU), ligadas por conector e fita de 40 pinos.
- Microcontrolador: NXP Kinetis K22 (MK22FN128..., ARM Cortex-M4, pouca memória).
- Processador grande na placa da frente (~144 pinos, modelo ilegível): provavelmente tela/interface.
- NXP MC33888: driver de saídas (relés/solenoides/lâmpadas) com proteção e diagnóstico.
- Fileira de MOSFETs de potência (bicos/bobinas, estimativa).
- MAP interno (peça vermelha com entrada de mangueira), buzzer, USB mini.
- JTAG e pontos RX/TX/GND para programação e teste.
- Tela e ECU na MESMA caixa.

### módulo de referência (placa "módulo de referência-A 1.5")
- Microcontrolador: NXP MPC5644A (SPC5644AMVZ1), PowerPC e200z4 automotivo,
  ~4 MB flash, 192 KB RAM, com eTPU (coprocessador de tempo para ignição/injeção).
- MC33888 de novo (driver de saídas).
- Dois chips NXP família MC33... (número ilegível; drivers de ignição/saídas, estimativa).
- Um microcontrolador menor (~64 pinos), provavelmente USB/comunicação/tela.
- Conector "INTERFACE" 2x5 e vários JTAG.

### módulo de referência
- Microcontrolador: NXP MPC5777C (lido "SPC5777C..." espelhado na foto), PowerPC dual-core
  e200z7, até ~264 MHz, ~8 MB flash, 2 eTPU. Nível de ECU de montadora, chip caro.
- Dois chips grandes ao lado (BGA, ilegíveis): provavelmente memória externa ou outro processador.
- Três chips grandes em fila (TSSOP, ilegíveis): provavelmente drivers de saída tipo MC33888.
- Muitos drivers NXP pequenos (QFN) e uma fileira grande de MOSFETs/diodos de potência.
- Marcações "ETH" e "CAN" perto de um conector: Ethernet + CAN.
- Dois conectores placa-a-placa no topo (tela em placa separada).

## 2. O que isso significa para nós

- O rusEFI NÃO roda nos chips PowerPC (MPC5644A / MPC5777C). Roda em STM32 (F4, F7, H7).
- STM32 dá conta de rotação, injeção e ignição; o rusEFI faz o papel do eTPU com timers.
- Problema real que já encontramos: memória. No STM32F4 (Proteus F4) a memória rápida (CCM)
  onde fica a configuração tem só ~692 bytes livres depois dos nossos itens.

## 3. Sugestão inicial (a validar, foco em custo baixo)

| Parte | Opção barata | Opção mais forte | Observação |
|---|---|---|---|
| Microcontrolador | STM32F7 (ex.: F767) | STM32H7 (ex.: H743) | Ambos já suportados pelo rusEFI (Proteus F7/H7). Resolve o problema de memória. F4 só se cortarmos funções. |
| Driver de saídas | MOSFETs simples + proteção | TLE8888 ou MC33810 (já suportados pelo rusEFI) | Driver integrado custa mais, mas dá diagnóstico de fio aberto/curto. |
| Ignição | Saídas lógicas para bobina com módulo integrado | Drivers IGBT na placa | Bobina com módulo integrado reduz custo e calor na ECU. |
| MAP | Sensor externo | MAP interno na placa | Interno é mais limpo, um pouco mais caro. |
| Entradas rotação/comando | Condicionador VR + Hall com pull-up por software (item 9 já feito) | — | Já preparado no firmware. |
| Tela | Separada, via CAN (painel ou celular) | Integrada (estilo módulo de referência) | Separada: ECU perto do motor, menos fios, tela trocável. Integrada: compacta, mas mais cara e com toda fiação indo ao painel. |
| Comunicação | USB + CAN | + Bluetooth/Wi-Fi para o app | Wi-Fi/Bluetooth pode ser módulo pronto barato (ex.: ESP32). |
| Sonda wideband | 2 entradas analógicas 0–5 V (uma por bancada) + CAN para controladores externos | 2 controladores de sonda na própria placa (ex.: CJ125 ou similar) | **Pedido do Carlos (31/10/2026): a placa deve ter 2 sondas**, uma por lado em motor V (V6/V8). O firmware já aceita Lambda 1 e Lambda 2 com correção separada por bancada (`cylinderBankSelect`). |
| Motores DC (borboleta, eGate, marcha lenta DC) | 2 pontes H na placa + saídas lógicas (PWM + direção + enable) num conector, para ligar drivers de ponte H externos | Mais pontes H na placa | **Ideia do Carlos (31/10/2026):** por causa da corrente, deixar saídas de controle para um driver externo. O firmware já comanda ponte H externa por pinos comuns (directionPin1/2, controlPin, disablePin; modo de 2 fios para TLE7209/L6205 ou 1 fio para TLE9201/VNH2SP30). Para mais de 2 motores ao mesmo tempo falta o item 27 (firmware hoje limita a 2). |
| Programação | Conector SWD + pontos RX/TX | — | Como as referência fazem (JTAG/serial). |

## 4. Pendências
- Decidir tela junto ou separada.
- Escolher F7 ou H7 (custo x memória).
- Sondas: 2 na placa (decidido em 31/10/2026). Falta escolher se o controlador da sonda fica na placa ou é externo (analógico/CAN).
- Motores DC: deixar saídas de controle para drivers de ponte H externos (decidido em 31/10/2026). Definir quantas (casa com o item 27).
- Definir número de saídas (bicos, bobinas, PWM) que queremos de verdade.
- Fazer uma lista de peças com preço antes de desenhar a placa.

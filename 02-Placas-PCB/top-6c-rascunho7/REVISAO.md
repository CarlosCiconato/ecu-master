# Placa top 6 camadas · revisão antes do pedido (09/11/2026)

Versão para pedir: **rascunho 7**. Os arquivos para a JLC estão em `jlc-r7/`: Gerber novo, mais a BOM e o CPL, que não mudaram desde o r5. O arquivo para o KiCad 9 é `placa-top-6c-rascunho7-kicad9.zip`.

## O que mudou desde o rascunho 5
1. **Furo H5** (M3, igual aos outros) em (100, 82) mm, entre os conectores C e B. Perto dos conectores, é o único lugar livre sem mexer em trilha. No alto da placa, do lado esquerdo, ainda cabem outros furos, se precisar.
2. **MAP trocado de pino.** O MAP interno/externo (AIN14) estava no PF10, que só tem ADC3. Nesse pino o rusEFI não consegue fazer a média do MAP sincronizada com o giro. Agora o MAP está no PC0 (ADC1) e o AV1 foi para o PF10. A troca foi feita logo depois das vias de saída do processador. O DRC continua igual, sem nenhuma ligação aberta.

## Conferido e certo
- As 525 peças da BOM batem uma a uma com o CPL e com a placa, e todas têm código LCSC.
- As peças marcadas DNP ficaram fora da BOM, como devem: capacitores e resistores opcionais das sondas e do VR.
- Alimentação do processador: todos os VDD e VSS, VCAP1/2, VDDA com ferrite, VREF+ de 3,3 V (REF3333), PDR_ON e VDDUSB. BOOT0 tem pull-down e botão, e o reset tem RC e botão.
- Todos os periféricos estão nos pinos certos: CAN1 PD0/PD1, CAN2 PB12/PB13, SD no SPI3, USB PA11/12, I2C2 do baro, TIM4 do ETB e UART4 do ESP32 (PH13/PH14).
- As entradas de rotação e digitais usam linhas EXTI todas diferentes (6, 7, 8, 10, 11, 12, 13, 14, 15), sem conflito.
- ESP32-S3 com regulador próprio de 3,3 V, EN com RC e IO0 com pull-up. TX e RX estão cruzados certo, com resistores de 470 Ω. O 5 V vem do buck LMR14020, que dá 2 A.
- Divisor das entradas analógicas: 5,6k/10k, ou seja, fator 1,56. Pull-up das entradas de temperatura: 2,7k no 5 V de sensor. Os dois valores batem com o firmware.
- Q2600 x H2: a cabeça do parafuso M3 (5,5 mm) fica a 1 mm do transistor. Não use arruela maior que 7 mm.

## Atenção na montagem e no uso
- **JP1 e JP2 (knock) vêm abertos.** Para usar o sensor de detonação, é preciso fechar com solda.
- JP3601 já vem com o MAP interno ligado (1-2). Para usar MAP externo no B17, corte a ponte 1-2 e feche 2-3.
- **ESP32:** a placa não tem conector de gravação. O plano é gravar pelo próprio STM32, mas essa função ainda não existe no firmware. Plano B: segurar o STM32 em reset, ligar um adaptador USB-serial nos pads do R4003 e do R4004 e pôr o IO0 em GND pelo R4006.
- **Sondas (STM32F042):** a primeira gravação é pelo SWD, nos pads J2600 e J2700, que vêm sem conector. Precisa de um ST-Link. Depois disso a atualização é pela CAN.
- O PB2 está ligado direto no GND: o firmware nunca pode usá-lo como saída.
- Acabamento: ENIG em vez de OSP, porque você vai soldar coisas à mão depois.

## Esquema
O esquema v0.1 não é o desta placa: faltam o processador LQFP176, as sondas e o Wi-Fi, e ele ainda tem a ign3, SW5-8 e os LEDs. A referência é a própria placa (.kicad_pcb). **Nunca use "Atualizar PCB a partir do esquema"**, porque isso desfaz o roteamento.

## Firmware (Mac)
- Branch `board-nossa-top6c` (commit 502527fc249), pasta `firmware/config/boards/nossa_top6c`. A F7 compila sem erros, com 44,9% da flash usada. O TunerStudio funciona na UART4 junto com o USB, e o ADC3 foi ligado para as entradas lentas. Também corrigi 4 pontos no código comum. Resumo em `placa-top6c-firmware.md`.
- Commit 41d43cb4adf: MAP no PC0 (ADC rápido, com média) e AV1 no PF10. TPS e pedal agora vêm por padrão no AV2-AV5. Testes 2030/2030. Falta validar na bancada a mudança de prioridade do ADC.

## Interface (app v0.31)
- Os fios da placa agora têm o pino real do conector e do processador, por exemplo "Azul 1 (A13)" ou "Branco 17 (B17)". Entraram Amarelo 9-12 (LS17-20), Vermelho 1-4 (saídas de 12 V) e Verde 1-13 (entradas digitais).

## Ainda em aberto
- Estoque na JLC: preciso da lista de peças que apareceram sem estoque para achar substitutas.
- Tabela completa de pinos: `pinos-firmware.md`.

## eGate (decisão do Carlos, 09/11/2026 18h21)
A placa fica como está. Os pinos A9–A12 (antiga IGN9-12) ficam livres. O eGate grande vai num driver de potência externo, comandado por uma saída auxiliar negativa (LS9–LS16), com resistor de pull-up no driver; a saída é escolhida no app/TunerStudio. Um eGate pequeno pode ligar direto na segunda ponte H (C13–C14). O firmware continua com as 2 ETBs (commit 41d43cb4adf). Manual atualizado.

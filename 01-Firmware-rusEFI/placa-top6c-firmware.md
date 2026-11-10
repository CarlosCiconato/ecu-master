# Firmware da placa "nossa top 6c" (STM32F767IIT6) — 09/11/2026

Branch: board-nossa-top6c (a partir de traction-wheel-speeds). Commits: 502527fc249 (placa) e 41d43cb4adf (troca de pinos do rascunho 7, o mais novo). Nada foi enviado (sem push).
Pasta: firmware/config/boards/nossa_top6c (board.mk, board_configuration.cpp, nossa_top6c_meta.h,
adc3_slow_config.h, knock_config.h, prepend*.txt, connectors/main.yaml + gerados, meta-info-nossa_top6c.env, compile_nossa_top6c.sh).

## Atualização 09/11/2026: PCB rascunho 7 (commit 41d43cb4adf)
- MAP (AIN14, MPXH6400 interno ou externo, conector B17): PF10 -> PC0 (ADC1_IN10, EFI_ADC_10). Ele volta ao ADC rápido,
  com MAP averaging (média sincronizada) normal. Não é forçado para o modo lento (o fallback só vale para EFI_ADC_32..39).
- AV1 (conector B1): PC0 -> PF10 (ADC3_IN8, EFI_ADC_36, ADC3 lento). Continuam no ADC3 lento: AV1 PF10, AV11 PF9, AIN13 PF3.
- TPS/PPS padrão foram para AV2/AV3/AV4/AV5 (antes AV1..AV4), para não ficarem no ADC3, que é dividido com o knock.
- Compilação F7 OK: flash0 691.424 B de 1504 KB (44,9%), flash1 505.632 B (32,8%), ram3 112.612 B (85,9%), ram2 10.216 B (62,4%).
- Testes unitários: 2030/2030 OK (com as 4 mudanças no código comum).
- Arquivos regenerados guardados nos stashes "regen depois nossa_top6c" e "regen depois nossa_top6c rascunho 7".
- Os itens 1 das Respostas abaixo descrevem a situação ANTIGA (MAP no PF10).

## Decisão 09/11/2026 (18:21): eGate
- A placa fica como está, com as 2 pontes TLE9201 (ETB1 e ETB2 em PD13/PD7/PI3). O firmware mantém as 2 ETBs.
- As antigas saídas da eGate (A9-A12, ex-IGN9-12) já estão desligadas na placa e não aparecem no firmware.
- eGate grande: será comandada por um driver de potência externo (com pull-up do lado do driver), ligado a uma das
  saídas LS9-LS16. A escolha é feita no TunerStudio (saída do controle de boost), sem mudança de firmware.

## Respostas
1. ADC3 (PF3/PF9/PF10): o modo EFI_ADC3_SLOW já existia no rusEFI (stm32_adc_v2_adc3.cpp; adc_onchip_slow.cpp:67-71),
   mas nenhuma placa STM32 usava. Faltavam: a) o arquivo adc3_slow_config.h da placa (criado: EFI_ADC_35 PF9, 36 PF10, 37 PF3);
   b) a prioridade de IRQ do ADC igual à do agendador (static_assert em stm32_adc_v2_adc3.cpp:21; corrigido em
   hw_layer/ports/stm32/interrupt_priority.h, igual ao AT32). MAP no PF10: só como MAP lento. A média sincronizada
   (MapFast/MAP averaging) usa o ADC rápido (ADC2), que não tem o PF10. Antes dava erro crítico no boot
   (adc_onchip_fast.cpp:236). Agora o MAP cai em modo lento (adc_inputs.cpp addFastAdcChannel). Também corrigi a leitura
   fora do buffer de token 0xFF (adc_onchip_fast.cpp getAdcChannelToken). O ADC3 é dividido com o knock (PF4/PF5): durante
   a janela de knock a leitura lenta pode envelhecer (expira em 6 ms). RECOMENDAÇÃO: no PCB, mover o MAP para um pino
   ADC1/2 livre (ex.: PA6).
2. VBUS: sim, já desligado em todas as F7: hw_layer/ports/stm32/stm32f7/board.h:40 (BOARD_OTG_NOVBUSSENS) ->
   ChibiOS hal_usb_lld.c:63-67 (sem VBDEN). O PA9 pode ser saída.
3. TS na UART4 + USB ao mesmo tempo: sim (threads separadas: console/usb_console.cpp:59 e
   console/binary/tunerstudio_io_serial_ports.cpp:17-54). Defines em board.mk: TS_PRIMARY_UxART_PORT=SD4,
   EFI_TS_PRIMARY_IS_SERIAL=TRUE, STM32_SERIAL_USE_UART4=TRUE, EFI_CONSOLE_TX/RX_BRAIN_PIN=H13/H14, EFI_CONSOLE_AF=8.
   Velocidade = uartConsoleSerialSpeed (115200 padrão).

## Outras decisões
- Sem LEDs: LED_CRITICAL_ERROR_BRAIN_PIN=Unassigned e os getters de LED retornam Unassigned. O TURN_FATAL_LED
  agora checa porta nula (antes daria falha de barramento num erro fatal).
- ESP32: PI5 (IO0) e PI4 (EN) em nível alto no boot (boot normal).
- Pull-ups Hall: VR1 PG9 = crank1, VR2 PG14 = cam1, VR3 PD6 = cam2. Widebands no CAN1 (enableAemXSeries ligado).
- Flash de 2 MB (2mb_flash.mk). SPI5/MAX31855 da Proteus removidos (o PF9 é AV11).
- A CONFERIR NO PCB: divisor das entradas analógicas (copiado da Proteus 5,6k/10k = 1,56) e pull-up dos AT (2700 ohms).

## Compilação F7
OK, sem erros. flash0 691.424 B de 1504 KB (44,9%), flash1 505.632 B (32,8%), ram3 112.612 B de 128 KB (85,9%),
ram2 10.216 B (62,4%), ram0 100% (o heap ocupa o resto, normal). Config 29.548 B.
Para compilar: primeiro "gmake -r -o .ramdisk-sentinel config" e depois build/rusefi.elf (senão o make tenta
compilar os pinos gerados antes de gerá-los).

## Pendente
- Nada testado em placa real ainda (prioridade de IRQ do ADC igual à do agendador precisa ser validada na bancada).

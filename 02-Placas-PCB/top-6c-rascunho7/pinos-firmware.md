# Placa top 6c (rascunho 7) · pino do conector → pino do STM32F767IIT6

Tirado direto da placa (rascunho 5, igual no 6), seguindo cada trilha pelo driver até o conector.
Conectores: A = J101 motor 34p, B = J102 sensores 34p, C = J103 carro 26p, D = J104 sondas/extras 26p.

## Saídas
| Função | Conector | MCU |
|---|---|---|
| LS1 (bico 1) | A13 | PH6 |
| LS2 (bico 2) | A14 | PB14 |
| LS3 (bico 3) | A15 | PB15 |
| LS4 (bico 4) | A16 | PD9 |
| LS5 (bico 5) | A17 | PG3 |
| LS6 (bico 6) | A18 | PG4 |
| LS7 (bico 7) | A19 | PG5 |
| LS8 (bico 8) | A20 | PG6 |
| LS9 | A21 | PG8 |
| LS10 | A22 | PC7 |
| LS11 | A23 | PC8 |
| LS12 | A24 | PA8 |
| LS13 | A25 | PD10 |
| LS14 | A26 | PD11 |
| LS15 | A27 | PD15 |
| LS16 | A28 | PG2 |
| LS17 | D13 | PE2 |
| LS18 | D14 | PE3 |
| LS19 | D15 | PE4 |
| LS20 | D16 | PE5 |
| IGN1 | A1 | PD14 |
| IGN2 | A2 | PH8 |
| IGN3 | A3 | PH10 |
| IGN4 | A4 | PH11 |
| IGN5 | A5 | PD3 |
| IGN6 | A6 | PI0 |
| IGN7 | A7 | PH15 |
| IGN8 | A8 | PG7 |
| HS1 (12 V) | A29 | PH9 |
| HS2 (12 V) | A30 | PH7 |
| HS3 (12 V) | A31 | PH12 |
| HS4 (12 V) | A32 | PD8 |
| ETB1 PWM / DIR / DIS | C11-C12 | PD12 (TIM4_CH1) / PA9 / PI2 |
| ETB2 PWM / DIR / DIS | C13-C14 | PD13 (TIM4_CH2) / PD7 / PI3 |
| Pull-up Hall VR1 / VR2 / VR3 | interno | PG9 / PG14 / PD6 |

## Entradas
| Função | Conector | MCU |
|---|---|---|
| VR1 (rotação) | C15-C16 | PE7 |
| VR2 (fase) | C17-C18 | PE8 |
| VR3 | C19-C20 | PA10 |
| DIGITAL1-4 | C21-C24 | PC6, PE11, PE12, PE14 |
| DIGITAL5-6 | D25-D26 | PE13, PE15 |
| SW1-SW4 | D17-D20 | PF0, PF1, PF2, PF11 |
| AV1 | B1 | PF10 (só ADC3, canal 8) desde o rascunho 7 |
| AV2-AV4 | B2-B4 | PC1, PC2, PC3 (ADC 11-13) |
| AV5-AV8 | B5-B8 | PA0, PA1, PA2, PA3 (ADC 0-3) |
| AV9-AV10 | B9-B10 | PA4, PA5 (ADC 4-5) |
| AV11 | B11 | PF9 (só ADC3, canal 7) |
| AT1-AT4 (temperatura) | B12-B15 | PC4, PC5, PB0, PB1 (ADC 14, 15, 8, 9) |
| AIN13 | B16 | PF3 (só ADC3, canal 9) |
| AIN14 = MAP interno (jumper JP3601 1-2) ou externo B17 | B17 | PC0 (ADC 10) desde o rascunho 7 |
| Tensão da bateria (82k/10k) | interno | PA7 (ADC 7) |
| Knock 1 / 2 | B18 / B19 | PF4 / PF5 (ADC3 14/15) |
| 5V sensor 1 / 2 "power good" | interno | PH2 / PH3 |

## Comunicação e outros
- CAN1: PD0 RX / PD1 TX (C7-C8). CAN2: PB12 RX / PB13 TX (C9-C10). Os 2 wideband ficam na CAN1.
- SD: SPI3 PC10 SCK / PC11 MISO / PC12 MOSI, CS PD2.
- Baro LPS25HB: I2C2 PB10 SCL / PB11 SDA.
- USB: PA11/PA12 (USB-C na placa). Sem pino de VBUS: PA9 é ETB1 DIR, então o firmware tem que rodar com detecção de VBUS desligada.
- ESP32-S3: UART4 PH13 TX / PH14 RX, EN PI4, IO0 PI5.
- Cristal 8 MHz (PH0/PH1), cristal 32,768 kHz do relógio (PC14/PC15), bateria no VBAT.
- PB2 está ligado direto no GND: nunca usar como saída.
- Livres (reserva arrancada/nitro): PE6, PI8, PC13, PI9, PI10, PI11, PF6, PF7, PF8, PH4, PH5, PA6, PF12-PF15, PG0, PG1, PE9, PE10, PC9, PI1, PA15, PD4, PD5, PG10-PG13, PG15, PB3-PB9, PE0, PE1, PI6, PI7 (sem trilha até o conector; pinos A9-A12, B28-B34, C5, C6, C25, C26, D21-D24 do conector estão vazios).

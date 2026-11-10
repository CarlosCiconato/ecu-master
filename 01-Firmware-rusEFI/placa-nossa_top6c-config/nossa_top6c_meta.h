/**
 * @file nossa_top6c_meta.h
 *
 * Pin map of the "nossa top 6c" board (STM32F767IIT6, LQFP176, 2 MB flash).
 * Source: the board PCB (MCU pins).
 */

#pragma once

#include "defaults.h"

// Low side outputs (LS1..LS8 are the default injectors 1..8)
#define TOP6C_LS_1 H6
#define TOP6C_LS_2 B14
#define TOP6C_LS_3 B15
#define TOP6C_LS_4 D9
#define TOP6C_LS_5 G3
#define TOP6C_LS_6 G4
#define TOP6C_LS_7 G5
#define TOP6C_LS_8 G6
#define TOP6C_LS_9 G8
#define TOP6C_LS_10 C7
#define TOP6C_LS_11 C8
#define TOP6C_LS_12 A8
#define TOP6C_LS_13 D10
#define TOP6C_LS_14 D11
#define TOP6C_LS_15 D15
#define TOP6C_LS_16 G2
#define TOP6C_LS_17 E2
#define TOP6C_LS_18 E3
#define TOP6C_LS_19 E4
#define TOP6C_LS_20 E5

// Ignition, logic level for smart coils. Max 8 cylinders on this board.
#define TOP6C_IGN_1 D14
#define TOP6C_IGN_2 H8
#define TOP6C_IGN_3 H10
#define TOP6C_IGN_4 H11
#define TOP6C_IGN_5 D3
#define TOP6C_IGN_6 I0
#define TOP6C_IGN_7 H15
#define TOP6C_IGN_8 G7

// High side 12 V
#define TOP6C_HS_1 H9
#define TOP6C_HS_2 H7
#define TOP6C_HS_3 H12
#define TOP6C_HS_4 D8

// ETB, two TLE9201
#define TOP6C_ETB1_PWM D12
#define TOP6C_ETB1_DIR A9
#define TOP6C_ETB1_DIS I2
#define TOP6C_ETB2_PWM D13
#define TOP6C_ETB2_DIR D7
#define TOP6C_ETB2_DIS I3

// Hall pull-up enable outputs
#define TOP6C_VR1_PULLUP G9
#define TOP6C_VR2_PULLUP G14
#define TOP6C_VR3_PULLUP D6

// Trigger and digital inputs
#define TOP6C_VR_1 E7
#define TOP6C_VR_2 E8
#define TOP6C_VR_3 A10
#define TOP6C_DIGITAL_1 C6
#define TOP6C_DIGITAL_2 E11
#define TOP6C_DIGITAL_3 E12
#define TOP6C_DIGITAL_4 E14
#define TOP6C_DIGITAL_5 E13
#define TOP6C_DIGITAL_6 E15
#define TOP6C_SW_1 F0
#define TOP6C_SW_2 F1
#define TOP6C_SW_3 F2
#define TOP6C_SW_4 F11
// 5 V sensor supply power-good inputs
#define TOP6C_5V1_GOOD H2
#define TOP6C_5V2_GOOD H3

// ESP32-S3 on UART4 (PH13 TX / PH14 RX)
#define TOP6C_ESP_EN I4
#define TOP6C_ESP_IO0 I5

// Analog inputs
#define TOP6C_IN_AV_1 EFI_ADC_36   // PF10, ADC3 only (connector B1), PCB rascunho 7
#define TOP6C_IN_AV_2 EFI_ADC_11   // PC1
#define TOP6C_IN_AV_3 EFI_ADC_12   // PC2
#define TOP6C_IN_AV_4 EFI_ADC_13   // PC3
#define TOP6C_IN_AV_5 EFI_ADC_0    // PA0
#define TOP6C_IN_AV_6 EFI_ADC_1    // PA1
#define TOP6C_IN_AV_7 EFI_ADC_2    // PA2
#define TOP6C_IN_AV_8 EFI_ADC_3    // PA3
#define TOP6C_IN_AV_9 EFI_ADC_4    // PA4
#define TOP6C_IN_AV_10 EFI_ADC_5   // PA5
#define TOP6C_IN_AV_11 EFI_ADC_35  // PF9, ADC3 only
#define TOP6C_IN_AT_1 EFI_ADC_14   // PC4
#define TOP6C_IN_AT_2 EFI_ADC_15   // PC5
#define TOP6C_IN_AT_3 EFI_ADC_8    // PB0
#define TOP6C_IN_AT_4 EFI_ADC_9    // PB1
#define TOP6C_IN_AIN_13 EFI_ADC_37 // PF3, ADC3 only
#define TOP6C_IN_AIN_14 EFI_ADC_10 // PC0, ADC1/2: internal MAP MPXH6400A or external MAP (connector B17), PCB rascunho 7
#define TOP6C_IN_VBATT EFI_ADC_7   // PA7, divider 82k/10k

// Suggested defaults
#define TOP6C_IN_MAP TOP6C_IN_AIN_14
#define TOP6C_IN_CLT TOP6C_IN_AT_1
#define TOP6C_IN_IAT TOP6C_IN_AT_2
// TPS/PPS kept off AV1: AV1 is ADC3 slow, shared with knock (stale reads during knock windows).
#define TOP6C_IN_TPS TOP6C_IN_AV_2
#define TOP6C_IN_TPS1_2 TOP6C_IN_AV_3
#define TOP6C_IN_PPS TOP6C_IN_AV_4
#define TOP6C_IN_PPS2 TOP6C_IN_AV_5

// Thermistor pull-up, copied from Proteus. CHECK against the PCB.
#define TOP6C_DEFAULT_AT_PULLUP 2700

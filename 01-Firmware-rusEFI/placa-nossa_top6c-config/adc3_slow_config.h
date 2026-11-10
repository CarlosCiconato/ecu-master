/**
 * @file adc3_slow_config.h
 *
 * ADC3-only pins read as normal slow analog inputs (EFI_ADC3_SLOW, see stm32_adc_v2_adc3.cpp).
 * ADC3 is shared with software knock (PF4/PF5): a knock window preempts a slow batch.
 */

#pragma once

#define ADC3_SLOW_CHANNELS { \
	EFI_ADC_35, /* PF9  ADC3_IN7, AV11 */ \
	EFI_ADC_36, /* PF10 ADC3_IN8, AV1 */ \
	EFI_ADC_37, /* PF3  ADC3_IN9, AIN13 */ \
}

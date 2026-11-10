/**
 * @file boards/nossa_top6c/board_configuration.cpp
 *
 * @brief Configuration defaults for the "nossa top 6c" board (STM32F767IIT6).
 *
 * Based on the Proteus board configuration.
 * This board has no LEDs: status LED getters return Gpio::Unassigned and
 * LED_CRITICAL_ERROR_BRAIN_PIN is Gpio::Unassigned (board.mk).
 * PB2 is hard-wired to GND: never configure it as an output.
 */

#include "pch.h"
#include "basic_configuration.h"
#include "nossa_top6c_meta.h"
#include "board_overrides.h"

static const brain_pin_e injPins[] = {
	Gpio::TOP6C_LS_1,
	Gpio::TOP6C_LS_2,
	Gpio::TOP6C_LS_3,
	Gpio::TOP6C_LS_4,
	Gpio::TOP6C_LS_5,
	Gpio::TOP6C_LS_6,
	Gpio::TOP6C_LS_7,
	Gpio::TOP6C_LS_8,
};

static const brain_pin_e ignPins[] = {
	Gpio::TOP6C_IGN_1,
	Gpio::TOP6C_IGN_2,
	Gpio::TOP6C_IGN_3,
	Gpio::TOP6C_IGN_4,
	Gpio::TOP6C_IGN_5,
	Gpio::TOP6C_IGN_6,
	Gpio::TOP6C_IGN_7,
	Gpio::TOP6C_IGN_8,
};

static void setInjectorPins() {
	for (size_t i = 0; i < efi::size(engineConfiguration->injectionPins); i++) {
		engineConfiguration->injectionPins[i] = i < efi::size(injPins) ? injPins[i] : Gpio::Unassigned;
	}
}

static void setIgnitionPins() {
	for (size_t i = 0; i < efi::size(engineConfiguration->ignitionPins); i++) {
		engineConfiguration->ignitionPins[i] = i < efi::size(ignPins) ? ignPins[i] : Gpio::Unassigned;
	}
}

// No LEDs on this board
Gpio getCommsLedPin() {
	return Gpio::Unassigned;
}

Gpio getRunningLedPin() {
	return Gpio::Unassigned;
}

Gpio getWarningLedPin() {
	return Gpio::Unassigned;
}

static void setupVbatt() {
	// Analog input divider: copied from Proteus (5.6k high side/10k low side). CHECK against the PCB.
	engineConfiguration->analogInputDividerCoefficient = 1.56f;

	// 82k high side/10k low side = 9.2
	engineConfiguration->vbattDividerCoeff = (92.0f / 10.0f);

	// Battery sense on PA7
	engineConfiguration->vbattAdcChannel = TOP6C_IN_VBATT;

	engineConfiguration->adcVcc = 3.3f;
}

static void setupEtb() {
	setupTLE9201IncludingStepper(Gpio::TOP6C_ETB1_PWM, Gpio::TOP6C_ETB1_DIR, Gpio::TOP6C_ETB1_DIS);
	setupTLE9201IncludingStepper(Gpio::TOP6C_ETB2_PWM, Gpio::TOP6C_ETB2_DIR, Gpio::TOP6C_ETB2_DIS, 1);
}

static bool applyTop6cBasicConfiguration(BasicConfigurationAction action) {
	return applyBasicConfiguration(action,
		setupEtb,
		TOP6C_IN_TPS,
		TOP6C_IN_TPS1_2,
		TOP6C_IN_PPS,
		TOP6C_IN_PPS2);
}

static void setupDefaultSensorInputs() {
	// VR1 = crank, VR2 = cam
	engineConfiguration->triggerInputPins[0] = Gpio::TOP6C_VR_1;
	engineConfiguration->triggerInputPins[1] = Gpio::Unassigned;
	engineConfiguration->camInputs[0] = Gpio::TOP6C_VR_2;

	// Hall pull-up enable outputs (turned on only when the input type is Hall)
	engineConfiguration->hallPullupCrank1Pin = Gpio::TOP6C_VR1_PULLUP;
	engineConfiguration->hallPullupCam1Pin = Gpio::TOP6C_VR2_PULLUP;
	// VR3 (PA10) is not assigned by default; its pull-up is offered as cam input 2
	engineConfiguration->hallPullupCam2Pin = Gpio::TOP6C_VR3_PULLUP;

	engineConfiguration->clt.adcChannel = TOP6C_IN_CLT;
	engineConfiguration->iat.adcChannel = TOP6C_IN_IAT;
	engineConfiguration->tps1_1AdcChannel = TOP6C_IN_TPS;

	// Internal MAP sensor MPXH6400A (4 bar) on AIN14 / PC0 (ADC1/2: fast ADC, crank-synced MAP averaging works)
	engineConfiguration->map.sensor.hwChannel = TOP6C_IN_MAP;
	engineConfiguration->map.sensor.type = MT_MPXH6400;

	// Both onboard rusEFI wideband controllers are on CAN1
	engineConfiguration->enableAemXSeries = true;
	engineConfiguration->widebandOnSecondBus = false;
}

static void setupSdCard() {
	engineConfiguration->sdCardSpiDevice = SPI_DEVICE_3;
	engineConfiguration->sdCardCsPin = Gpio::D2;

	engineConfiguration->is_enabled_spi_3 = true;
	engineConfiguration->spi3sckPin = Gpio::C10;
	engineConfiguration->spi3misoPin = Gpio::C11;
	engineConfiguration->spi3mosiPin = Gpio::C12;
}

static void top6c_boardConfigOverrides() {
	setupSdCard();
	setupVbatt();

	engineConfiguration->clt.config.bias_resistor = TOP6C_DEFAULT_AT_PULLUP;
	engineConfiguration->iat.config.bias_resistor = TOP6C_DEFAULT_AT_PULLUP;

	engineConfiguration->canTxPin = Gpio::D1;
	engineConfiguration->canRxPin = Gpio::D0;
	engineConfiguration->can2RxPin = Gpio::B12;
	engineConfiguration->can2TxPin = Gpio::B13;

	engineConfiguration->lps25BaroSensorScl = Gpio::B10;
	engineConfiguration->lps25BaroSensorSda = Gpio::B11;
}

static void top6c_boardDefaultConfiguration() {
	setInjectorPins();
	setIgnitionPins();
	setupEtb();

	engineConfiguration->isSdCardEnabled = true;

	setupDefaultSensorInputs();

	engineConfiguration->enableSoftwareKnock = true;
}

// ESP32-S3: IO0 high = normal boot from flash, EN high = run.
static void top6c_boardInitHardware() {
#if EFI_PROD_CODE
	palSetLine(PAL_LINE(GPIOI, 5));
	palSetLineMode(PAL_LINE(GPIOI, 5), PAL_MODE_OUTPUT_PUSHPULL);
	palSetLine(PAL_LINE(GPIOI, 4));
	palSetLineMode(PAL_LINE(GPIOI, 4), PAL_MODE_OUTPUT_PUSHPULL);
#endif // EFI_PROD_CODE
}

void boardPrepareForStop() {
	// Wake on the CAN RX pin
	palEnableLineEvent(PAL_LINE(GPIOD, 0), PAL_EVENT_MODE_RISING_EDGE);
}

void setup_custom_board_overrides() {
	custom_board_DefaultConfiguration = top6c_boardDefaultConfiguration;
	custom_board_ConfigOverrides = top6c_boardConfigOverrides;
	custom_board_applyBasicConfiguration = applyTop6cBasicConfiguration;
	custom_board_InitHardware = top6c_boardInitHardware;
}

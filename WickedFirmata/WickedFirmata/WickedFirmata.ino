/*
 * WickedFirmata.ino generated by FirmataBuilder
 * Wed Aug 02 2017 14:58:42 GMT-0400 (EDT)
 */

#include <ConfigurableFirmata.h>

#include <DigitalInputFirmata.h>
DigitalInputFirmata digitalInput;

#include <DigitalOutputFirmata.h>
DigitalOutputFirmata digitalOutput;

#include <AnalogInputFirmata.h>
AnalogInputFirmata analogInput;

#include <AnalogOutputFirmata.h>
AnalogOutputFirmata analogOutput;

#include <Servo.h>
#include <ServoFirmata.h>
ServoFirmata servo;

#include <StepperFirmata.h>
StepperFirmata stepper;

#include <SerialFirmata.h>
SerialFirmata serial;

#include <FirmataScheduler.h>
FirmataScheduler scheduler;

#include <FirmataExt.h>
FirmataExt firmataExt;

#include <AnalogWrite.h>

#include <FirmataReporting.h>
FirmataReporting reporting;

void systemResetCallback()
{
  for (byte i = 0; i < TOTAL_PINS; i++) {
    if (IS_PIN_ANALOG(i)) {
      Firmata.setPinMode(i, ANALOG);
    } else if (IS_PIN_DIGITAL(i)) {
      Firmata.setPinMode(i, OUTPUT);
    }
  }
  firmataExt.reset();
}

void initTransport()
{
  // Uncomment to save a couple of seconds by disabling the startup blink sequence.
  // Firmata.disableBlinkVersion();
  Firmata.begin(57600);
}

void initFirmata()
{
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);

  firmataExt.addFeature(digitalInput);
  firmataExt.addFeature(digitalOutput);
  firmataExt.addFeature(analogInput);
  firmataExt.addFeature(analogOutput);
  firmataExt.addFeature(servo);
  firmataExt.addFeature(stepper);
  firmataExt.addFeature(serial);
  firmataExt.addFeature(scheduler);
  firmataExt.addFeature(reporting);

  Firmata.attach(SYSTEM_RESET, systemResetCallback);
}

void setup()
{
  initFirmata();

  initTransport();

  systemResetCallback();
}

void loop()
{
  digitalInput.report();

  while(Firmata.available()) {
    Firmata.processInput();
    if (!Firmata.isParsingMessage()) {
      goto runtasks;
    }
  }
  if (!Firmata.isParsingMessage()) {
runtasks: scheduler.runTasks();
  }

  if (reporting.elapsed()) {
    analogInput.report();
  }

  stepper.update();
  serial.update();
}

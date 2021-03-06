/*
 * Firmata is a generic protocol for communicating with microcontrollers
 * from software on a host computer. It is intended to work with
 * any host computer software package.
 *
 * To download a host software package, please clink on the following link
 * to open the download page in your default browser.
 *
 * http://firmata.org/wiki/Download
 */

/* This firmware supports as many servos as possible using the Servo library 
 * included in Arduino 0017
 *
 * TODO add message to configure minPulse/maxPulse/degrees
 *
 * This example code is in the public domain.
 */
 
#include <Servo.h>
#include <Firmata.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

Servo servos[MAX_SERVOS];

void analogWriteCallback(byte pin, int value)
{
    if (IS_PIN_SERVO(pin)) {
        servos[PIN_TO_SERVO(pin)].write(value);
    }
}

//pin assignments
// pin 0 is rx , pin 1 is tx
// pin 2 is HIGH when test is running, low when warming up
// pin 3 is HIGH when we are heating
// pin 4 is HIGH when we are stable
// pin 5 is HIGH when we enable temp servo control
// pin 6 is the flickRGB i/o pin
// pin 7 is HIGH when we enable the COOL/OFF/HEAT servo
// future:
// pin 8 and 9 work together (binary add) to get blinkrate
// pin 9=0, 8=1 Blinkrate = 1
// pin 9=1, 8=0 Blinkrate = 2
// pin 9=1, 8=1 Blinkrate = 3
// pin 9 = 0 and 8 = 0 --> buzzer on
// pin 10  - servo01
// pin 11  - servo02

int testrunPin = 2;
int testrunval = 0;     // 0 means we are not running a test right now
int heatingPin = 3;
int heatingval = 0;  // are we heating or cooling?
int stablePin = 4;
int stableval = 0;  // is the temp in the chamber stable?
int servopowerPin = 5;
int servopowerval = 0; // should the servo be powered or not?

int redval = 0;
int blueval = 0; 
int greenval=0;

int liteon = 0;
int liteblink = 0;
int blinkrate = 0; 

int i = 1; 

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            6

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      1

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 1000; // delay for half a second

void setup() 
{
  pinMode(testrunPin, INPUT);      // sets the digital pins as input
  pinMode(heatingPin , INPUT);     
  pinMode(stablePin, INPUT);      
  pinMode(servopowerPin, INPUT);

    byte pin;

    Firmata.setFirmwareVersion(0, 2);
    Firmata.attach(ANALOG_MESSAGE, analogWriteCallback);

    for (pin=0; pin < TOTAL_PINS; pin++) {
        if (IS_PIN_SERVO(pin)) {
        servos[PIN_TO_SERVO(pin)].attach(PIN_TO_DIGITAL(pin));
        }
    }
   
    Firmata.begin(57600);
    pixels.begin(); // This initializes the NeoPixel library.
}

void loop() 
{
    while(Firmata.available())
        Firmata.processInput();
 
 //read some input pins and do cool stuff based on the results
 
   testrunval = digitalRead(testrunPin);   // read the input pins
   heatingval = digitalRead(heatingPin);  // are we heating or cooling?
   stableval = digitalRead(stablePin);  // are we stable or not?
   servopowerval = digitalRead(servopowerPin);   // are we making a change?
   
    // We only have one flickRGB right now, so we don't need to worry about cycling through them 
    //  for(int i=0;i<NUMPIXELS;i++)
      i=0;
   
   // uncomment for testing
   //testrunval = 1;
   //stableval = 1;
   //heatingval = 1;
   //servopowerval = 1;
   
   if (testrunval == 0) {
            redval = 200;
            greenval = 200;
            blueval = 200;   
            blinkrate = 0; 
    }
    else {
      if (servopowerval == 1) {
            redval = 255;
            greenval = 180;
            blueval = 0;   
            blinkrate = 3; 
          }
        
      else {
        if (stableval == 0 )
          {
          blinkrate = 1;  
          // set the led color based on the value of heatingval
          if (heatingval == 1) {
            redval = 255;
            greenval = 0;
            blueval = 0;
          }
          else {
            redval = 0;
            greenval = 0;
            blueval = 255;   

           }
          }
        else
        {
          // stable, so steady green
          blinkrate = 0;
          redval = 0;
          greenval = 255;
          blueval = 0;   
        }   
        
         } // end servopower check  

        // digitalWrite(pin, val);    // should we plan to write pins, or always let firmata set them?
         
        // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
        pixels.setPixelColor(i, pixels.Color(redval,greenval,blueval));
        pixels.show(); // This sends the updated pixel color to the hardware.
       
        if (blinkrate == 0) {
            delay(delayval*2); // Delay for a period of time (in milliseconds).
         }
         else {
          delay(delayval/blinkrate); // Delay for a period of time (in milliseconds).
          pixels.setPixelColor(i, pixels.Color(0,0,0));
          pixels.show(); // This sends the updated pixel color to the hardware.
          delay(delayval/blinkrate); // Delay for a period of time (in milliseconds).
        }
    } // end onoff check

        //delay(delayval); // Delay for a period of time (in milliseconds).

        //end for loop for neopixel count
      

}

import os
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
#Setup variables for user input
led_choice = 0
count = 0

os.system('clear')

print "Which LED you want to blink?"
print "1: Red?"
print "2: Blue?"
print "3: Yellow?"
print "4: All?"
led_choice = input("Make your choice: ")

if led_choice == 1:
  os.system('clear')
  print "You choose the red LED"
  count = input("How many times you want it to blink?: ")
  while count > 0:
    print("red")
    GPIO.output(36,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(36,GPIO.LOW)
    time.sleep(1)
    count = count - 1

if led_choice == 2:
  os.system('clear')
  print "You choose the blue LED"
  count = input("How many times you want it to blink?: ")
  while count > 0:
    GPIO.output(37,GPIO.HIGH)
    print("blue")
    time.sleep(1)
    GPIO.output(37,GPIO.LOW)
    time.sleep(1)
    count = count - 1

if led_choice == 3:
  os.system('clear')
  print "You choose the yellow LED"
  count = input("How many times you want it to blink?: ")
  while count > 0:
    GPIO.output(13,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(13,GPIO.LOW)
    time.sleep(1)
    count = count - 1

if led_choice == 4:
  os.system('clear')
  print "You choose all LEDs"
  count = input("How many times you want them to blink?: ")
  while count > 0:
    GPIO.output(36,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(36,GPIO.LOW)

    GPIO.output(37,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(37,GPIO.LOW)

    GPIO.output(13,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(13,GPIO.LOW)

    count = count - 1


GPIO.cleanup()

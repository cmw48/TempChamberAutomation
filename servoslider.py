#!/usr/bin/python
 
import pyfirmata
board = pyfirmata.Arduino('/dev/ttyACM0')

board.digital[5].write(1) 
board.digital[5].write(1)
board.digital[4].write(1)
board.digital[2].write(1)

# set up pin D9 as Servo Output
pin11 = board.get_pin('d:11:s')
 
pin11.write(30)
pin11.write(45)
pin11.write(75)
pin11.write(2)


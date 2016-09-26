import time
import serial

ser = serial.Serial(
    port='COM126',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout=5
)

ser.setRTS(False)
time.sleep(0.5)
ser.setRTS(True)
time.sleep(0.5)
ser.setRTS(False)

if ser.isOpen():
    ser.close()

ser.open() 
ser.write('D')
s=ser.read(13)
print s
ser.close
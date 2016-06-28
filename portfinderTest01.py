import serial
import sys
import time
import serial.tools.list_ports

serPort = ""
int1 = 0
str1 = ""
str2 = ""

# Find Live Ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
   print p # This causes each port's information to be printed out.
           # To search this p data, use p[1].

   while int1 < 99:   # Loop checks "COM0" to "COM98" for Adruino Port Info. 

      if "CH340" in p[1]:  # Looks for "CH340" in P[1].
            str2 = str(int1) # Converts an Integer to a String, allowing:
            str1 = "COM" + str2 # add the strings together.

      if "CH340" in p[1] and str1 in p[1]: # Looks for "CH340" and "COM#"
         print "Found Arduino Uno on " + str1
         int1 = 99 # Causes loop to end.

      if int1 == 98:
         print str(int1) + " - UNO not found!"
         sys.exit() # Terminates Script.

      int1 = int1 + 1

time.sleep(5)  # Gives user 5 seconds to view Port information -- can be   changed/removed.

# Set Port
ser = serial.Serial(str1, 9600, timeout=10) # Put in your speed and timeout value.

# This begins the opening and printout of data from the Adruino.

ser.close()  # In case the port is already open this closes it.
ser.open()   # Reopen the port.

ser.flushInput()
ser.flushOutput()

int1 = 0
str1 = ""
str2 = ""

while int1==0:

   if "\n" not in str1:        # concatinates string on one line till a line feed "\n"
      str2 = ser.readline()    # is found, then prints the line.
      str1 += str2
   print(str1)
   str1=""
   time.sleep(.1)

print 'serial closed'
ser.close()
#!/usr/bin/python 
# but not that python, use Anaconda
#
# Copyright (c) 2016 Chris Westling <cmwestling@gmail.com>
# All Rights Reserved
# 
# includes the Paho Python MQTT client - find resources at 
#     http://www.eclipse.org/paho/
#

# This code is to non-invasively automate the Thermotron temp chamber
 
#TODO userio to enter an egg serial before each run
#TODO implement raspi 

import paho.mqtt.client as paho
import json
import datetime
import time
import sys
import getopt
from pyfirmata import Arduino, util

board = Arduino('/dev/ttyUSB0')

#declare a global list of temps
recent_temps=[]
temp_record=[]
deltas=[]


# why does this need to be here instead of in main?
global startblvrun
global M 
global msgCount
msgCount = 0

class MQTT_Message:

    def __init__(self):
        self.values = []      # creates a new list of values for each message
        self.tempc = 0
        
    def setmessage(self, msg_json):
        try:

            self.values = msg_json
            self.tempc = self.values['raw-instant-value'] 
            
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected errorC:", sys.exc_info()[0]
   
    def getmessage(self):
        try:
            print(self.values)
            print(str(self.values['raw-instant-value']))

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except:
            print "Unexpected errorA:", sys.exc_info()[0]    
            


# squawk when subscribe to egg topic is successful
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# do something as each message is received 
# TODO: break all the workywork out of this function and just return the message to the main code 
# should this be a Message object?  (it's not really pervasive...)
def on_message(client, userdata, msg):
    try:
        global isStable
        global startStable
        global stopStable
        global startUnstable
        global stopUnstable
        global msgCount
        global M
        global lastMessageTimeStamp
        # msgack deprecated
        global msgAck
        msgAck = 1  

        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
        #samplePayload m = {"serial-number":"egg00802a548c180123","converted-value":25.96,"converted-units":"degC","raw-value":25.96,"raw-instant-value":25.96,"raw-units":"degC","sensor-part-number":"SHT25"}
        parsed_msg = json.loads(msg.payload)
        M.setmessage(parsed_msg)
        msgCount = msgCount + 1
        lastMessageTimeStamp = time.time()     
        
        raw_instant_temp = (parsed_msg['raw-instant-value'])
        temp_record.append([raw_instant_temp, time.time()])   
        recent_temps.append(raw_instant_temp)

        # review recent temps and report
        templistlen = len(recent_temps)
        if templistlen <= 10: 
          #once we are warmed up, this condition won't be met and this code will not run
          #use this spot to initialize local variables until we get threading working
          # set servopower flag to on
          board.digital[5].write(1)
          startStable = time.time()
          stopUnstable = time.time()
          stopStable = time.time() 
          startUnstable = time.time() 
          isStable = False
          print ("gathering data, ready in " + str(11-templistlen)+"...")
          # fill up deltaslist
          deltas.append(templistlen)
        elif templistlen > 10 :
          # set servopower flag to off
          board.digital[5].write(0)
          
          for x in range (0, 10):
            deltas[x]=(recent_temps[x] - recent_temps[x+1])
          # print(deltas)
          # print(sum(deltas))
          #f.write(str(sum(deltas)))
          #json.dump(recent_temps[10], f)
          recent_temps.pop(0)
          #print(recent_temps[9])
          #print(temp_record)
          tempmsg = ""
          if abs(sum(deltas)) == 0 :
            if isStable :
              tempmsg = (str(recent_temps[9]) + " ...STABLE... " + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
              board.digital[4].write(1)
            else:
              isStable = True
              board.digital[4].write(1)
              tempmsg = (str(recent_temps[9]) + "STABILITY LOCK" + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
              startStable = time.time()
              stopUnstable = time.time()
          elif 0 < abs(sum(deltas)) <= 0.05:
            tempmsg = (str(recent_temps[9]) +"  ..stable..  " + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
          elif  0.05 < abs(sum(deltas)) <= 0.1:
            tempmsg = (str(recent_temps[9]) +"   .nominal.  "  + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
          elif 0.1 < abs(sum(deltas)) <= .3:
            if isStable :
              isStable = False
              board.digital[4].write(0)
              stopStable = time.time() 
              startUnstable = time.time() 
              tempmsg = (str(recent_temps[9]) + "**NOT STABLE**" + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
            else:
              tempmsg = (str(recent_temps[9]) + "--UNSTABLE-- " + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
          else:
            tempmsg = (str(recent_temps[9]) +" change/slope " + str(sum(deltas)) + "   " + time.ctime(int(time.time())))
            #print(isStable)
          if isStable:
            print(tempmsg + " stable for " + (time.strftime("%H:%M:%S", time.gmtime(time.time()-startStable))))
          else: 
            print(tempmsg + " elapsed... " + (time.strftime("%H:%M:%S", time.gmtime(time.time()-startUnstable))))
          if (sum(deltas)) > 0:
            board.digital[3].write(0)
          else:
            board.digital[3].write(1)          
                       
        else:
          print("templist error, this should never happen.") 
    except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
      print "Could not convert data to an integer."
    except:
      print "Unexpected error:", sys.exc_info()[0]
      #raise

def main(argv):


    #
    #pin assignments
    # pin 0 is rx , pin 1 is tx
    # pin 2 is HIGH when test is running, low when warming up
    # pin 3 is HIGH when we are heating
    # pin 4 is HIGH when we are stable
    # pin 5 is HIGH when we enable temp servo control
    # pin 6 is the flickRGB i/o pin
    # pin 7 is HIGH when we enable the COOL/OFF/HEAT servo
    # future:
    # pin 8 and 9 work together (binary add) to get blinkrate
    # pin 9=0, 8=1 Blinkrate = 1
    # pin 9=1, 8=0 Blinkrate = 2
    # pin 9=1, 8=1 Blinkrate = 3
    # pin 9 = 0 and 8 = 0 --> buzzer on
    # pin 10  - servo01
    # pin 11  - servo02

    #int testrunPin = 2;
    #int testrunval = 0;     // 0 means we are not running a test right now
    #int heatingPin = 3;
    #int heatingval = 0;     // are we heating or cooling?
    #int stablePin = 4;
    #int stableval = 0;      // is the temp in the chamber stable?
    #int servopowerPin = 5;
    #int servopowerval = 0;  // should the servo be powered or not?


    try:
        while 1 == 1:
            board.digital[2].write(1)
            board.digital[3].write(1)
            board.digital[4].write(1)
            time.sleep(3)
            board.digital[2].write(1)
            board.digital[3].write(0)
            board.digital[4].write(0)
            time.sleep(3)
            board.digital[2].write(1)
            board.digital[3].write(1)
            board.digital[4].write(0)
            time.sleep(3)

    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        # change power flag to off
        # change arduino LED to green
        board.digital[5].write(0)
        board.digital[4].write(0)
        board.digital[2].write(0)

if __name__ == "__main__":
    main(sys.argv[1:])
  

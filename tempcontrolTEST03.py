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

#declare a global list of temps
recent_temps=[]
temp_record=[]
deltas=[]


# why does this need to be here instead of in main?
global startblvrun
global M 
global msgCount
msgCount = 0

class MyClass:
    """A simple example class"""
    i = 12345

    def f(self, anyname):
        karen = "hello " + str(anyname)
        return karen
        
class MQTT_Message:

    def __init__(self):
        self.values = []      # creates a new list of values for each message
        self.tempc = 0
        
    def setmessage(self, msg_json):
        try:

            self.values = msg_json
            print('Hey, just loaded up the list.')
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

    print("gathering data... ready in 10")

# do something as each message is received 
# TODO: break all the workywork out of this function and just return the message to the main code 
# should this be a Message object?  (it's not really pervasive...)
def on_message(client, userdata, msg):
    try:
        global msgCount
        global M
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
        #samplePayload m = {"serial-number":"egg008028c05e9b0152","converted-value":25.96,"converted-units":"degC","raw-value":25.96,"raw-instant-value":25.96,"raw-units":"degC","sensor-part-number":"SHT25"}

        parsed_msg = json.loads(msg.payload)
        M.setmessage(parsed_msg)
        msgCount = msgCount + 1
        
    except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
      print "Could not convert data to an integer."
    except:
      print "Unexpected errorB:", sys.exc_info()[0]
      #raise

def main(argv):
    global board
    global msgAck
    global x
    global M
    
    
    x = MyClass()
    norman = x.f("David ")
    print(norman)
    
    
    M = MQTT_Message()
    M.setmessage([1,4,5,8])
    
    board = Arduino('/dev/ttyACM0')
    msgAck = 0 

    ##MAIN EXECUTION STARTS HERE##
    # TODO: consider this should be a "main" function or __init__ or what the heck?
    # change power flag to on
    board.digital[2].write(1)
    print("Here we go! Press CTRL+C to exit")
    # reset timers and counts
    incr = 0
    prevelapsedruntime = "00:00:00"
    timeSinceLastMessage = "00:00:00"
    lastMessageTimeStamp = "00:00:00"
    
    prevmsgCount = 0
    try:
        #start temp chamber run clock and set blvrun flag
        blvrun = 1
        startblvrun = time.time() 
        #assume room temp 25-27c
        #io for data (what needs to be saved?)
        f = open('workfile', 'w')

        client = paho.Client(client_id="2940")
        client.on_subscribe = on_subscribe

        client.username_pw_set("wickeddevice", "mXtsGZB5")
        client.connect("mqtt.opensensors.io")

        client.subscribe("/orgs/wd/aqe/temperature/egg008028c05e9b0152", qos=0)

        # message loop should be one of these (first two down't work for what we want)
        #client.loop_read()
        #client.loop_forever()
        client.loop_start()
        while blvrun: 
            client.on_message = on_message
      
            # is this message new? (if flag is 1, then its value gets added to count.  if 0, then no addition)
            #TODO: not currently working right.
      

            # advance counts and clocks
            elapsedruntime = (time.strftime("%H:%M:%S", time.gmtime(time.time() - startblvrun)))
            if msgCount == prevmsgCount:
                timeSinceLastMessage = (time.strftime("%H:%M:%S", time.gmtime(time.time() - lastMessageTimeStamp)))
            else:
                # reset timeSinceLastMessage
                lastMessageTimeStamp = time.time()
                
            # only print time string when it changes (each second)
            if elapsedruntime == prevelapsedruntime:
                pass
            else:
                print("msgs recieved: " + str(msgCount) + "   time since last msg:     " + timeSinceLastMessage + "   total run time: " + elapsedruntime)
                print('check this out ' + str(M.tempc))
            prevelapsedruntime = elapsedruntime
            prevmsgCount = msgCount
            # reset message flag

  
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        # change power flag to off
        # change arduino LED to green
        board.digital[5].write(0)
        board.digital[4].write(0)
        board.digital[2].write(0)
        client.loop_stop()
        client.unsubscribe("/orgs/wd/aqe/temperature/egg008028c05e9b0152")
        json.dump(temp_record, f)
        f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
  

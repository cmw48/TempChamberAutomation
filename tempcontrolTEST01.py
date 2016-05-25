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


class MQTT_Message:

    try:
        def __init__(self, name):
            self.values = []    # creates a new list of values for each message

        def setmessage(self, msg_json):
            self.values = msg_json
            print('Hey, just loaded up the list.')
            print(self.values)      
    
        def getmessage(self, raw_instant_temp):
            raw_instant_temp = (self.values['raw-instant-value'])    
            return raw_instant_temp
        
    except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
      print "Could not convert data to an integer."
    except:
      print "Unexpected error:", sys.exc_info()[0]
        
        
# squawk when subscribe to egg topic is successful
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

    print("gathering data... ready in 10")

# do something as each message is received 
# TODO: break all the workywork out of this function and just return the message to the main code 
# should this be a Message object?  (it's not really pervasive...)
def on_message(client, userdata, msg):
    try:
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
        #samplePayload m = {"serial-number":"egg008028c05e9b0152","converted-value":25.96,"converted-units":"degC","raw-value":25.96,"raw-instant-value":25.96,"raw-units":"degC","sensor-part-number":"SHT25"}
        parsed_msg = json.loads(msg.payload)
        M.setmessage(self, parsed_msg)
        
        
    except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
      print "Could not convert data to an integer."
    except:
      print "Unexpected error:", sys.exc_info()[0]
      #raise

def main(argv):
    global board
    global msgAck
    global msgCount
    M = MQTT_Message()
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
    msgCount = 0

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
            # only print time string when it changes (each second)
            if elapsedruntime == prevelapsedruntime:
                pass
            else:
                print("msgs recieved: " + str(msgCount) + "    total run time: " + elapsedruntime)
            prevelapsedruntime = elapsedruntime
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
  

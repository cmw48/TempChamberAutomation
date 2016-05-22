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

#declare a global list of temps
recent_temps=[]
temp_record=[]
deltas=[]


# why does this need to be here instead of in main?
global startblvrun

# squawk when subscribe to egg topic is successful
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

    print("gathering data... ready in 10")

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
        global msgAck
        msgAck = 1  
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
        #samplePayload m = {"serial-number":"egg008028c05e9b0152","converted-value":25.96,"converted-units":"degC","raw-value":25.96,"raw-instant-value":25.96,"raw-units":"degC","sensor-part-number":"SHT25"}
        parsed_msg = json.loads(msg.payload)
        raw_instant_temp = (parsed_msg['raw-instant-value'])
        temp_record.append([raw_instant_temp, time.time()])   
        recent_temps.append(raw_instant_temp)

        # review recent temps and report
        templistlen = len(recent_temps)
        if templistlen <= 10: 
          #once we are warmed up, this condition won't be met and this code will not run
          #use this spot to initialize local variables until we get threading working
          startStable = time.time()
          stopUnstable = time.time()
          stopStable = time.time() 
          startUnstable = time.time() 
          isStable = False
          print (str(11-templistlen)+"...")
          # fill up deltaslist
          deltas.append(templistlen)
        elif templistlen > 10 :
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
            else:
              isStable = True
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
    debug = False
    host = "mqtt.opensensors.io"
    client_id = 2940
    keepalive = 60
    port = 1883
    password = "mXtsGZB5"
    topic = "/orgs/wd/aqe/temperature"
    username = "wickeddevice"
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "dh:i:k:p:P:t:u:v", ["debug", "id", "keepalive", "port", "password", "topic", "username", "verbose"])
    except getopt.GetoptError as s:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-i", "--id"):
            client_id = arg
        elif opt in ("-k", "--keepalive"):
            keepalive = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-P", "--password"):
            password = arg
        elif opt in ("-t", "--topic"):
            topic = arg
            print(topic)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    if topic == None:
        print("You must provide a topic to clear.\n")
        print_usage()
        sys.exit(2)

    # does this work as a global init?  Why?
    msgAck = 1 
    
    ##MAIN EXECUTION STARTS HERE##
    # TODO: consider this should be a "main" function or __init__ or what the heck?
  
    print("Here we go! Press CTRL+C to exit")
    # reset timers and counts
    incr=0
    prevelapsedruntime = "00:00:00"
    msgCount=0
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
            #get one message (and do a buncha stuff in that function)
            client.on_message = on_message
      
            # is this message new? (if flag is 1, then its value gets added to count.  if 0, then no addition)
            #TODO: not currently working right.
            msgCount = msgCount + msgAck

            # advance counts and clocks
            elapsedruntime = (time.strftime("%H:%M:%S", time.gmtime(time.time() - startblvrun)))
            # only print time string when it changes (each second)
            if elapsedruntime == prevelapsedruntime:
              pass
            else:
              print("msgs recieved: " + str(msgCount) + "    total run time: " + elapsedruntime)
            prevelapsedruntime = elapsedruntime
            # reset message flag
            msgAck = 0
  
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        client.loop_stop()
        client.unsubscribe("/orgs/wd/aqe/temperature/egg008028c05e9b0152")
        json.dump(temp_record, f)
        f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
  

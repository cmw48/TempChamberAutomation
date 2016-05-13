import paho.mqtt.client as paho
import json
import datetime
import time
# This code is to non-invasively automate the Thermotron temp chamber
 
#TODO allow user to enter an egg serial before each run
#TODO implement raspi 

#declare a global list of temps
recent_temps=[]
temp_record=[]
deltas=[]

#does this work?  Why?
msgAck = 1 

global startblvrun


# squawk when subscribe to egg topic is successful
def on_subscribe(client, userdata, mid, granted_qos):
  print("Subscribed: "+str(mid)+" "+str(granted_qos))

  print("gathering data... ready in 10")

# do something as each message is received  
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

print("Here we go! Press CTRL+C to exit")
incr=0
prevelapsedruntime = "00:00:00"
msgCount=0
try:
    #start temp chamber run
    blvrun = 1
    startblvrun = time.time() 
    #assume room temp 25-27c
    #step 1 monitor 
    f = open('workfile', 'w')
    client = paho.Client(client_id="2940")
    client.on_subscribe = on_subscribe

    client.username_pw_set("wickeddevice", "mXtsGZB5")
    client.connect("mqtt.opensensors.io")
    # use egg0080220259180152
    client.subscribe("/orgs/wd/aqe/temperature/egg00802ad5e9880121", qos=0)
    #client.loop_read()
    #client.loop_forever()
    client.loop_start()
    #client.loop.start()

	
    while blvrun: 
      client.on_message = on_message
      msgCount = msgCount + msgAck
      elapsedruntime = (time.strftime("%H:%M:%S", time.gmtime(time.time() - startblvrun)))
      if elapsedruntime == prevelapsedruntime:
        pass
      else:
        print("msgs recieved: " + str(msgCount) + "    total run time: " + elapsedruntime)
      msgAck = 0
      prevelapsedruntime = elapsedruntime

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    client.loop_stop()
    client.unsubscribe("/orgs/wd/aqe/temperature/egg00802ad5e9880121")
    json.dump(temp_record, f)
    f.close()



  

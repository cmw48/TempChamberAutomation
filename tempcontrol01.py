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
  
# squawk when subscribe to egg topic is successful
def on_subscribe(client, userdata, mid, granted_qos):
  print("Subscribed: "+str(mid)+" "+str(granted_qos))

  print("gathering data... ready in 10")

# do something as each message is received  
def on_message(client, userdata, msg):
  #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
  #samplePayload m = {"serial-number":"egg008028c05e9b0152","converted-value":25.96,"converted-units":"degC","raw-value":25.96,"raw-instant-value":25.96,"raw-units":"degC","sensor-part-number":"SHT25"}
  parsed_msg = json.loads(msg.payload)
  raw_instant_temp = (parsed_msg['raw-instant-value'])
  temp_record.append([raw_instant_temp, time.time()])  
  recent_temps.append(raw_instant_temp)
  
  # review recent temps and report
  templistlen = len(recent_temps)
  if templistlen <= 10: 
    print (str(11-templistlen)+"...")
    # fill up deltaslist
    deltas.append(templistlen)
  elif templistlen > 10 :
    for x in range (0, 10):
      deltas[x]=(recent_temps[x] - recent_temps[x+1])
    print(deltas)
    print(sum(deltas))
    f.write(str(sum(deltas)))
    json.dump(recent_temps, f)
    recent_temps.pop(0)
    print(recent_temps)
    #print(temp_record)

 #   print sum(deltas) 
#  if abs(deltas[0]) == 0 :
#    print("not changing at all")
#  elif 0 <= abs(deltas[0]) <= 0.5:
#    print("changing less than .5...")
#  elif  abs(deltas[0]) > 0.5:
#    print("changing a lot...")
#  else:
#    print(recent_temps)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        incr=0
        #start temp chamber run
        #assume room temp 25-27c
        #step 1 monitor 
        f = open('workfile', 'w')
        client = paho.Client(client_id="2940")
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.username_pw_set("wickeddevice", "mXtsGZB5")
        client.connect("mqtt.opensensors.io")
        client.subscribe("/orgs/wd/aqe/temperature/egg0080281b299b0150", qos=0)
        #client.loop_read()
        #client.loop_forever()
        mqttc.loop()
        client.loop.start()

        incr=0
        incr=incr+1
        print("counted " + str(incr))

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    client.unsubscribe("/orgs/wd/aqe/temperature/egg0080281b299b0150")
    json.dump(temp_record, f)
    f.close()



  

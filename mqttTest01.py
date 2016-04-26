import paho.mqtt.client as mqtt
import os, urlparse

# Define event callbacks
def on_connect(mqtt, obj, rc):
    print("rc: " + str(rc))

    def on_message(mqtt, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

	def on_publish(mqtt, obj, mid):
	    print("mid: " + str(mid))

	    def on_subscribe(mqtt, obj, mid, granted_qos):
	        print("Subscribed: " + str(mid) + " " + str(granted_qos))

		def on_log(mqtt, obj, level, string):
		    print(string)

		    #mqttc = mosquitto.Mosquitto()
		    mqttc = mqtt.Client()
		    # Assign event callbacks
		    mqttc.on_message = on_message
		    mqttc.on_connect = on_connect
		    mqttc.on_publish = on_publish
		    mqttc.on_subscribe = on_subscribe

		    # Uncomment to enable debug messages
		    mqttc.on_log = on_log

		    # Parse CLOUDMQTT_URL (or fallback to localhost)
		    url_str = os.environ.get('MQTT_URL', 'mqtt://localhost:1883')
		    url = urlparse.urlparse(url_str)

		    # Connect
		    mqttc.username_pw_set("wickeddevice", "mXtsGZB5")
		    mqttc.connect(url.hostname, url.port)

		    # Start subscribe, with QoS level 0
		    mqttc.subscribe("/orgs/wd/aqe/temperature/egg008022605f180151", 0)

		    # Publish a message
		    # mqttc.publish("hello/world", "my message")

		    # Continue the network loop, exit when an error occurs
		    rc = 0
		    while rc == 0:
		        rc = mqttc.loop()
			print("rc: " + str(rc))

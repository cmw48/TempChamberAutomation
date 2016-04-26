import os

url_str = os.environ.get('MQTT_URL', 'mqtt://localhost:1883')
print(url_str);

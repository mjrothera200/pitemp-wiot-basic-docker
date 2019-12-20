import paho.mqtt.client as paho
import json
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import ssl




# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 17
instance = dht11.DHT11(pin=17)

# device credentials
ca_absolute_path = '/app/messaging.pem'
iotidentifier = 'pi1'
iotorg = 'cg3orm'
iottype = 'pitemp'

device_id        = 'use-token-auth'      # * set your device id (will be the MQTT client username)
device_secret = '12345678'
random_client_id = 'd:'+iotorg+':'+iottype+':'+iotidentifier      # * set a random client_id (max 23 char)


# extract the serial number
cpuserial = "0000000000000000"
try:
    f=open('/proc/cpuinfo', 'r')
    for line in f:
        if line[0:6]=='Serial':
            cpuserial = line[10:26]
    f.close()
except:
    cpuserial="ERROR000000000"

print("CPU Serial # is %s" % (cpuserial))


# device topics
out_topic_environmentals = 'iot-2/evt/environmentals/fmt/json'  # publishing messages


# --------------- #
# Callback events #
# --------------- #

# connection event
def on_connect(client, data, flags, rc):
    print('Connected, rc: ' + str(rc))

# connection event

def on_disconnect(client, data, rc):
    print('Disonnected, rc: ' + str(rc))

# subscription event
def on_subscribe(client, userdata, mid, gqos):
    print('Subscribed: ' + str(mid))

# received message event
def on_message(client, obj, msg):
    print(msg.topic)
# ------------- #
# MQTT settings #
# ------------- #

# create the MQTT client
client = paho.Client(client_id=random_client_id, protocol=paho.MQTTv311)  # * set a random string (max 23 chars)

# assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe


# client connection
client.username_pw_set(device_id, device_secret)  # MQTT server credentials
client.tls_set(ca_certs=ca_absolute_path, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

try:
    client.connect(iotorg+".messaging.internetofthings.ibmcloud.com", port=8883)                   # MQTT server address
    client.subscribe(in_topic_snapshot, 0)                     # MQTT subscribtion (with QoS level 0)
except:
    print('could not connect')
    

client.loop_start()

while True:
    time.sleep(6)
    result = instance.read()
    if result.is_valid():
    	temp_c = result.temperature 
    	temp_f = (result.temperature * 9)/5 + 32 
    	humidity = result.humidity 
    	message = { 'd': {'temp_c': temp_c, 'temp_f': temp_f, 'humidity': humidity } }     
    	client.publish(out_topic_environmentals, json.dumps(message))




import paho.mqtt.client as mqtt
import zlib
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("zipped")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(str(sys.getsizeof(msg.payload)) + " Bytes, Esta mensagem tem " + str(len(msg.payload)) +" Caracteres")
    try:
        decompressed_data = zlib.decompress(msg.payload, 16 + zlib.MAX_WBITS)
        print " Decompressing"
        print " Esta Mensagem tem " + str(sys.getsizeof(decompressed_data)) + " Bytes"
        print " Esta Mensagem tem no total " + str(len(decompressed_data)) + " Caracteres"
    except:
        print "NotEncoded"

client = mqtt.Client(client_id="SensorID", clean_session=False, userdata=None, protocol="MQTTv311")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("sub","123456")
client.connect("www.semantixsense.com.br", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
import paho.mqtt.publish as publish
# from datetime import datetime
import time
import os
import sys
import paho.mqtt.client as mqtt
import logging
import gzip
import shutil




# with open('/home/felipe/dcup.csv', 'rb') as f_in, gzip.open('file.txt.gz', 'wb') as f_out:
#     shutil.copyfileobj(f_in, f_out)
# with open('file.txt.gz', 'rb') as f:
#     x = f.read()
#     print sys.getsizeof(x)

#
# with gzip.open('file.txt.gz', 'rb') as f:
#     content = f.read()
#     print len(bytearray(content))
# print "ReadingFile"
# file = ("/home/felipe/Desktop/cassandraoutput.csv.zip", "r")
# file = bytearray([elem.encode("hex") for elem in file.read()])
# print "File Read"
client = mqtt.Client(client_id="SensorGabrielID", clean_session=False, userdata=None, protocol="MQTTv311")
client.max_inflight_messages_set(999)
client.username_pw_set("pub", password="123456")
client.connect("34.196.59.158", 1883, 60)
for x in range(0,50000):
    # print "Tentando enviar"
    print client.publish("serial", payload="8416f9ac4a0615428107988389027f3f78N -- "+str(x), qos=1, retain=False)
    client.loop()
    # time.sleep(1)
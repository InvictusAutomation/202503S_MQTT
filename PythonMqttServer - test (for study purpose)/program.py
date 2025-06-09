import paho.mqtt.client as mqtt
import json
import time
import MQTTClientHandel
import json
#===================================================================[Change 1]=================
# client = mqtt.Client("ADADWWRWFGWERWRWFGTERTER-PUB")
client = mqtt.Client(
    client_id="ADADWWRWFGWERWRWFGTERTER-PUB",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION1 #assign this version
)
# client.username_pw_set("test001", password="test001")
client.username_pw_set("admin", password="admin")
# mqttPrefix = "a/b/c"
mqttPrefix = "groundup"

serverip = "13.76.182.87"
port = 1883
#==============================================================================================

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))  
    print(client.is_connected())
    client.subscribe(mqttPrefix+"/Online/#")

def on_message(client, userdata, msg):
    topicstrs = msg.topic.replace(mqttPrefix, "Doton").split('/')
    res = MQTTClientHandel.handel(msg.topic, topicstrs[3], msg.payload)
    if (res.isReplay):
        client.publish(res.tpoic, qos=0, payload=res.payload)
    print(msg.topic+" " + json.dumps(res.__dict__))

client.on_connect = on_connect  # Callback for the broker's response when connecting to the broker
client.on_message = on_message  # Callback when receiving a subscription message

#===================================================================[Change 2]=================
# result = client.connect("192.168.0.102", 1883, 190)  # Connect to the broker
result = client.connect(serverip, port, 190)  # Connect to the broker
#==============================================================================================

client.loop_start()
while (True):
    time.sleep(1)

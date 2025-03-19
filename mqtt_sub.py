# subscriber.py
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

#1 assign a broker
# mqtt_broker='mqtt.eclipseprojects.io'   
mqtt_broker = "localhost"
port = 1883
topic = "home/sensor/#"  #subscribe to all sub-topic
QoS = 1


#2 connect function for client
class SubInfo:
    def __init__(self, client_id):
        self.client_id = client_id
        self.message_count = 0

client_id = "subscriber_001"
user_data = SubInfo(
    client_id=client_id,
)

def on_connect(client, userdata, flags, rc):
    # get some info from the device
    if rc == 0:
        client.subscribe(topic, qos=QoS)
        print(f"✅ Device: {userdata.client_id} is connected.")
    else:
        print(f"❌ Connection failed, status: {rc}")


#3 message function for client
def on_message(client, userdata, msg):
    userdata.message_count += 1
    print(f"📊 Total message count: {userdata.message_count}")
    try:
        # print(f"📥 Received message: Topic={msg.topic}, QoS={msg.qos}, body={msg.payload.decode()}")
        print(f"📥 Received message: Topic={msg.topic}, QoS={msg.qos}")
        print(f"body={msg.payload.decode()}")

    except UnicodeDecodeError:
        print(f"⚠️ Fail to decode, binary content:{msg.payload}")

#4 initiate a client instance
client = mqtt.Client(client_id=user_data.client_id,userdata=user_data)
client.on_connect = on_connect
client.on_message = on_message

#5 subscribe!
try:
    # client.tls_set(ca_certs="ca.crt")
    client.connect(mqtt_broker, port, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("🛑 Terminated by keyboard")
except Exception as e:
    print(f"❌ Error: {str(e)}")
finally:
    client.disconnect()
    print(f"📨 Messages received: {user_data.message_count}")
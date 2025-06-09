# Download ：https://mosquitto.org/download/
# net start mosquitto
# pip install paho-mqtt python-dotenv

# import paho.mqtt.client as mqtt
# from random import randrange, uniform
# import time

# #1 assign a broker
# # mqtt_broker='mqtt.eclipseprojects.io'   
# mqtt_broker = "localhost"
# port = 1883
# topic = "groundup/#"
# QoS = 1
# LWT_topic = "groundup/status"


# #2 connect function for client

# #header
# user_data = DeviceInfo(
#     device_id="temperature_sensor_001", #outside sensor
#     location="outside"
# )

# def on_connect(client, userdata, flags, rc):
#     # get some info from the device
#     if rc == 0:
#         print(f"✅ Connected.")
#     else:
#         print(f"❌ Connection failed, status: {rc}")


# #3 initiate a client instance. A client can stay on multiple topics
# client=mqtt.Client() 
# client.on_connect = on_connect


# #4 publish count
# def on_publish(client, userdata, mid):
#     # count messages
#     userdata.message_count += 1
#     print(f"📊 Total message count: {userdata.message_count}")

# client.on_publish = on_publish


# #5 connect with broker
# try:
#     client.loop_start()
#     #set the connect after the loop, so that subscriber can see the test message
#     client.connect(mqtt_broker, port, 60)

#     while True:
#         temperature = uniform(6,13.5)
#         payload = f'{{"value": {temperature:.2f}, "unit": "°C"}}'
        
#         #publish
#         info = client.publish(topic, payload, qos=QoS, retain=True)
#         info.wait_for_publish()  #ensure the message is sent
#         print("📤 Published")
#         time.sleep(5)
# except KeyboardInterrupt:
#     print("🛑 Terminated by keyboard")
# except Exception as e:
#     print(f"❌ Error: {str(e)}")
# finally:
#     client.loop_stop()
#     client.disconnect()
#     # last status
#     print("See you!")




#==============================================================================================
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

#1 assign a broker
# mqtt_broker='mqtt.eclipseprojects.io'   
# mqtt_broker = "localhost"
mqtt_broker = "192.168.1.6" #this depends on your laptop's wirelessLAN ipv4
port = 1883
topic = "home/sensor/temperature"
QoS = 1
LWT_topic = "home/status"


#2 connect function for client
class DeviceInfo:
    def __init__(self, device_id, location):
        self.device_id = device_id
        self.location = location
        self.message_count = 0

#header
user_data = DeviceInfo(
    device_id="temperature_sensor_002",
    location="living_room"
)

def on_connect(client, userdata, flags, rc):
    # get some info from the device
    if rc == 0:
        print(f"✅ Device: {userdata.device_id} is connected.")
        print(f"✅ Location: {userdata.location}")
        client.publish(topic, "First Test Message: Hello! begin to send temperature data.", qos=QoS,retain=True)
    else:
        print(f"❌ Connection failed, status: {rc}")

'''
rc=0: Connection successful 157
rc=1: Protocol version not supported
rc=2: Client identifier invalid
rc=3: Broker unavailable (e.g., network issues)
rc=4: Username or password incorrect
rc=5: Unauthorized access 69
'''

#3 initiate a client instance. A client can stay on multiple topics
client=mqtt.Client(client_id=user_data.device_id,userdata=user_data) 
client.will_set(LWT_topic, f"{user_data.device_id} offline", qos=QoS, retain=True) #lastwill should be set before the loop
client.on_connect = on_connect



#4 publish count
def on_publish(client, userdata, mid):
    # count messages
    userdata.message_count += 1
    print(f"📊 Total message count: {userdata.message_count}")

client.on_publish = on_publish


#5 connect with broker
try:
    client.loop_start()
    #set the connect after the loop, so that subscriber can see the test message
    client.connect(mqtt_broker, port, 60) 
    
    while True:
        temperature = uniform(20,23.5)
        payload = f'{{"value": {temperature:.2f}, "unit": "°C"}}'
        
        #publish
        info = client.publish(topic, payload, qos=QoS, retain=True)
        info.wait_for_publish()  #ensure the message is sent
        print(f"📤 Published: {payload} (Message ID: {info.mid})")
        time.sleep(5)
except KeyboardInterrupt:
    print("🛑 Terminated by keyboard")
except Exception as e:
    print(f"❌ Error: {str(e)}")
finally:
    client.loop_stop()
    client.disconnect()
    # last status
    print(f"\n📝 Last Status--Device: {user_data.device_id}")
    print(f"📍 Location: {user_data.location}")
    print(f"📨 Messages sent: {user_data.message_count}")



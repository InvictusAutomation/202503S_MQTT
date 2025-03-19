import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

#1 assign a broker
# mqtt_broker='mqtt.eclipseprojects.io'   
mqtt_broker = "localhost"
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


## If want to use tls, you have to set the port as 8883
## client.tls_set() #SSL encoding
## client.username_pw_set("admin", "admin123")  #has to map with subscriber

### Explicitly Specify CLIENT_ID
'''
The client will connect to the MQTT server using a fixed CLIENT_ID. 
If two clients connect using the same ID, the server will disconnect the old connection, 
and the new connection will replace the old one. 
This is suitable for scenarios that require persistent sessions or fixed identification 
(such as production environments).
'''
### Not specifying client_id (automatically generated)
'''
The library will automatically generate a random ID (formatted as paho-XXXXXX). 
The ID will be different each time the client runs, 
making it suitable for testing or temporary connections.
'''

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


#loop_start
'''
"After calling loop_start(), 
the library will start an independent thread in the background 
(implemented via threading.Thread), 
which will automatically invoke loop_forever(). 
This thread is responsible for continuously performing the following operations:

- Maintaining the TCP connection with the Broker
- Handling the sending and receiving of messages (including QoS 1/2 acknowledgments)
- Automatically reconnecting 
  (attempting to reconnect with an exponential backoff strategy 
  when a network interruption is detected)
- Non-blocking features: The main thread will not be blocked, 
  allowing other tasks (such as GUI updates, sensor data collection) 
  to execute simultaneously. For example, in IoT devices, 
  the main thread can continuously read sensor data and send it via publish(), 
  while network communication is handled by the background thread."
'''

#loop_stop
'''"Thread Termination
Calling loop_stop() will set the internal flag _thread_terminate=True, 
signaling the background thread to terminate the execution of loop_forever().

Thread Resource Release: 
- After termination, the thread object is removed from client._thread (set to None) 
  to avoid memory leaks.
- Network Loop Stopping: Stops all processing of network packets, 
                         including heartbeat packet sending and message retransmission.
- Considerations for Active Disconnection:
  If disconnect() is actively called, the network loop will also stop. 
  However, if reconnection is needed, 
  reconnect() must be explicitly called and loop_start() must be restarted.
'''
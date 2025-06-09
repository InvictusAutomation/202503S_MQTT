const mqtt = require("mqtt");
require("./protocol")
var _ = require('c-struct');

// =====================================================[Change 1]=======================================
// MQTT Broker URL
const url = "mqtt://13.76.182.87:1883";
const application_name = "vib";
const options = {
  connectTimeout: 4000,
  clientId: "clientId",
  username: "admin", // change to your mqtt username
  password: "admin", // change to your mqtt password
};
// =======================================================================================================

// Create a client instance
const client = mqtt.connect(url, options);

// Publish a message when the client connects.
client.on("connect", function () {
  console.log("Connected to MQTT Broker!");

  // Subscribe to the topic
  // ====================================================[Change 2]=======================================

  client.subscribe(`Doton111/rak/${application_name}/device/+/rx`);
  console.log(`subcribe to: Doton111/rak/${application_name}/device/+/rx`)
  // =====================================================================================================

});  
console.log("dataTime:",new Date());





// The callback function when the client receives a message from the server
client.on("message", function (topic, message) {
  // Process the received messages
  console.log("Received Message:", topic, message.toString());
  // ====================================================[Change 3]=======================================
  const topicParts = topic.split('/');
  const deviceIndex = topicParts.indexOf('device');
  if (deviceIndex === -1 || deviceIndex + 1 >= topicParts.length) {
    console.error("Invalid topic format, cannot extract device_EUI:", topic);
    return;
  }
  const device_EUI = topicParts[deviceIndex + 1];
  console.log("Extracted device_EUI:", device_EUI);
  // =====================================================================================================
  try {
    var pyload = JSON.parse(message.toString());
    var data = pyload.data;
    const buffer = Buffer.from(data, 'base64');
    
    if (buffer[0] != 0x05) return;
    
    console.log("dataTime:", new Date());
    var dataRevice = _.unpackSync("dataRevice", new Uint8Array(buffer));
    console.log("Temperature", dataRevice.temp);
    console.log("Voltage", dataRevice.batteryV / 1000);
    console.log("X_ACC_RMS", dataRevice.XAccRms / 100);
    console.log("X_velocity_RMS", dataRevice.XVelRms / 100);
    console.log("Y_ACC_RMS", dataRevice.YAccRms / 100);
    console.log("Y_velocity_RMS", dataRevice.YVelRms / 100);
    console.log("Z_ACC_RMS", dataRevice.ZAccRms / 100);
    console.log("Z_velocity_RMS", dataRevice.ZvelRms / 100);
    console.log("id", dataRevice.id);
    
    //if you should change params you should execute the next code
    // ====================================================[Change 4]=======================================
    var dataSend = {
    //  cmd:0x05,
      id : dataRevice.id+1,
      fre:0,
      len:0,
      interval:1//upload interval change to 1 min
    }
    // =====================================================================================================
  
    var sendBuffer = _.packSync("dataSend", dataSend);
    const base64String = sendBuffer.toString('base64');
    pyload.data = base64String;

   // ======================================================[Change 5]=======================================
    client.publish(`testbyrock/Doton111/rak/${application_name}/device/${device_EUI}/tx`,JSON.stringify(pyload));
    console.log(`publish in : testbyrock/Doton111/rak/${application_name}/device/${device_EUI}/tx`);
  } catch (error) {
    console.error("Error processing message:", error);
  }
   // ======================================================================================================
});





// Callback function when the connection between the client and the server is interrupted
client.on("offline", function () {
  console.log("MQTT Client Offline");
});

// Callback function when the client closes
client.on("close", function () {
  console.log("MQTT Client Closed");
});

// Callback function when a client connection error occurs
client.on("error", function (err) {
  console.log("MQTT Client Error:", err.message);
});

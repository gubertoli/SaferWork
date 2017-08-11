//SaferWork - Device Code
//
// References:
//     https://github.com/adafruit/DHT-sensor-library
//     https://quadmeup.com/hc-12-433mhz-wireless-serial-communication-module-configuration/
//     https://www.elecrow.com/download/HC-12.pdf
//     https://playground.arduino.cc/Main/MQGasSensors
//     https://github.com/bblanchon/ArduinoJson
//

#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <DHT.h>

#define DHTPIN A1     // Analog PIN A1 for DHT11
#define DHTTYPE DHT11 // DHT 11

//Device Configuration
#define DEVID  "Device01"
#define MSG_PUSH_TIME 5000 //in miliseconds

DHT dht(DHTPIN, DHTTYPE);

//Pins for Serial connection to HC-12
SoftwareSerial HC12_Device(10, 11); // RX, TX
int HC12_SET = 7; // Pin to setup HC-12 Wireless module

// GAS Sensors Pinout no Arduino
int MQ2_gasPin = 5;    //sensitive for flamable and combustible gasses (Methane, Butane, LPG, smoke)
int MQ9_gasPin = 4;    //sensitive for Carbon Monoxide, flammable gasses
int MQ135_gasPin = 3;  //For Air Quality (sensitive for Benzene, Alcohol, smoke)

void setup(){
  pinMode(HC12_SET, OUTPUT);
  HC12_Device.begin(9600);
  Serial.begin(9600);

  digitalWrite(7, LOW);            // enter AT command mode
  HC12_Device.print("AT+DEFAULT"); // 9600, CH1, FU3, (F) to bypass flash memory
  delay(100);
  digitalWrite(7, HIGH);           // enter transparent mode
  
  dht.begin();
}

void loop(){
  // Reserve memory space
  StaticJsonBuffer<256> jsonBuffer;

  char buffer[256];
  JsonObject& root = jsonBuffer.createObject();


  delay(MSG_PUSH_TIME);
  
  //Sensors Readings
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int MQ2 = analogRead(MQ2_gasPin);
  int MQ9 = analogRead(MQ9_gasPin); 
  int MQ135 = analogRead(MQ135_gasPin); 
  
  // JSON Construct
  // Example: {"DeviceID":"Device01","key":0x00,"data":[TEMPERATURE,HUMIDITY,MQ2_LEVEL,MQ9_LEVEL,MQ135_LEVEL]}
  
  root["DeviceID"] = DEVID;
  root["key"] = "0x00";
  
  JsonArray& data = root.createNestedArray("data");
  data.add(h);
  data.add(t);
  data.add(MQ2);
  data.add(MQ9);
  data.add(MQ135);
  
  root.printTo(buffer, sizeof(buffer));
  HC12_Device.println(buffer);

}

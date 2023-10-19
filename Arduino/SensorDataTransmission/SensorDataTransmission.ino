#include <Arduino_LSM6DS3.h>
#include <ArduinoBLE.h>

BLEService sensorService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLECharacteristic sensorDataCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLENotify, 40); // 40 bytes for 10 floats

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  if (!BLE.begin()) {
    Serial.println("Failed to initialize BLE!");
    while (1);
  }

  BLE.setLocalName("SensorData");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(sensorDataCharacteristic);
  BLE.addService(sensorService);
  BLE.advertise();

  Serial.print("Arduino BLE Address: ");
  Serial.println(BLE.address());

  Serial.println("Waiting for connections...");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      float sensorData[20]; // 10 for gyro, 10 for accel
      uint8_t buffer[120]; // Buffer to hold 20 floats (120 bytes)

      // Collect 10 readings of gyroscope
      for (int i = 0; i < 10; ++i) {
        if (IMU.gyroscopeAvailable()) {
          IMU.readGyroscope(sensorData[i * 2], sensorData[i * 2 + 1], sensorData[i * 2 + 2]);
        }
        delay(100); 
      }

      // Collect 10 readings of accelerometer
      for (int i = 0; i < 10; ++i) {
        if (IMU.accelerationAvailable()) {
          IMU.readAcceleration(sensorData[i * 2 + 10], sensorData[i * 2 + 11], sensorData[i * 2 + 12]);
        }
        delay(100); 
      }

      // Pack sensor data into the buffer
      memcpy(buffer, sensorData, sizeof(buffer));

      // Send the sensor data buffer
      sensorDataCharacteristic.writeValue(buffer, sizeof(buffer));
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}
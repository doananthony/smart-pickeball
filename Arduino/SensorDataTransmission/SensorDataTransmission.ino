#include <Arduino_LSM6DS3.h>
#include <ArduinoBLE.h>

BLEService sensorService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLECharacteristic sensorDataCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLENotify, 24); // 24 bytes for 6 floats

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
      float gyroX, gyroY, gyroZ, accelX, accelY, accelZ;

      if (IMU.gyroscopeAvailable() && IMU.accelerationAvailable()) {
        IMU.readGyroscope(gyroX, gyroY, gyroZ);
        IMU.readAcceleration(accelX, accelY, accelZ);

        // Pack sensor data into the buffer
        uint8_t buffer[24];
        memcpy(buffer, &gyroX, sizeof(gyroX));
        memcpy(buffer + sizeof(gyroX), &gyroY, sizeof(gyroY));
        memcpy(buffer + sizeof(gyroX) + sizeof(gyroY), &gyroZ, sizeof(gyroZ));
        memcpy(buffer + sizeof(gyroX) + sizeof(gyroY) + sizeof(gyroZ), &accelX, sizeof(accelX));
        memcpy(buffer + sizeof(gyroX) + sizeof(gyroY) + sizeof(gyroZ) + sizeof(accelX), &accelY, sizeof(accelY));
        memcpy(buffer + sizeof(gyroX) + sizeof(gyroY) + sizeof(gyroZ) + sizeof(accelX) + sizeof(accelY), &accelZ, sizeof(accelZ));

        // Send the sensor data buffer
        sensorDataCharacteristic.writeValue(buffer, sizeof(buffer));

      }

      delay(1000); // Adjust the delay time as needed
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

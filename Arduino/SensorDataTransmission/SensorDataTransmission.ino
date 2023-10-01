#include <Arduino_LSM6DS3.h>
#include <ArduinoBLE.h>

// Set up UUID to connect via Bluetooth Low Energy
BLEService sensorService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLEFloatCharacteristic gyroCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify);
BLEFloatCharacteristic accelCharacteristic("19B10002-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Start BLE
  if (!BLE.begin()) {
    Serial.println("Failed to initialize BLE!");
    while (1);
  }

  BLE.setLocalName("SensorData");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(gyroCharacteristic);
  sensorService.addCharacteristic(accelCharacteristic);
  BLE.addService(sensorService);
  BLE.advertise();

  // Print the Bluetooth MAC address
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

        // Update BLE characteristics
        gyroCharacteristic.writeValue(gyroX);
        gyroCharacteristic.writeValue(gyroY);
        gyroCharacteristic.writeValue(gyroZ);
        accelCharacteristic.writeValue(accelX);
        accelCharacteristic.writeValue(accelY);
        accelCharacteristic.writeValue(accelZ);

        // Print data to Serial Monitor
        Serial.print("Gyro: ");
        Serial.print(gyroX);
        Serial.print('\t');
        Serial.print(gyroY);
        Serial.print('\t');
        Serial.print(gyroZ);
        Serial.print("\tAccel: ");
        Serial.print(accelX);
        Serial.print('\t');
        Serial.print(accelY);
        Serial.print('\t');
        Serial.println(accelZ);
      }

      delay(1000); // Adjust the delay time as needed
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

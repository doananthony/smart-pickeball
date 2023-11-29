# smart-pickeball
IoT Project for a smart pickle ball paddle that contains the Arduino code to stream Gyroscope and Accelerometer sensor data from the Arduino Nano 33 IoT and the Python client to receive the data and plot it. 

## Repository
- **`Arduino`**:  
  - `Examples`
    - `SimpleAccelometer`
      - SimpleAccelerometer.ino
    - `SimpleGryoscope`
      - SimpleGyroscope.ino
  - `SensorDataTransmission`
    - SensorDataTransmission.ino
- **`Python`**: 
  - BluetoothDataReceiver.py
  - BluetoothDeviceDiscovery.py


##  'Arduino' Folder
The folder contains two example code files to understand how the Accelerometer and Gyroscope sensors works with respect to the LSM6DS3 libary. It then contains the SensorDataTransmission code that is used to send both Accelerometer and Gyroscope data as an array of 6 values to the client using Bluetooth Low Energy.

### Running
Plug in the Arduino Nano 33 IoT device and start up the Arduino IDE. Compile and run this code to start the connection for the device.

## 'Python' Folder
The folder contains the BluetoothDeviceDiscover.py code that is used to discover bluetooth address of surrounding bluetooth devices. This address of the client device is used in the BluetoothDataReceiver.py code to establish the connection with the Arduino code to receive the sensor data from the Arduino Nano 33 IoT device and plot a visual to display the data for the orientation and behavior of the paddle.

### Setup
- Navigate into the `Python` folder
- Install Requirements: `pip install -r requirements.txt`

### Running
- BluetoothDeviceDiscovery.py:  `python3 BluetoothDeviceDiscovery`
- BluetoothDataReceiver.py:  `python3 BluetoothDataReceiver.py`


## Contributors
|        Member          |          email         |           Role         |
| ---------------------- | ---------------------- | ---------------------- |
|      Anthony Doan      |        atdoan2@illinois.edu        |        Maintainer       |

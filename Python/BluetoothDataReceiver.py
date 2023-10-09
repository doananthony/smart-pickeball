import asyncio
import struct
from bleak import BleakClient

# Gyroscope Characteristic UUID
GYRO_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
# Accelerometer Characteristic UUID
ACCEL_CHARACTERISTIC_UUID = "19B10002-E8F2-537E-4F6C-D104768A1214"

async def connect_and_read_ble_data(device_address):
    while True:
        async with BleakClient(device_address) as client:
            # Read gyroscope data
            gyro_data_bytes = await client.read_gatt_char(GYRO_CHARACTERISTIC_UUID)
            gyro_data = struct.unpack('f', gyro_data_bytes)[0]
            print("Gyroscope Data:", gyro_data)

            # Read accelerometer data
            accel_data_bytes = await client.read_gatt_char(ACCEL_CHARACTERISTIC_UUID)
            accel_data = struct.unpack('f', accel_data_bytes)[0]
            print("Accelerometer Data:", accel_data)

            await asyncio.sleep(0.1)  # Sleep for 100ms (adjust as needed)

# Replace 'device_address' with the address of your Arduino BLE device
device_address = ""  # Replace with the actual device address - look at BluetoothDeviceDiscover.py to get addresses if needed

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_read_ble_data(device_address))

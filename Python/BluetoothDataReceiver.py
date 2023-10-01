import asyncio
from bleak import BleakClient

# Gyroscope Characteristic UUID
GYRO_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Accelerometer Characteristic UUID
ACCEL_CHARACTERISTIC_UUID = "19B10002-E8F2-537E-4F6C-D104768A1214"

async def connect_and_read_ble_data(device_address):
    async with BleakClient(device_address) as client:
        # Read gyroscope data
        gyro_data = await client.read_gatt_char(GYRO_CHARACTERISTIC_UUID)
        print("Gyroscope Data:", gyro_data.decode())

        # Read accelerometer data
        accel_data = await client.read_gatt_char(ACCEL_CHARACTERISTIC_UUID)
        print("Accelerometer Data:", accel_data.decode())

# Replace 'device_address' with the address of your Arduino BLE device
device_address = "XX:XX:XX:XX:XX:XX"  # Replace with the actual device address

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_read_ble_data(device_address))

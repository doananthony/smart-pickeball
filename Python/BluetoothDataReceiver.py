import asyncio
import struct
from bleak import BleakClient

# Define the Arduino BLE device address (replace with your device's address)
arduino_ble_address = "1D016F86-06D3-D42A-DF14-9F5D7DD4F912"
sensor_data_characteristic_uuid = "19B10001-E8F2-537E-4F6C-D104768A1214"

def handle_sensor_data(sender,data):
    # Unpack the received data as an array of floats (10 floats, 40 bytes)
    sensor_data = struct.unpack('10f', data)
    print(sensor_data)
    # for i in range(0, len(sensor_data)):
    #     print(i)
    #     gyro_x = sensor_data[i]
    #     gyro_y = sensor_data[i+1]
    #     gyro_z = sensor_data[i+2] 
    #     accel_x = sensor_data[i+3]
    #     accel_y = sensor_data[i+4]
    #     # accel_z = sensor_data[i+5]
    #     print(f"Gyro: X={gyro_x}, Y={gyro_y}, Z={gyro_z}, Accel: X={accel_x}, Y={accel_y}")

async def connect_ble_device(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        # Enable notifications for the sensor data characteristic
        await client.start_notify(sensor_data_characteristic_uuid, handle_sensor_data)

        print("Waiting for sensor data...")

        # Keep the script running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_ble_device(arduino_ble_address))
    loop.run_forever()

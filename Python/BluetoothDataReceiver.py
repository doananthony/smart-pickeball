import asyncio
import struct
import matplotlib.pyplot as plt
from bleak import BleakClient

# Accelerometer and Gyroscope Characteristic UUID
SENSOR_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Lists to store data for plotting
gyro_data = [[], [], []]
accel_data = [[], [], []]

def handle_sensor_data(sender, data):
    # Unpack the received data as an array of floats (6 floats, 24 bytes)
    sensor_data = struct.unpack('6f', data)

    # Split the data into x, y, z components for gyro and accel
    gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = sensor_data

    # Append data to lists
    gyro_data[0].append(gyro_x)
    gyro_data[1].append(gyro_y)
    gyro_data[2].append(gyro_z)

    accel_data[0].append(accel_x)
    accel_data[1].append(accel_y)
    accel_data[2].append(accel_z)

    # Update the plot for Gyroscope and Accelerometer
    plt.clf()
    plt.subplot(2, 1, 1)
    plt.plot(gyro_data[0], label='X')
    plt.plot(gyro_data[1], label='Y')
    plt.plot(gyro_data[2], label='Z')
    plt.title('Gyroscope Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Rate (rad/s)')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(accel_data[0], label='X')
    plt.plot(accel_data[1], label='Y')
    plt.plot(accel_data[2], label='Z')
    plt.title('Accelerometer Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.pause(0.1)

async def connect_and_read_ble_data(device_address):
    async with BleakClient(device_address) as client:
        print(f"Connected: {client.is_connected}")

        # Enable notifications for the sensor characteristic
        await client.start_notify(SENSOR_CHARACTERISTIC_UUID, handle_sensor_data)

        print("Waiting for sensor data...")

        # Keep the script running
        while True:
            await asyncio.sleep(1)

# Replace 'device_address' with the address of your Arduino BLE device
device_address = "1D016F86-06D3-D42A-DF14-9F5D7DD4F912"  # Replace with the actual device address

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_read_ble_data(device_address))
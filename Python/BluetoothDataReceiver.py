import asyncio
import struct
import matplotlib.pyplot as plt
import numpy as np
import time
from bleak import BleakClient

# Accelerometer and Gyroscope Characteristic UUID
SENSOR_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Lists to store data for plotting
gyro_data = [[], [], []]
accel_data = [[], [], []]

# Add thresholds for gyroscope
plus_threshold = 30
minus_threshold = -30

# Map function to help replicate the degrees sent
def map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

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
    
    # Check for tilting in the x and y direction
    if accel_x > 0.1:
        degrees_x = 100 * accel_x
        degrees_x_mapped = map(degrees_x, 0, 97, 0, 90)
        tilt_info_x = f"Tilting down {degrees_x_mapped} degrees"
    elif accel_x < -0.1:
        degrees_x = 100 * accel_x
        degrees_x_mapped = map(degrees_x, 0, -100, 0, 90)
        tilt_info_x = f"Tilting up {degrees_x_mapped} degrees"
    else:
        tilt_info_x = ""
    if accel_y > 0.1:
        degrees_y = 100 * accel_y
        degrees_y_mapped = map(degrees_y, 0, 97, 0, 90)
        tilt_info_y = f"Tilting left {degrees_y_mapped} degrees"
    elif accel_y < -0.1:
        degrees_y = 100 * accel_y
        degrees_y_mapped = map(degrees_y, 0, -100, 0, 90)
        tilt_info_y = f"Tilting right {degrees_y_mapped} degrees"
    else:
        tilt_info_y = ""
        
    # Check for swing direction using gyroscope data
    if gyro_y > plus_threshold:
        print("Swing front")
        time.sleep(0.5)

    if gyro_y < minus_threshold:
        print("Swing back")
        time.sleep(0.5)

    if gyro_x < minus_threshold:
        print("Swing right")
        time.sleep(0.5)

    if gyro_x > plus_threshold:
        print("Swing left")
        time.sleep(0.5)

    # Update the plots for Gyroscope and Accelerometer
    plt.clf()
    
    # Subplot 1: Gyroscope Data
    plt.subplot(2, 1, 1)
    plt.plot(gyro_data[0], label='X')
    plt.plot(gyro_data[1], label='Y')
    plt.plot(gyro_data[2], label='Z')
    plt.title('Gyroscope Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Rate (rad/s)')
    plt.legend()

    # Subplot 2: Accelerometer Data
    plt.subplot(2, 1, 2)
    plt.plot(accel_data[0], label='X')
    plt.plot(accel_data[1], label='Y')
    plt.plot(accel_data[2], label='Z')
    
    # Annotate the plot with tilt information
    plt.annotate(tilt_info_x, xy=(0.5, 0.9), xycoords='axes fraction', ha='center', va='center', color='red')
    plt.annotate(tilt_info_y, xy=(0.5, 0.8), xycoords='axes fraction', ha='center', va='center', color='blue')
    
    plt.title('Accelerometer Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()

    plt.tight_layout()
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

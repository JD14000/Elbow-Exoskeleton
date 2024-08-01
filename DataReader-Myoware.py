import serial
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import signal
import sys
import os

# Configure the serial port and baud rate (adjust as needed)
serial_port = 'COM3'  # Replace with your Arduino serial port
baud_rate = 9600

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate)

# Initialize lists to store all data
timestamps = []
intensity_values = []

# Function to read data from serial port and update the plot
def update(frame):
    global timestamps, intensity_values

    # Read multiple lines from the serial port
    lines = []
    while ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        lines.append(line)

    for line in lines:
        try:
            intensity = int(line)
            timestamp = datetime.datetime.now()
            
            # Append data to lists
            timestamps.append(timestamp)
            intensity_values.append(intensity)
        except ValueError:
            pass

    # Clear the current plot
    plt.cla()

    # Plot data
    plt.plot(timestamps, intensity_values, label='Intensity')
    plt.xlabel('Time')
    plt.ylabel('Intensity')
    plt.title('Real-Time Muscle Sensor Data')
    plt.legend(loc='upper right')
    plt.grid(True)  # Enable grid
    plt.tight_layout()

# Set up the real-time plot with a larger figure size
fig = plt.figure(figsize=(12, 6))
ani = FuncAnimation(fig, update, interval=20)  # Update every 20ms

# Function to save data to CSV file
def save_to_csv():
    data = {'Timestamp': timestamps, 'Intensity': intensity_values}
    df = pd.DataFrame(data)
    folder_path = r'C:\Users\jayad\Documents\Arduino\Python\Limit Switch'
    os.makedirs(folder_path, exist_ok=True)  # Create directory if it doesn't exist
    filename = os.path.join(folder_path, 'muscle_sensor_data.csv')
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')

# Function to save the plot as a vector image with higher resolution
def save_vector_image():
    folder_path = r'C:\Users\jayad\Documents\Arduino\Python\Limit Switch'
    os.makedirs(folder_path, exist_ok=True)  # Create directory if it doesn't exist
    filename = os.path.join(folder_path, 'muscle_sensor_plot.svg')
    fig.savefig(filename, format='svg', dpi=300)  # Higher DPI for better resolution
    print(f'Plot saved as {filename}')

# Signal handler to save data and plot on exit
def signal_handler(sig, frame):
    print('Exiting and saving data...')
    save_to_csv()
    save_vector_image()
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Function to handle plot window closure
def on_close(event):
    print('Plot window closed, saving data...')
    save_to_csv()
    save_vector_image()

# Connect the plot window close event to the function
fig.canvas.mpl_connect('close_event', on_close)

# Show the plot
plt.show()

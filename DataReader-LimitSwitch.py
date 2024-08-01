import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from openpyxl import Workbook
import datetime

# Setup serial connection
ser = serial.Serial('COM3', 9600)

# Create a workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Sensor Data"

# Write the headers
ws.append(["Timestamp", "Pin 6", "Pin 7"])

# Create figure for plotting
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Pin 6')
line2, = ax.plot([], [], label='Pin 7')
ax.legend()
plt.title('Real-time Arduino Data')
plt.xlabel('Time')
plt.ylabel('Digital Value (0 or 1)')
ax.set_ylim(0, 1)

# Variables to store data
x_data = []
y_data_6 = []
y_data_7 = []

def init():
    ax.set_xlim(0, 100)
    return line1, line2

def update(frame):
    line = ser.readline().decode('utf-8').strip()
    print(f"Received line: {line}")  # Debugging line to check incoming data
    try:
        if ',' not in line:
            print("Error: line does not contain a comma")
            return line1, line2
        
        sensor_value_6, sensor_value_7 = map(int, line.split(','))
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save the data to the Excel sheet
        ws.append([timestamp, sensor_value_6, sensor_value_7])
        # Save the workbook periodically to avoid data loss in case of interruption
        if len(x_data) % 10 == 0:  # Save every 10 data points
            wb.save("sensor_data.xlsx")

        # Update the plot data
        x_data.append(len(x_data))
        y_data_6.append(sensor_value_6)
        y_data_7.append(sensor_value_7)
        
        if len(x_data) > 100:  # Keep the latest 100 data points
            x_data.pop(0)
            y_data_6.pop(0)
            y_data_7.pop(0)

        ax.set_xlim(max(0, len(x_data)-100), len(x_data))

        line1.set_data(x_data, y_data_6)
        line2.set_data(x_data, y_data_7)
    except ValueError:
        print("Error parsing line:", line)  # Debugging line to check for parsing errors
        pass  # In case of bad data, skip it

    return line1, line2

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=100)
plt.show()

ser.close()
wb.save("sensor_data.xlsx")  # Save the workbook one last time at the end

import serial
import time
from openpyxl import Workbook

# Define serial port settings
ser = serial.Serial('COM3', 9600)  # Update 'COM3' to your Arduino's COM port

# Create a new Excel workbook and select the active sheet
wb = Workbook()
ws = wb.active
ws.append(["Time", "Data"])  # Header row

# Constants
MAX_READINGS = 1000  # Number of readings to take before stopping
MIN_VALUE = 0  # Minimum acceptable value
MAX_VALUE = 1023  # Maximum acceptable value
MAX_DEVIATION = 100  # Maximum allowed deviation between consecutive readings

try:
    count = 0
    last_value = None
    
    while count < MAX_READINGS:
        data = ser.read_all().decode('utf-8')
        
        if data:
            lines = data.splitlines()
            for line in lines:
                try:
                    value = float(line.strip())
                    
                    # Filter out unrealistic values and spikes
                    if MIN_VALUE <= value <= MAX_VALUE:
                        if last_value is None or abs(value - last_value) <= MAX_DEVIATION:
                            timestamp = time.strftime('%H:%M:%S')
                            ws.append([timestamp, value])
                            count += 1
                            
                            # Save to Excel periodically
                            if count % 10 == 0:
                                wb.save("arduino_data.xlsx")
                            
                            print(f"Reading {count}/{MAX_READINGS}: {value}")
                            
                            # Update last_value
                            last_value = value
                        else:
                            print(f"Ignore spike: {value}")
                    
                    else:
                        print(f"Ignore unrealistic value: {value}")
                        
                except ValueError:
                    print(f"Ignore non-numeric data: {line}")
        
        time.sleep(0.1)  # Adjust delay as needed to prevent high CPU usage

    print(f"Finished taking {MAX_READINGS} readings. Exiting...")

except KeyboardInterrupt:
    print("Logging stopped by user.")

finally:
    ser.close()
    wb.save("arduino_data.xlsx")  # Save final changes before closing
    print("Excel file saved.")

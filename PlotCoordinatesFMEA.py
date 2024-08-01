import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# File path
file_path = r"C:\Users\jayad\Desktop\New folder (3)\FMEA\Plot.xlsx"

# Read the Excel file
df = pd.read_excel(file_path, sheet_name=0)  # Adjust if needed

# Print the DataFrame and its columns to debug
print("DataFrame Head:")
print(df.head())
print("Columns:", df.columns)

# Ensure the DataFrame has at least 3 columns
if len(df.columns) < 3:
    raise IndexError("The DataFrame does not have at least 3 columns.")

# Extract the coordinates and labels
x = df.iloc[:, 0]  # Column index A (0-based index)
y = df.iloc[:, 1]  # Column index B (0-based index)
labels = df.iloc[:, 2]  # Column index C (0-based index)

# Initialize plot with higher resolution
plt.figure(figsize=(19.2, 10.8), dpi=100)  # Set figure size to match 1920x1080 resolution

# Plot the coordinates
plt.scatter(x, y, color='blue', edgecolor='k', s=100)  # Scatter plot with blue points

# Function to place labels around the point in a circular pattern
def place_labels_around_point(x, y, labels, radius=0.5, n_labels=1):
    angles = np.linspace(0, 2 * np.pi, n_labels, endpoint=False)  # Generate evenly spaced angles
    for i in range(n_labels):
        angle = angles[i]
        offset_x = radius * np.cos(angle)
        offset_y = radius * np.sin(angle)
        plt.text(x + offset_x, y + offset_y, str(labels[i]), fontsize=9, ha='center', va='center', color='black')

# Place labels around each point
for i in range(len(x)):
    # Collect labels for points that are at the same coordinates
    overlapping_labels = [labels[j] for j in range(len(x)) if x[j] == x[i] and y[j] == y[i]]
    
    # Number of overlapping labels
    num_labels = len(overlapping_labels)
    
    # Place labels in a circular pattern around the point
    place_labels_around_point(x[i], y[i], overlapping_labels, radius=0.5, n_labels=num_labels)

# Shade the red triangle region above the line connecting (10, 0) to (0, 10)
x_fill_red = np.array([0, 10, 10, 0])
y_fill_red = np.array([10, 0, 10, 10])
plt.fill(x_fill_red, y_fill_red, color='lightcoral', alpha=0.5, label='High Priority')

# Shade the yellow parallelogram between the lines connecting (0, 10) to (10, 0) and (0, 5) to (5, 0)
x_fill_yellow = np.array([0, 10, 5, 0])
y_fill_yellow = np.array([10, 0, 0, 5])
plt.fill(x_fill_yellow, y_fill_yellow, color='lightyellow', alpha=0.5, label='Medium Priority')

# Shade the blue triangle region below the line connecting (5, 0) to (0, 5)
x_fill_blue = np.array([0, 5, 0])
y_fill_blue = np.array([0, 0, 5])
plt.fill(x_fill_blue, y_fill_blue, color='lightblue', alpha=0.5, label='Low Priority')

# Set fixed axis limits with more resolution
plt.xlim(0, 10)
plt.ylim(0, 10)

# Set grid lines with major and minor ticks for better resolution
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.5')

# Rename axes
plt.xlabel('Severity')
plt.ylabel('Occurrence')

# Update plot title
plt.title('Occurrence versus Severity')

plt.legend()
plt.show()

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the input and output directories
input_dir = r'C:\Users\jayad\Documents\Arduino\Python\FSR\New folder'
output_dir = r'C:\Users\jayad\Documents\Arduino\Python\FSR\New folder\Graphs'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get a list of all Excel files in the input directory
excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]

# Initialize a figure for the combined plot with adjusted size and aspect ratio
combined_fig, combined_ax = plt.subplots(figsize=(15, 8))  # Set the figure size to 1080x720 (aspect ratio 15:8)

# Define the y-axis limits
y_axis_limits = (1, 1000)

for file in excel_files:
    # Read the Excel file
    file_path = os.path.join(input_dir, file)
    df = pd.read_excel(file_path)

    # Check if the file has at least two columns
    if df.shape[1] >= 2:
        # Convert timestamps in the first column to durations
        df['Duration'] = (pd.to_datetime(df.iloc[:, 0]) - pd.to_datetime(df.iloc[:, 0][0])).dt.total_seconds()

        # Plot the individual graph with adjusted size and aspect ratio
        plt.figure(figsize=(15, 8))  # Set the figure size to 1080x720 (aspect ratio 15:8)
        plt.plot(df['Duration'], df.iloc[:, 1])
        plt.xlabel('Duration (seconds)')
        plt.ylabel('Sensor Data')  # Change y-axis label
        plt.title(f'Plot of {os.path.splitext(file)[0]}')  # Remove file extension from title
        plt.ylim(y_axis_limits)  # Set y-axis limits

        # Save the individual plot without file extension in the title
        plot_name = os.path.splitext(file)[0]  # Get filename without extension
        plot_path = os.path.join(output_dir, f'{plot_name}_plot.png')
        plt.savefig(plot_path)
        plt.close()

        # Add the current plot to the combined plot with a label (without legend)
        combined_ax.plot(df['Duration'], df.iloc[:, 1], label=plot_name)

# Finalize the combined plot
combined_ax.set_xlabel('Duration (seconds)')
combined_ax.set_ylabel('Sensor Data')  # Change y-axis label
combined_ax.set_title('Combined Plot of All Files')
combined_ax.set_ylim(y_axis_limits)  # Set y-axis limits
combined_ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))  # Move legend outside the plot
combined_fig.tight_layout()  # Adjust layout for better spacing

# Save the combined plot with adjusted size and aspect ratio
combined_plot_path = os.path.join(output_dir, 'combined_plot.png')
combined_fig.savefig(combined_plot_path, bbox_inches='tight')
plt.close(combined_fig)

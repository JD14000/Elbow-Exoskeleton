import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the input and output directories
input_dir = r'C:\Users\jayad\Documents\Arduino\Python\Limit Switch\Newfolder'
output_dir = r'C:\Users\jayad\Documents\Arduino\Python\Limit Switch\New folder\Graphs'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get a list of all Excel files in the input directory
excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]

for file in excel_files:
    # Read the Excel file
    file_path = os.path.join(input_dir, file)
    df = pd.read_excel(file_path)

    # Check if the file has at least three columns
    if df.shape[1] >= 3:
        # Convert timestamps in the first column to durations in milliseconds
        df['Duration'] = (pd.to_datetime(df.iloc[:, 0]) - pd.to_datetime(df.iloc[:, 0][0])).dt.total_seconds() * 1000

        # Plot both the second and third columns against the first column (duration)
        plt.figure(figsize=(15, 8))  # Set the figure size to 1080x720 (aspect ratio 15:8)
        plt.plot(df['Duration'], df.iloc[:, 1], label='Pin 6')
        plt.plot(df['Duration'], df.iloc[:, 2], label='Pin 7')
        plt.xlabel('Duration (milliseconds)')
        plt.ylabel('Values')
        plt.title(f'Plot of {os.path.splitext(file)[0]}')
        plt.legend()

        # Save the plot
        plot_path = os.path.join(output_dir, f'{os.path.splitext(file)[0]}_combined_plot.png')
        plt.savefig(plot_path)
        plt.close()
    else:
        print(f"Skipping file {file} as it does not contain at least three columns.")

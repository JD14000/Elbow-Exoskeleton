import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
excel_file = 'path_to_your_excel_file.xlsx'

# Read the data into a DataFrame
df = pd.read_excel(excel_file, usecols=['A', 'B'], engine='openpyxl')

# Parse the timestamp column (Column A) to datetime format
df['A'] = pd.to_datetime(df['A'])

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(df['A'], df['B'], marker='o', linestyle='-')

# Set the title and labels
plt.title('Time Series Plot')
plt.xlabel('Time')
plt.ylabel('Values')

# Format the x-axis for better readability
plt.gcf().autofmt_xdate()

# Show the grid for better readability
plt.grid(True)

# Display the plot
plt.show()

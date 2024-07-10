import pandas as pd
import matplotlib.pyplot as plt


# Sample data
# data = [
#     "E:/Scanned and Processed strips/TEST_06_11_24,07/02/2024 08:27:32 PM,0:30:13",
#     "E:/Scanned and Processed strips/TEST_06_12_24,07/02/2024 08:34:08 PM,0:20:04",
#     "E:/Scanned and Processed strips/TEST_06_13_24,07/02/2024 09:27:32 PM,0:20:43",
#     "E:/Scanned and Processed strips/TEST_06_14_24,07/02/2024 10:27:08 PM,0:20:04",
#     "E:/Scanned and Processed strips/TEST_06_11_24,08/02/2024 08:27:32 PM,0:50:13",
#     "E:/Scanned and Processed strips/TEST_06_12_24,08/02/2024 08:34:08 PM,0:20:04",
#     "E:/Scanned and Processed strips/TEST_06_13_24,09/02/2024 09:27:32 PM,1:20:43",
#     "E:/Scanned and Processed strips/TEST_06_14_24,09/02/2024 10:27:08 PM,0:20:04"
# ]
csv_path = "completion_times.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Optional: Set column names with better descriptions (assuming specific format)
df.columns = ["Job", "Completion Time", "Duration"]

# Convert 'Completion Time' to datetime
df['Completion Time'] = pd.to_datetime(df['Completion Time'], format='%m/%d/%Y %I:%M:%S %p')

# Extract the date part from 'Completion Time'
df['Date'] = df['Completion Time'].dt.date

# Convert 'Duration' to timedelta
df['Duration'] = pd.to_timedelta(df['Duration'])

# Calculate total duration per day
daily_total_duration = df.groupby('Date')['Duration'].sum()

# Plotting the data
plt.figure(figsize=(10, 6))
daily_total_duration.plot(kind='bar', color='skyblue')
plt.xlabel('Date')
plt.ylabel('Total Duration')
plt.title('Total Time Taken for All Jobs by Day')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Load the sleep data file
sleep_data_path = '../data/harris-sleep-data-feb-2023.csv'
sleep_data = pd.read_csv(sleep_data_path)

# Convert 'Start' and 'End' columns to datetime and extract dates and times
sleep_data['Start'] = pd.to_datetime(sleep_data['Start'])
sleep_data['End'] = pd.to_datetime(sleep_data['End'])
sleep_data['StartDate'] = sleep_data['Start'].dt.date
sleep_data['StartTime'] = sleep_data['Start'].dt.time
sleep_data['EndDate'] = sleep_data['End'].dt.date
sleep_data['EndTime'] = sleep_data['End'].dt.time

# Filter out rows where 'End' is NaT
# Instead of directly assigning values to the filtered DataFrame, use .copy() to explicitly create a copy
filtered_sleep_data = sleep_data.dropna(subset=['End']).copy()

# Function to convert time to hours since midnight
def time_to_hours(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    return time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600

# Convert times into hours
# Convert times into hours using .loc to avoid SettingWithCopyWarning
filtered_sleep_data.loc[:, 'StartHour'] = filtered_sleep_data['StartTime'].astype(str).apply(time_to_hours)
filtered_sleep_data.loc[:, 'EndHour'] = filtered_sleep_data['EndTime'].astype(str).apply(time_to_hours)

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
days = filtered_sleep_data['StartDate'].unique()
for day in days:
    day_data = filtered_sleep_data[filtered_sleep_data['StartDate'] == day]
    for _, row in day_data.iterrows():
        duration_hours = row['EndHour'] - row['StartHour']
        if duration_hours < 0:  # Handle overnight sleep
            duration_hours += 24
        ax.bar(row['StartDate'], duration_hours, bottom=row['StartHour'], width=0.4, align='center')

# Format the x-axis
plt.xticks(rotation=45)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Format the y-axis to show hours
ax.set_yticks(np.arange(0, 24, 1))
ax.set_yticklabels([f'{int(hour):02d}:00' for hour in np.arange(0, 24, 1)])
plt.ylim(0, 24)
plt.ylabel('Time of Day')
plt.xlabel('Date')
plt.title('Sleep Patterns for February 2023 - Bar Graph Style')
plt.grid(True, axis='y')

plt.tight_layout()
plt.savefig('../results/bar_graph.png')

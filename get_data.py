# These are libraries of python
import requests, os, pandas as pd
import matplotlib.pyplot as plt

# These are the built-in modules
from datetime import datetime, timedelta

#-----------------------------------------
today = datetime.now();
week_ago = today - timedelta(days = 7);

# Format dates for API (YYYY-MM-DD)
start_date = week_ago.strftime("%Y-%m-%d");
end_date= today.strftime("%Y-%m-%d");

# Get Paris weather for past week
url = f"https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

#sending the request to API
response = requests.get(url);
data = response.json();

#----------------------------------------------
# Extracting the daily max and min temperatures
daily_data  = data["daily"];

#create a dataframe inserting this data
df = pd.DataFrame({
    "date" : daily_data["time"],
    "max_temp" : daily_data["temperature_2m_max"],
    "min_temp" : daily_data["temperature_2m_min"]
});

# convert date strings to datetime. Because datetime objects are much easier to use for:
# sorting dates, calculating differences, plotting the dates...
df["date"] = pd.to_datetime(df["date"]);

#--------------------------create the plot
plt.figure(figsize=(10,6))
plt.plot(df["date"], df["max_temp"], marker = 'o', label = 'Max Temp');
plt.plot(df["date"], df["min_temp"], marker = 'o', label = "MIn Temp");
# Add labels and title
plt.xlabel("Date");
plt.ylabel("Temperature (°C)");
plt.title("PAris Weather report for the past - 7 days")
plt.legend();

plt.xticks(rotation = 30);
plt.tight_layout();

plt.savefig("paris_weather_report.png");
plt.show();

#----------------------------------------------
#File creation
if not os.path.exists("data"):
    os.makedirs("data");

# Save the data to a CSV file 
df.to_csv('data/paris_weather.csv', index = False)
print("Data is saved successfully...")
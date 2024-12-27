import requests
import time

# Define the required parameters
api_key = r"EYpogGibFrIWHqNCgPwQAuBxypYHNbXk"
latitude = 40.7128  # Example latitude (New York City)
longitude = -74.0060  # Example longitude (New York City)
start_time = int(time.time() - 3600)  # 1 hour ago
end_time = int(time.time())  # Current timestamp

# NOAA API for historical weather data (1-hour window)
url = (
    f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?"
    f"dataset=GHCND&"
    f"startDate={time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_time))}&"
    f"endDate={time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(end_time))}&"
    f"stations=USW00014739&"  # Station ID (use the relevant station ID)
    f"limit=1000&"
    f"format=JSON"
)

# Make the API request
response = requests.get(url, headers={'Token': api_key})

# Check for response
if response.status_code == 200:
    data = response.json()
    for entry in data['results']:
        print(f"Time: {entry['date']} | Temperature: {entry['value']}°F")
else:
    print(f"Error: {response.status_code}, {response.text}")

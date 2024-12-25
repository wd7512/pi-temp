import pytz

TIMEZONE = pytz.timezone('Europe/Lisbon')

def get_sensor_data():
    import datetime
    temperature_c = 20  # Mock temperature value
    humidity = 50       # Mock humidity value
    pressure = 1000     # Mock pressure value
    # Generate a timestamp for the current time
    timestamp_tz = datetime.datetime.now(pytz.utc).astimezone(TIMEZONE)
    return timestamp_tz, temperature_c, humidity, pressure
import smbus2
import bme280
import pytz

# Constants
ADDRESS = 0x77
TIMEZONE = pytz.timezone('Europe/Lisbon')

# Initialize I2C bus and load calibration
bus = smbus2.SMBus(1)
calibration_params = bme280.load_calibration_params(bus, ADDRESS)

def get_sensor_data():
    data = bme280.sample(bus, ADDRESS, calibration_params)
    temperature_c = data.temperature
    humidity = data.humidity
    pressure = data.pressure
    timestamp_tz = data.timestamp.replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
    return timestamp_tz, temperature_c, humidity, pressure

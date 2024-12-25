from firebase import upload_sensor_data
from BME280_script import get_sensor_data
from datetime import datetime, timedelta
import time

print("Initialised Script")

def wait_for_next_minute():
    """Wait until the next whole minute starts."""
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    time.sleep((next_minute - now).total_seconds())

def main():
    try:
        while True:
            try:
                data = get_sensor_data()
                upload_sensor_data(*data)
            except Exception as e:
                print(f"Error during data upload: {e}")
            
            # Wait for the next full minute
            wait_for_next_minute()
    except KeyboardInterrupt:
        print("Program stopped")

if __name__ == "__main__":
    main()

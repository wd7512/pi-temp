from meteostat import Point, Hourly, Daily
import pandas as pd
from datetime import datetime

def get_weather_data(lat, lon, alt, start_date, end_date, granularity="daily"):
    """
    Fetch historical weather data for a given location and time range.

    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        alt (float): Altitude of the location in meters.
        start_date (datetime): Start date for the data.
        end_date (datetime): End date for the data.
        granularity (str): Granularity of the data ('daily', 'hourly', 'minute').

    Returns:
        pd.DataFrame: DataFrame containing the requested weather data.
    """
    # Define location
    location = Point(lat, lon, alt)

    # Select granularity
    if granularity == "daily":
        data = Daily(location, start_date, end_date).fetch()
    elif granularity == "hourly":
        data = Hourly(location, start_date, end_date).fetch()
    else:
        raise ValueError("Unsupported granularity. Choose 'daily' or 'hourly'.")

    return pd.DataFrame(data)
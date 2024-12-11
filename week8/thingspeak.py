from datetime import datetime
import pytz
import requests

URL = "https://api.thingspeak.com/channels/2578404/feeds.json?api_key=XSXF6WH7DAECB6S1&results=20"
FINNISH_TZ = pytz.timezone("Europe/Helsinki")


def convert_to_finnish_time(utc_time_str):
    """
    Converts the incoming time to a finnish time
    :param utc_time_str: Timestamp string
    :return: Finnish timestamp string
    """
    input_format = "%Y-%m-%dT%H:%M:%SZ"
    # Parse the UTC time string to a datetime object
    utc_time = datetime.strptime(utc_time_str, input_format)
    # Set the timezone to UTC
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    # Convert to Finnish time
    finnish_time = utc_time.astimezone(FINNISH_TZ)
    # Format the datetime object to the desired format
    return finnish_time.strftime("%d.%m.%Y, %H:%M")

def get_data():
    """
    Makes an API call to the Thingspeak API using HTTP GET method
    :return: Response JSON or None
    """
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    return None


def transform_data(raw_data):
    """
    Parses the JSON data into more usable format
    :param raw_data: JSON format data
    :return: parsed data
    """
    res = []
    for entry in raw_data["feeds"]:
        finnish_time = convert_to_finnish_time(entry["created_at"])
        data = {
            "movement": entry["field1"],
            "temperature": entry["field2"],
            "time": finnish_time
        }
        res.append(data)
    return res
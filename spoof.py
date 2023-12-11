import requests
import datetime
import random
import time

endpoint_url = "https://x8ki-letl-twmt.n7.xano.io/api:wcmTvkYk/cardetection"
while (True):
    #Generate random data
    b_box = random.randint(5,25)

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Extract year, day of the year, and hour
    current_year = current_datetime.year
    day_of_year = current_datetime.timetuple().tm_yday
    hour_of_day = current_datetime.hour

    #create json for xano post
    xjson = {
        "b_box": b_box,
        "year": current_year,
        "day": day_of_year,
        "hour": hour_of_day
    }
    # Send a PUT request to update the value
    response = requests.put(endpoint_url, json=xjson)

    # Check the response status
    if response.status_code == 200:
        print("Value updated successfully.")
    else:
        print("Failed to update value. Status code:", response.status_code)
        print("Response content:", response.content)
    time.sleep(4)
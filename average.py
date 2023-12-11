import requests
import datetime

def fetch_data(source_url, current_year, day_of_year, hour_of_day):
    try:
        

        # Create the JSON payload
        payload = {
            "year": current_year,
            "day": day_of_year,
            "hour": hour_of_day
        }

        response = requests.get(source_url, params=payload)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {source_url}: {e}")
        return None

def calculate_average_b_box(data):
    if not data:
        return None

    # Extract b_box values from the data
    bbox_values = [entry.get("b_box", 0) for entry in data]

    # Calculate the average
    average_b_box = sum(bbox_values) / len(bbox_values) if len(bbox_values) > 0 else 0
    return average_b_box

def send_data(target_url, data):
    try:
        response = requests.post(target_url, json=data)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        print("Data sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to {target_url}: {e}")

def main():
    # Replace these URLs with your actual API endpoints
    source_api_url = "https://x8ki-letl-twmt.n7.xano.io/api:wcmTvkYk/cardetection"
    target_api_url = "https://x8ki-letl-twmt.n7.xano.io/api:wcmTvkYk/cardetectionaverage"

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Extract year, day of the year, and hour
    year = current_datetime.year
    day = current_datetime.timetuple().tm_yday
    hour = current_datetime.hour

    # Fetch data from the source API
    data_to_send = fetch_data(source_api_url, year, day, hour)

    if data_to_send:
        # Calculate the average b_box value
        average_b_box = calculate_average_b_box(data_to_send)
        print(f"Average BBox value: {average_b_box}")

        #Create json to put in Avg databse
        data =  {
        "b_box_avg": average_b_box,
        "year": year,
        "day": day,
        "hour": hour
        }

        # Send data to the target API
        send_data(target_api_url, data)

if __name__ == "__main__":
    main()

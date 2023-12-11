import tkinter as tk
import tkinter.ttk as ttk
import requests
from datetime import datetime, timedelta
import pytz
import random
import time

#Function to toggle between average data and set data modes
def toggle_mode():
    global mode
    if mode == "Average":
        mode = "Set"
    else:
        mode = "Average"
    update_mode_label()
    update_title()
    update_data()

# Function to switch to the 'Data' tab
def switch_to_data_tab(event = None):
    notebook.select(1)  # Select the 'Data' tab (index 1)
# Function to switch to the 'Home' tab
def return_home(event = None):
    notebook.select(0)

# Function to fetch the latest data from the API based on the highest ID (locally sorted)
def fetch_latest_traffic_data():
    current_datetime = datetime.now()

    year = current_datetime.year
    day = current_datetime.timetuple().tm_yday
    hour = current_datetime.hour

    payload = {
        "year": year,
        "day": day,
        "hour": hour
    }
    try:
        response = requests.get("https://x8ki-letl-twmt.n7.xano.io/api:wcmTvkYk/cardetection", params = payload)
        data = response.json()
        
        if data and len(data) > 0:
            sorted_data = sorted(data, key=lambda x: x.get("id", 0), reverse=True)
            return sorted_data[0]
        else:
            return {"error": "No data available."}
    except Exception as e:
        return {"error": str(e)}
    
# Grab average data
def fetch_average_data():
    current_datetime = datetime.now()

    year = current_datetime.year
    day = current_datetime.timetuple().tm_yday
    hour = current_datetime.hour

    data = {
        "year": year,
        "day": day,
        "hour": hour
    }
    try:
        response = requests.get("https://x8ki-letl-twmt.n7.xano.io/api:wcmTvkYk/cardetectionaverage", params=data)
        #print("Average API Response:", response.text)  # Debugging statement
        rdata = response.json()
        #print(rdata)

        if isinstance(rdata, list) and len(rdata) > 0:
            # Extract "b_box_avg" from the first dictionary in the list
            return rdata[0].get("b_box_avg", None)
        else:
            return None
    except Exception as e:
        print(f"Error fetching average data: {e}")
        return None

# Calculates average data over last week
def fetch_last_seven_days_average():
    current_datetime = datetime.now()

    year = current_datetime.year
    hour = current_datetime.hour

    # Create a list to store b_box data from each day
    b_box_values = []

    # Fetch data for the last 7 days
    for i in range(1, 8):
        previous_date = current_datetime - timedelta(days=i)
        day = previous_date.timetuple().tm_yday

        payload = {
            "year": year,
            "day": day,
            "hour": hour
        }
        #print(payload)
        try:
            response = requests.get("https://x8ki-letl-twmt.n7.xano.io/api:wcmTvkYk/cardetectionaverage", params=payload)
            data = response.json()
            #print(data)
            # Check if the response has 'b_box_avg' key
            if isinstance(data, list) and len(data) > 0 and 'b_box_avg' in data[0]:
                b_box_values.append(data[0]['b_box_avg'])
            else:
                # Append 0 if 'b_box_avg' is missing or data is empty
                b_box_values.append(0)
        except Exception as e:
            print(f"Error fetching data for day {i}: {e}")
            # Append 0 if there's an error in API call
            b_box_values.append(0)
        #print(b_box_values)
        time.sleep(3)

    # Calculate the average of b_box values
    if b_box_values:
        average_b_box = sum(b_box_values) / len(b_box_values)
        return round(average_b_box)
    else:
        return None

# Function to convert timestamp to a human-readable date and time in EST
def timestamp_to_datetime(timestamp):
    try:
        timestamp = int(timestamp) / 1000  # Convert to seconds
        utc_time = datetime.utcfromtimestamp(timestamp)
        est = pytz.timezone('US/Eastern')
        est_time = utc_time.replace(tzinfo=pytz.utc).astimezone(est)
        return est_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")  # Display EST with timezone information
    except:
        return "N/A"
def checkhour(lastHour):
    current_datetime = datetime.now()
    currenthour = current_datetime.hour
    if(currenthour != lastHour):
        return True

current_hour = datetime.now().hour
average_b_box = fetch_average_data()
save_average = average_b_box
mode = "Average"
delay_id = None
color = color2 = color3 = color4 =  "green"
weekly_b_box = fetch_last_seven_days_average()
# Function to update the displayed data and calculate time since last update
def update_data():
    global current_hour
    global average_b_box
    global save_average
    global mode
    global delay_id
    global color, color2, color3, color4
    global weekly_b_box
    set = 10
    #print("first hour: ", current_hour)
    latest_record = fetch_latest_traffic_data()
    if(checkhour(current_hour)):
        current_hour = datetime.now().hour
        save_average = fetch_average_data()
        weekly_b_box = fetch_last_seven_days_average()
        

    if mode == "Average":
        average_b_box = save_average
    else:
        average_b_box = set

    if "error" in latest_record:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, latest_record["error"])
        result_text.config(bg="white")  # Set background to white if there's an error
    else:
        bbox_value = latest_record.get("b_box", "N/A")
        time_updated = latest_record.get("time_updated", "N/A")
        formatted_time_updated = timestamp_to_datetime(time_updated)
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Latest Number of Cars: {bbox_value}\nLast Updated: {formatted_time_updated}\n")
        if mode == "Average":
            result_text.insert(tk.END, f"Average Number of Cars Yesterday: {average_b_box}\n")
        else:
            result_text.insert(tk.END, f"Regular Number of Cars: {set}\n")
        result_text.insert(tk.END, f"Average Number of Cars in the Last Week: {weekly_b_box}\n")
        if average_b_box is not None:
            
            # Calculate the difference between latest and average
            difference = abs(bbox_value - average_b_box)

            # Set background to green if latest <= average, and red otherwise
            if bbox_value <= average_b_box:
                # Adjust green shade based on the difference
                if difference < 5:
                    color = "#DDFFDD" # Lighter green if close
                elif difference < 10:
                    color = "#AAFFAA" # Medium green
                else:
                    color = "#77FF77" # Darker green if far
            else:
                # Adjust red shade based on the difference
                if difference < 5:
                    color = "#FFDDDD" # Lighter red if close
                elif difference < 10:
                    color = "#FFAAAA" #Medium red
                else:
                    color = "#FF7777" # Darker red if far
                    
            result_text.config(bg = color)
            update_box_color(color)
    global last_api_call_time
    last_api_call_time = datetime.now()
    elapsed_time = datetime.now() - last_api_call_time
    time_since_last_fetch_text.config(text=f"Seconds since last fetch: {elapsed_time.total_seconds():.2f}")

    # Clear the existing timer before setting a new one
    if delay_id:
        root.after_cancel(delay_id)
    delay_id = root.after(5000, update_data)

    # Add debugging statements
    #print("Latest BBox:", bbox_value)
    #if average_b_box is not None:
    #    print("Average BBox:", average_b_box)


# Function to update the elapsed time separately
def update_elapsed_time():
    elapsed_time = datetime.now() - last_api_call_time
    time_since_last_fetch_text.config(text=f"Seconds since last fetch: {elapsed_time.total_seconds():.2f}")
    root.after(1000, update_elapsed_time)  # Schedule the function to run every second for elapsed time

# Function to update the mode label
def update_mode_label():
    mode_label.config(text=f"Mode: {mode}")

# Function to update the window title
def update_title():
    root.title(f"Traffic Visualization App - Mode: {mode}")


# Create the main window
root = tk.Tk()
root.title("Traffic Visualization App")

# Set the window size (width x height)
root.geometry("800x600")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create a 'Home' tab
home_tab = tk.Frame(notebook)
notebook.add(home_tab, text="Home")

# Create the intersection depicion
canvas = tk.Canvas(home_tab, width=400, height=400, bg = "white")
canvas.pack()
canvas.create_line(50, 150, 150, 150, fill="black", width=5)  # Horizontal road
canvas.create_line(250, 150, 350, 150, fill="black", width=5)
canvas.create_line(50, 250, 150, 250, fill="black", width=5)
canvas.create_line(250, 250, 350, 250, fill="black", width=5)
canvas.create_line(150, 50, 150, 150, fill="black", width=5)  # Vertical road
canvas.create_line(150, 250, 150, 350, fill="black", width=5) 
canvas.create_line(250, 50, 250, 150, fill="black", width=5) 
canvas.create_line(250, 250, 250, 350, fill="black", width=5) 

# Create a clickable box
box = tk.Label(home_tab,width=6, height=4, bg=color)
box.pack(pady=20)
box.bind("<Button-1>", switch_to_data_tab)

box2 = tk.Label(home_tab,width=6, height=4, bg=color2)
box2.pack(pady=20)

box3 = tk.Label(home_tab,width=6, height=4, bg=color3)
box3.pack(pady=20)

box4 = tk.Label(home_tab,width=6, height=4, bg=color4)
box4.pack(pady=20)

canvas.create_window(200, 100, window=box)
canvas.create_window(200, 300, window=box2)
canvas.create_window(100, 200, window=box3)
canvas.create_window(300, 200, window=box4)

# Function to periodically update Box color
def update_box_color(color):
    box.config(bg = color)
    colors = ["#DDFFDD", "#AAFFAA", "#77FF77", "#FFDDDD", "#FFAAAA", "#FF7777"]
    int1 = random.randint(0,5)
    int2 = random.randint(0,5)
    int3 = random.randint(0,5)
    box2.config(bg = colors[int1])
    box3.config(bg = colors[int2])
    box4.config(bg = colors[int3])



# Create a 'Data' tab
data_tab = tk.Frame(notebook)
notebook.add(data_tab, text="Data")

# Create a label for displaying mode
mode_label = tk.Label(data_tab, text=f"Mode: {mode}", font=("Helvetica", 16))
mode_label.pack()

# Create a Text widget to display the API response with larger size
result_text = tk.Text(data_tab, wrap=tk.WORD, width=60, height=20)
result_text.pack(pady=1)

# Create a label for displaying seconds since last fetch
time_since_last_fetch_text = tk.Label(data_tab, text="", font=("Helvetica", 16))
time_since_last_fetch_text.pack()

# Create a button to toggle between modes
toggle_button = tk.Button(data_tab, text="Toggle Mode", command=toggle_mode)
toggle_button.pack()

# Create a button to switch back to home
home_button = tk.Button(data_tab, text = "Home", command = return_home)
home_button.pack()

# Initialize variables
mode = "Average"
last_api_call_time = datetime.now() - timedelta(seconds=15)

# Start the data update process and elapsed time update process
update_data()
update_elapsed_time()

# Run the GUI main loop
root.mainloop()
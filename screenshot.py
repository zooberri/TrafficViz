import cv2
import os
import time
import subprocess
import pyautogui
import numpy as np

# Define the directory where you want to save the images
output_directory = "C:/Users/Moneeb Zuberi/Code Projects/TrafficViz/yolov7/inference/images/webcam"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Set the time interval for capturing images (in seconds)
capture_interval = 15
time.sleep(10)
while True:
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a NumPy array
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Generate a unique filename based on the current timestamp
    timestamp = int(time.time())
    image_filename = os.path.join(output_directory, f"image_{timestamp}.jpg")

    # Save the captured image to the specified folder
    cv2.imwrite(image_filename, frame)
    print(f"Image saved: {image_filename}")

    # Run YOLO on the captured image
    yolo_command = f'python detect.py --weights best.pt --conf 0.25 --img-size 640 --source "{image_filename}"'
    subprocess.run(yolo_command, shell=True)


    # Wait for the specified interval before capturing the next image
    time.sleep(capture_interval)

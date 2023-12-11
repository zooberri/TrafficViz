import cv2
import os
import time
import subprocess

# Define the directory where you want to save the images
output_directory = "C:/Users/Moneeb Zuberi/Code Projects/TrafficViz/yolov7/inference/images/webcam"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Set the time interval for capturing images (in seconds)
capture_interval = 15


# Open the webcam (0 represents the default camera, change it if needed)
cap = cv2.VideoCapture(1)
time.sleep(3)
while True:
    

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        break

    # Allow the camera to stabilize for 1 second
    time.sleep(1)

    # Read a frame from the webcam
    ret, frame = cap.read()

    if ret:
        # Generate a unique filename based on the current timestamp
        timestamp = int(time.time())
        image_filename = os.path.join(output_directory, f"image_{timestamp}.jpg")

        # Save the captured image to the specified folder
        cv2.imwrite(image_filename, frame)
        print(f"Image saved: {image_filename}")

        # Run YOLO on the captured image
        yolo_command = f"python detect.py --weights best.pt --conf 0.25 --img-size 640 --source inference/images/webcam/image_{timestamp}.jpg"
        subprocess.run(yolo_command, shell=True)

    

    # Wait for the specified interval before capturing the next image
    time.sleep(capture_interval)

# Release the webcam
cap.release()

# Release the webcam and close any open windows (if any)
cv2.destroyAllWindows()

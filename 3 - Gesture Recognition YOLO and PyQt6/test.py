import cv2
import sys
from ultralytics import YOLO
import time
import subprocess

global_variables = {
        'gesture_commands': {'Thumb': 'pqiv --fullscreen ~/Untitled.jpeg',
                             'Fist': 'xdg-open https://www.google.com',
                             'Five': 'xdg-open https://www.youtube.com',
                             'Four': '',
                             'Three': '',
                             'Two': '',
                             'One': '',
                             'Horns': '',
                             'Zero': '',
                             'C': ''},
        'countdown_time': 5
        }


# Load YOLO model
model = YOLO("model/yolov8_transfer_learning_v3.pt")

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()

# Initialize variables for prediction tracking
last_prediction = None
prediction_start_time = None
countdown_started = False
countdown_time = 3  # Countdown time in seconds


def execute_command(command):
    print(f"Executing command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        print(f"Command error (if any): {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")

while True:
    ret, frame = cap.read()
    if frame is None:
        print("BYE")
        break

    # Run YOLO prediction
    results = model(frame)
    
    # Get the prediction with the highest confidence
    current_prediction = "No detection"
    if len(results) > 0 and len(results[0].boxes) > 0:
        best_box = results[0].boxes[0]
        if best_box.conf.item() > 0.5:  # Adjust confidence threshold as needed
            current_prediction = results[0].names[int(best_box.cls)]

    # Check if prediction is stable
    if current_prediction == last_prediction:
        if prediction_start_time is None:
            prediction_start_time = time.time()
        elif time.time() - prediction_start_time >= 1 and not countdown_started:
            countdown_started = True
            countdown_end_time = time.time() + global_variables['countdown_time']
    else:
        last_prediction = current_prediction
        prediction_start_time = None
        countdown_started = False

    # Draw prediction and countdown on frame
    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame, f"Prediction: {current_prediction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if countdown_started:
        remaining_time = max(0, int(countdown_end_time - time.time()))
        cv2.putText(annotated_frame, f"Countdown: {remaining_time}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if remaining_time == 0:
            countdown_started = False
            if current_prediction != "No detection" and current_prediction not in global_variables['gesture_commands']:
                continue
            
            if current_prediction in global_variables['gesture_commands']:
                print(f"Detected stable gesture: {current_prediction}")
                if global_variables['gesture_commands'][current_prediction] == '':
                    # Destroy all windows
                    break
                execute_command(global_variables['gesture_commands'][current_prediction])

    cv2.imshow('YOLO Detection', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'images'))

import cv2
import time
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from src.MainWindow import GestureRecognitionUI
from ultralytics import YOLO
from src.settings import SettingsDialog


FILE = "settings.txt"


class GestureRecognitionApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = GestureRecognitionUI()
        self.ui.setupUi(self)

        # Initialize YOLO model
        self.model = YOLO("model/yolov8_transfer_learning_v3.pt")

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            sys.exit(1)

        # Set up a QTimer to periodically capture frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Timer interval in milliseconds

        self.last_prediction = None
        self.prediction_start_time = None
        self.countdown_started = False
        self.countdown_end_time = 0



    def update_frame(self):
        """Capture a frame from the camera and process it"""
        ret, frame = self.cap.read()

        if not ret:
            print("Error: Could not read frame.")
            return
        
        frame = cv2.resize(frame, (640, 480))

        result = self.model(frame)
        current_prediction = None
        highest_confidence = 0
        best_box = None

        # Process results and find the highest confidence bounding box
        if len(result) > 0 and len(result[0].boxes) > 0:
            for box in result[0].boxes:
                if box.conf.item() > highest_confidence:
                    highest_confidence = box.conf.item()
                    best_box = box

            if best_box is not None and highest_confidence > 0.55:
                current_prediction = result[0].names[int(best_box.cls)]

                # Draw the bounding box on the frame
                x1, y1, x2, y2 = map(int, best_box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{current_prediction} ({highest_confidence:.2f})', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                text = self.ui.settings.gesture_commands.get(current_prediction, '')
                if len(text) > 25:
                    text = text[:25] + "..."
                self.ui.command_text.setText(text)

        # Handle gesture execution
        if current_prediction == self.last_prediction:
            if self.prediction_start_time is None:
                self.prediction_start_time = time.time()
            elif time.time() - self.prediction_start_time >= 1 and not self.countdown_started:
                self.countdown_started = True
                self.countdown_end_time = time.time() + self.ui.settings.countdown
        else:
            self.last_prediction = current_prediction
            self.prediction_start_time = None
            self.countdown_started = False

        self.ui.display_gesture(current_prediction)

        if self.countdown_started:
            remaining_time = max(0, int(self.countdown_end_time - time.time()))
            self.ui.update_progress_bar(remaining_time, self.ui.settings.countdown)

            if remaining_time == 0:
                self.countdown_started = False
                if current_prediction is not None and self.ui.settings.gesture_commands.get(current_prediction, '') != '':
                    self.execute_command(self.ui.settings.gesture_commands[current_prediction])

        # Update the camera image display
        self.update_image(frame)


    def open_settings_dialog(self):
        dialog = SettingsDialog(self.ui.settings)
        if dialog.exec():
            self.update_settings(dialog.get_settings())

    def update_settings(self, new_settings):
        self.ui.settings = new_settings
        self.save_settings_to_file()

    def save_settings_to_file(self):
        with open(FILE, "w") as file:
            for gesture, command in self.ui.settings.gesture_commands.items():
                file.write(f"{gesture}<=>{command}\n")
            file.write(f"countdown<=>{self.ui.settings.countdown}\n")

    def update_image(self, frame):
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            scaled_pixmap = QPixmap.fromImage(qt_image.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio))
            self.ui.camera_image.setPixmap(scaled_pixmap)
        else:
            print("Error: Frame is None or has invalid shape.")

    def execute_command(self, command):
        subprocess.run(command, shell=True)

    def closeEvent(self, event):

        """Handle window close event"""
        if self.cap.isOpened():
            self.cap.release()  # Release the camera
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = GestureRecognitionApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


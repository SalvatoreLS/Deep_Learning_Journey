# PyQt6 Gesture Command Executor
## Overview

The PyQt6 Gesture Command Executor is a graphical user interface (GUI) application that allows users to define commands and execute them based on hand gestures detected using a YOLO (You Only Look Once) gesture detection algorithm. This project uses the PyQt6 framework for its GUI and employs the YOLO algorithm for real-time hand gesture recognition.

## Features

- **GUI for Command Definition**: Easily define and manage commands that will be triggered by specific gestures.
- **Real-time Gesture Detection**: Utilize YOLO for accurate and efficient hand gesture recognition.
- **Customizable Gestures**: Map gestures to specific commands as per your requirements. Commands are saved automatically on a `settings.txt` file and retrieved any time the program starts.
They can be defined by pressing the "settings" button on the GUI.
- **Interactive Interface**: Simple interactive interface built in PyQt6 to simplify interaction and commands definition.

## Developing path

Throughout the development of this project, I iterated through 13 different versions of the algorithm, refining data and parameters.

The dataset initially contained approximately 250 images, but it was later expanded to around 400 images.
Data augmentation brought the number to 1000.
The **augmentation techniques** used are:
- Rotation
- Noise
- Blur
- Brightness

The third version showed better results in gesture detection, although it occasionally produced false positives in some parts of the image.

For this reason I decided to introduce a further class and address the issue.
The intent was to make the algorithm recognize false positive as part of an extra class, preventing them from being assigned to a valid class.
Although this approach is useful in some cases, overall performance slightly decreased.

In subsequent versions, I enriched the dataset with the purpose of addressing the weak points of the algorithm.

To conclude, I recommend using version 3 of the algorithm, as it shows the best results, despite not being perfect.
If you wish to try later versions, you can modify the version used in `app.py` or `test.py`.

## Further improvements
- **Multi-threading**: performance could be improved by using QThread or the standard threading library to enable multi-threading

## Prerequisites

Make sure you have the following installed:

- Python 3.8 or higher
- PyQt6
- OpenCV
- ultralytics

Be sure to install any dependency in `requirements.txt`:
```bash
    pip install -r requirements.txt
```

## Usage

Run the Application:

```bash
python main.py
```

Define Commands:
- Open the command definition window from the GUI.
- Add new commands and associate them with specific gestures.

Test Gestures:
- Use your webcam to perform gestures.
- The application will detect gestures in real-time and execute the corresponding commands.

## Note
This is my first project in computer vision, so it may not be perfect. The dataset used for gesture recognition was not sourced from any existing datasets but was manually collected and labeled using [Roboflow](https://roboflow.com/). Please be aware that this might affect the accuracy and performance of the gesture detection.

## Contributing

Feel free to contribute by submitting issues, pull requests or by providing any suggestion that could lead to better results. Your feedback and improvements are welcome!

## License
This project is licensed under the MIT License.
# settings.py

from PyQt6 import QtWidgets, QtCore

FILE = "settings.txt"


class Settings():
    def __init__(self):
        self.gesture_commands = {'Thumb': '',
                                 'Zero': '',
                                 'One': '',
                                 'Two': '',
                                 'Three': '',
                                 'Four': '',
                                 'Five': '',
                                 'C': '',
                                 'Horns': '',
                                 'Fist': ''}
        self.countdown = 3

    # read data from file and fill the settings
    def fill_settings(self, settings_file):
        with open(settings_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line == "":
                    continue
                key, value = line.split("<=>")
                if key == "countdown":
                    self.countdown = int(value)
                else:
                    self.gesture_commands[key] = value


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, current_settings):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.current_settings = current_settings
        self.load_current_settings()

        # Connect the OK button to accept the dialog
        self.ui.buttonBox.accepted.connect(self.accept)
        # Connect the Cancel button to reject the dialog
        self.ui.buttonBox.rejected.connect(self.reject)

    def load_current_settings(self):
        # Populate the dialog fields with current settings
        gestures = ["Thumb", "Zero", "One", "Two", "Three", "Four", "Five", "Horns", "Fist", "C"]
        for i, gesture in enumerate(gestures):
            input_field = self.ui.gestures_settings.itemAt(i, QtWidgets.QFormLayout.ItemRole.FieldRole).widget()
            input_field.setText(self.current_settings.gesture_commands[gesture])

        self.ui.countdown_value.setText(str(self.current_settings.countdown))

    def get_settings(self):
        # Retrieve the settings from the dialog fields
        new_settings = Settings()
        new_settings.fill_settings(FILE)
        gestures = ["Thumb", "Zero", "One", "Two", "Three", "Four", "Five", "Horns", "Fist", "C"]
        for i, gesture in enumerate(gestures):
            input_field = self.ui.gestures_settings.itemAt(i, QtWidgets.QFormLayout.ItemRole.FieldRole).widget()
            new_settings.gesture_commands[gesture] = input_field.text()

        new_settings.countdown = int(self.ui.countdown_value.text())
        return new_settings

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 600)  # Reduced width and height
        
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        
        # Create a scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        
        # Gestures settings
        self.gestures_settings = QtWidgets.QFormLayout()
        self.gestures_settings.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.gestures_settings.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        
        gestures = ["Thumb", "Zero", "One", "Two", "Three", "Four", "Five", "Horns", "Fist", "C"]
        for gesture in gestures:
            label = QtWidgets.QLabel(gesture)
            input_field = QtWidgets.QLineEdit()  # Changed to QLineEdit for smaller input
            input_field.setFixedHeight(25)  # Reduced height
            self.gestures_settings.addRow(label, input_field)
        
        self.scroll_layout.addLayout(self.gestures_settings)
        
        # Countdown settings
        self.countdown_settings = QtWidgets.QHBoxLayout()
        self.countdown_label = QtWidgets.QLabel("Countdown length")
        self.countdown_value = QtWidgets.QLineEdit()  # Changed to QLineEdit
        self.countdown_value.setFixedHeight(25)  # Reduced height
        self.countdown_settings.addWidget(self.countdown_label)
        self.countdown_settings.addWidget(self.countdown_value)
        
        self.scroll_layout.addLayout(self.countdown_settings)
        
        # Set up scroll area
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        # Button box
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel|
            QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.main_layout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))

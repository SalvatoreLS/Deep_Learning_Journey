# MainWindow.py
import sys
import os

from PyQt6 import QtCore, QtGui, QtWidgets
from settings import Settings, SettingsDialog
from info import InfoDialog

# GLOBALS
FILE = "settings.txt"


class GestureRecognitionUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(966, 845)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Camera frame and image
        self.camera_frame = QtWidgets.QHBoxLayout()
        self.camera_frame.setObjectName("camera_frame")
        self.camera_image = QtWidgets.QLabel(parent=self.centralwidget)
        self.camera_image.setMaximumWidth(1100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_image.sizePolicy().hasHeightForWidth())
        self.camera_image.setSizePolicy(sizePolicy)
        self.camera_image.setObjectName("camera_image")
        self.camera_image.setScaledContents(True)
        self.camera_frame.addWidget(self.camera_image)
        self.verticalLayout_2.addLayout(self.camera_frame)

        # Lower section
        self.lower_section = QtWidgets.QHBoxLayout()
        self.lower_section.setObjectName("lower_section")

        # Buttons
        self.buttons_section = QtWidgets.QVBoxLayout()
        self.buttons_section.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.buttons_section.setContentsMargins(5, -1, 5, -1)
        self.buttons_section.setObjectName("buttons_section")
        self.settings_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.settings_button.setMinimumSize(QtCore.QSize(80, 50))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.buttons_section.addWidget(self.settings_button)
        self.info_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.info_button.setMinimumSize(QtCore.QSize(80, 50))
        self.info_button.setObjectName("info_button")
        self.info_button.clicked.connect(self.show_info_dialog)
        self.buttons_section.addWidget(self.info_button)
        self.lower_section.addLayout(self.buttons_section)

        # Gesture section
        self.gesture_section = QtWidgets.QVBoxLayout()
        self.gesture_section.setObjectName("gesture_section")
        self.gesture_section.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gesture_image = QtWidgets.QLabel(parent=self.centralwidget)
        self.gesture_image.setMinimumSize(QtCore.QSize(250, 250))
        self.gesture_image.setMaximumSize(QtCore.QSize(350, 350))
        self.gesture_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gesture_image.setFixedSize(250, 250)
        self.gesture_image.setObjectName("gesture_image")
        self.gesture_section.addWidget(self.gesture_image)
        self.progress_bar = QtWidgets.QProgressBar(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.gesture_section.addWidget(self.progress_bar)
        self.lower_section.addLayout(self.gesture_section)

        # Command section
        self.command_section = QtWidgets.QVBoxLayout()
        self.command_section.setObjectName("command_section")
        self.command_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.command_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.command_label.setObjectName("command_label")
        self.command_section.addWidget(self.command_label)
        self.command_text = QtWidgets.QLabel(parent=self.centralwidget)
        self.command_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.command_text.setObjectName("command_text")
        self.command_text.setMaximumWidth(300)
        self.command_section.addWidget(self.command_text)
        self.lower_section.addLayout(self.command_section)
        self.verticalLayout_2.addLayout(self.lower_section)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.settings = Settings()
        self.settings.fill_settings(FILE)

    def show_info_dialog(self):
        dialog = InfoDialog()
        dialog.exec()

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.settings)
        if dialog.exec():
            self.update_settings(dialog.get_settings())

    def update_settings(self, settings):
        self.settings = settings
        self.save_settings_to_file()

    def save_settings_to_file(self):
        with open(FILE, "w") as file:
            for gesture, command in self.settings.gesture_commands.items():
                file.write(f"{gesture}<=>{command}\n")
            file.write(f"countdown<=>{self.settings.countdown}\n")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.camera_image.setText(_translate("MainWindow", "CAMERA IMAGE"))
        self.settings_button.setText(_translate("MainWindow", "SETTINGS"))
        self.info_button.setText(_translate("MainWindow", "INFO"))
        self.gesture_image.setText(_translate("MainWindow", "GESTURE IMAGE"))
        self.command_label.setText(_translate("MainWindow", "Command to execute:"))
        self.command_text.setText(_translate("MainWindow", "rm -rf /"))

    def display_gesture(self, gesture):
        # Display gesture image
        pixmap = QtGui.QPixmap(f"images/{gesture}.jpg")
        self.gesture_image.setPixmap(pixmap)
        self.gesture_image.setScaledContents(True)

    def update_progress_bar(self, remaining_time, total_time):
        # Update progress bar
        value = int((total_time - remaining_time) / total_time * 100)
        self.progress_bar.setValue(value)

    def update_image(self, image):
        # Update camera image
        pixmap = QtGui.QPixmap.fromImage(image)
        self.camera_image.setPixmap(pixmap)
        self.camera_image.setScaledContents(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GestureRecognitionUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

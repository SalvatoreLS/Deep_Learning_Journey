import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDialog, QDialogButtonBox

class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        # Layout
        layout = QVBoxLayout()

        # Program Info
        program_info = QLabel("Program Name: GestureRecognitionYOLO\nVersion: 1.0\nDescription: The program is combining YOLOv8 gestures detection with PyQt6 GUI.\nThis is my first project involving computer vision.\nFurther information can be found on the README.md file.")
        developer_info = QLabel("Developer: Salvatore Lo Sardo\nEmail: losardosalvatorejr@gmail.com\nLinkedIn: https://www.linkedin.com/in/salvatore-lo-sardo-81535925b/")

        # Add widgets to layout
        layout.addWidget(program_info)
        layout.addWidget(developer_info)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        # Set the layout for the dialog
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Assuming you already have other widgets and layouts
        # Add them to the main window layout
        self.setLayout(layout)

        # Connect existing info button to show dialog
        self.info_button.clicked.connect(self.show_info_dialog)

    def show_info_dialog(self):
        dialog = InfoDialog()
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

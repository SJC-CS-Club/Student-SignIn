import sys
import os
import json
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QRegExpValidator, QIcon, QFontDatabase
from PyQt5.QtCore import QRegExp, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.full_name_input = QLineEdit()
        self.student_id_input = QLineEdit()
        self.is_cs_major_checkbox = QCheckBox("CS Major")
        self.needs_help_checkbox = QCheckBox("Zybooks Help")

        self.time = datetime.now()

        self.setup_ui()

    def setup_ui(self):
        self.setup_title_label()
        self.setup_full_name_input()
        self.setup_student_id_input()
        self.setup_checkboxes()
        self.setup_sign_in_button()
        self.central_widget.setLayout(self.main_layout)

        QFontDatabase.addApplicationFont("fonts/static/RobotoMono-Regular.ttf")

    def setup_title_label(self):
        title_label = QLabel("COSC Club")
        title_label.setObjectName("titleLabel")

        title_label.setAlignment(Qt.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.main_layout.addWidget(title_label)

    def setup_full_name_input(self):
        name_label = QLabel("Full Name:")
        self.full_name_input.setPlaceholderText("e.g. John Doe")
        self.full_name_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\s]+")))

        self.full_name_input.returnPressed.connect(self.student_id_input.setFocus)

        name_layout = QHBoxLayout()
        name_layout.addStretch()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.full_name_input)
        name_layout.addStretch()

        self.main_layout.addLayout(name_layout)

    def setup_student_id_input(self):
        id_label = QLabel("G#:")
        self.student_id_input.setPlaceholderText("e.g. 01234567")
        self.student_id_input.setValidator(QRegExpValidator(QRegExp("^[0-9]{8}$")))

        id_layout = QHBoxLayout()
        id_layout.addStretch()
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.student_id_input)
        id_layout.addStretch()

        self.main_layout.addLayout(id_layout)

    def setup_checkboxes(self):
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.is_cs_major_checkbox)
        checkbox_layout.addWidget(self.needs_help_checkbox)
        checkbox_layout.addStretch()

        self.main_layout.addLayout(checkbox_layout)

    def setup_sign_in_button(self):
        sign_in_button = QPushButton("Sign In")
        sign_in_button.setFixedWidth(100)
        sign_in_button.clicked.connect(self.submit_form)
        self.main_layout.addWidget(sign_in_button, 0, Qt.AlignCenter)

    def submit_form(self):
        name = self.full_name_input.text()
        uid = self.student_id_input.text()

        if len(name.split()) < 2:
            return QMessageBox.critical(self, "Name Error", "Please enter your full name.")

        if len(uid) != 8:
            return QMessageBox.critical(self, "ID Error", "Please enter a valid G#.")

        cs_major = self.is_cs_major_checkbox.isChecked()
        help_needed = self.needs_help_checkbox.isChecked()

        time_date = self.time.date()
        date = f"{time_date.month}-{time_date.day}-{time_date.year}"

        if not os.path.exists('form.json'):
            open('form.json', 'w').close()

        with open('form.json', 'r') as f:
            if f.read() == "":
                data = {}
            else:
                f.seek(0)
                data = json.load(f)

        if uid in data.keys():
            if help_needed:
                data[uid]["help_needed"].append(date)
            data[uid]["date"].append(date)
        else:
            data[uid] = {
                "name": name,
                "cs_major": cs_major,
                "help_needed": [date] if help_needed else [],
                "date": [date]
            }

        with open('form.json', 'w') as f:
            json.dump(data, f, indent=4)

        self.reset_form()

    def reset_form(self):
        self.full_name_input.clear()
        self.student_id_input.clear()
        self.is_cs_major_checkbox.setChecked(False)
        self.needs_help_checkbox.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    stylesheet = """
    * {
        font-family: 'Roboto Mono', monospace;
        font-size: 14px;
    }
    
    QMainWindow {
        background-image: url("assets/background.png");
    }
    
    QMessageBox {
        background-color: #0D274F;
    }

    QPushButton {
        padding: 8px;
        border-radius: 5px;
        background-color: #ebd152;
        color: #000000;
    }
    
    QPushButton:hover {
        background-color: #f3e7a8;
    }

    QLineEdit {
        max-width: 150px;
        padding: 3px 5px;
        border: 1px solid #ccc;
        border-radius: 5px;
        color: #000000;
        background-color: #FFFFFF;
    }

    QLabel {
        color: #FFFFFF;
    }

    QCheckBox {
        color: #FFFFFF;
        margin-top: 10px;
        padding: 0 5px;
    }
    
    QCheckBox::indicator {
        width: 12px;
        height: 12px;
        border: 1px solid white;
        border-radius: 4px;
    }
    
    QCheckBox::indicator:checked {
        border: 1px solid black;
        background-color: #ebd152;
    }

    #titleLabel {
        margin-top: 10px;
        color: #FFFFFF;
        font-size: 46px;
        font-weight: bold;
    }
    """
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.resize(400, 250)
    window.setWindowIcon(QIcon("assets/icon.png"))
    window.setWindowTitle("SJC CS Club")
    window.show()
    sys.exit(app.exec_())

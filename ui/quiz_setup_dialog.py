from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton,
    QButtonGroup
)
from PyQt5.QtCore import Qt
from core.storage import load_bank


class QuizSetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Setup")
        self.resize(300, 400)

        self.bank = load_bank()
        self.selected_categories = None

        layout = QVBoxLayout()

        # Mode selection
        layout.addWidget(QLabel("Select Quiz Mode"))

        self.mode_group = QButtonGroup()

        self.all_radio = QRadioButton("Entire Question Bank")
        self.cat_radio = QRadioButton("Category-wise")

        self.all_radio.setChecked(True)

        self.mode_group.addButton(self.all_radio)
        self.mode_group.addButton(self.cat_radio)

        layout.addWidget(self.all_radio)
        layout.addWidget(self.cat_radio)

        # Category list
        layout.addWidget(QLabel("Categories"))

        self.category_list = QListWidget()
        self.category_list.setSelectionMode(
            QListWidget.MultiSelection
        )

        for cat in self.bank.get("categories", {}):
            item = QListWidgetItem(cat)
            self.category_list.addItem(item)

        self.category_list.setEnabled(False)
        layout.addWidget(self.category_list)

        self.cat_radio.toggled.connect(
            self.category_list.setEnabled
        )

        # Start button
        start_btn = QPushButton("Start Quiz")
        start_btn.clicked.connect(self.accept)
        layout.addWidget(start_btn)

        self.setLayout(layout)

    def get_selection(self):
        if self.all_radio.isChecked():
            return None  # Entire bank

        return [
            item.text()
            for item in self.category_list.selectedItems()
        ]

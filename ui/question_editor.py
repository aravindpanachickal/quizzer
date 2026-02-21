from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QRadioButton, QPushButton,
    QComboBox, QButtonGroup, QMessageBox
)

from core.storage import load_bank, save_bank
from core.models import new_question


class QuestionEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.bank = load_bank()

        layout = QVBoxLayout()

        # -------- Category (Editable Dropdown) --------
        layout.addWidget(QLabel("Category"))

        self.category = QComboBox()
        self.category.setEditable(True)
        self.category.setPlaceholderText("Select or type new category")

        existing_categories = self.bank.get("categories", {}).keys()
        self.category.addItems(sorted(existing_categories))

        layout.addWidget(self.category)

        # -------- Question Text --------
        layout.addWidget(QLabel("Question"))
        self.question = QTextEdit()
        layout.addWidget(self.question)

        # -------- Options + Correct Answer --------
        self.options = []
        self.correct_group = QButtonGroup()

        for i in range(4):
            rb = QRadioButton(f"Option {chr(65 + i)}")
            self.correct_group.addButton(rb, i)

            opt = QLineEdit()
            opt.setPlaceholderText(f"Enter option {chr(65 + i)}")

            layout.addWidget(rb)
            layout.addWidget(opt)

            self.options.append(opt)

        # Default correct option
        self.correct_group.buttons()[0].setChecked(True)

        # -------- Save Button --------
        save_btn = QPushButton("Save Question")
        save_btn.clicked.connect(self.save_question)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_question(self):
        cat = self.category.currentText().strip()
        question_text = self.question.toPlainText().strip()
        options = [o.text().strip() for o in self.options]
        correct_index = self.correct_group.checkedId()

        # -------- Validation --------
        if not cat:
            QMessageBox.warning(self, "Missing Category", "Please select or enter a category.")
            return

        if not question_text:
            QMessageBox.warning(self, "Missing Question", "Question text cannot be empty.")
            return

        if any(not opt for opt in options):
            QMessageBox.warning(self, "Missing Options", "All four options must be filled.")
            return

        # -------- Create Question --------
        q = new_question(
            cat,
            question_text,
            options,
            correct_index
        )

        # -------- Save to Bank --------
        self.bank.setdefault("categories", {})
        self.bank["categories"].setdefault(cat, [])
        self.bank["categories"][cat].append(q)

        save_bank(self.bank)

        # -------- OPTIONAL IMPROVEMENT --------
        # Auto-add new category to dropdown
        if self.category.findText(cat) == -1:
            self.category.addItem(cat)

        # -------- Clear Inputs --------
        self.question.clear()
        for o in self.options:
            o.clear()
        self.correct_group.buttons()[0].setChecked(True)

        QMessageBox.information(self, "Saved", "Question saved successfully.")


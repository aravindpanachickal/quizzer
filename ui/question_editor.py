from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QRadioButton, QPushButton,
    QComboBox, QButtonGroup
)
from core.storage import load_bank, save_bank
from core.models import new_question

class QuestionEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.bank = load_bank()

        layout = QVBoxLayout()

        self.category = QLineEdit()
        self.question = QTextEdit()

        self.options = [QLineEdit() for _ in range(4)]
        self.correct_group = QButtonGroup()
        radios = []

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category)

        layout.addWidget(QLabel("Question"))
        layout.addWidget(self.question)

        for i in range(4):
            rb = QRadioButton(f"Option {chr(65+i)}")
            self.correct_group.addButton(rb, i)
            layout.addWidget(rb)
            layout.addWidget(self.options[i])
            radios.append(rb)

        radios[0].setChecked(True)

        save_btn = QPushButton("Save Question")
        save_btn.clicked.connect(self.save_question)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_question(self):
        cat = self.category.text().strip()
        if not cat:
            return

        q = new_question(
            cat,
            self.question.toPlainText(),
            [o.text() for o in self.options],
            self.correct_group.checkedId()
        )

        self.bank.setdefault("categories", {})
        self.bank["categories"].setdefault(cat, [])
        self.bank["categories"][cat].append(q)

        save_bank(self.bank)
        self.question.clear()
        for o in self.options:
            o.clear()

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton,
    QPushButton, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt
from core.quiz_engine import QuizEngine


class QuizWindow(QWidget):
    def __init__(self, categories=None):
        super().__init__()
        self.engine = QuizEngine(categories=categories)

        # For now: entire question bank
        self.engine = QuizEngine()

        self.current_question = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # Question text
        self.q_label = QLabel("")
        self.q_label.setWordWrap(True)
        self.q_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        self.layout.addWidget(self.q_label)

        # Options
        self.option_group = QButtonGroup()
        self.options = []

        for i in range(4):
            rb = QRadioButton()
            rb.setStyleSheet("font-size: 14px;")
            self.option_group.addButton(rb, i)
            self.options.append(rb)
            self.layout.addWidget(rb)

        # Submit button
        self.submit_btn = QPushButton("Save & Next")
        self.submit_btn.clicked.connect(self.submit_answer)
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)

        self.load_next_question()

    def load_next_question(self):
        self.current_question = self.engine.next_question()

        if not self.current_question:
            QMessageBox.information(
                self, "Done", "Quiz completed."
            )
            return

        # CLEAR previous selection — IMPORTANT
        self.option_group.setExclusive(False)
        for btn in self.option_group.buttons():
            btn.setChecked(False)
        self.option_group.setExclusive(True)

        self.q_label.setText(self.current_question["question"])

        for i, opt in enumerate(self.current_question["options"]):
            self.options[i].setText(
                f"{chr(65+i)}. {opt}"
            )


    def submit_answer(self):
        selected = self.option_group.checkedId()

        if selected == -1:
            QMessageBox.warning(
                self, "No Selection",
                "Please select an option."
            )
            return

        correct = self.engine.submit_answer(selected)

        if correct:
            QMessageBox.information(self, "Correct", "✔ Correct answer")
        else:
            correct_index = self.current_question["correct"]
            QMessageBox.information(
                self,
                "Wrong",
                f"✘ Wrong answer\nCorrect: {chr(65+correct_index)}"
            )

        self.load_next_question()

    # Keyboard shortcuts
    def keyPressEvent(self, event):
        key_map = {
            Qt.Key_A: 0,
            Qt.Key_B: 1,
            Qt.Key_C: 2,
            Qt.Key_D: 3
        }

        if event.key() in key_map:
            self.options[key_map[event.key()]].setChecked(True)

        elif event.key() == Qt.Key_Return:
            self.submit_answer()

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem, QLabel
)
from core.storage import load_bank


class QuestionViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.bank = load_bank()

        main_layout = QHBoxLayout()

        # LEFT: question list
        self.question_list = QListWidget()
        self.question_list.itemClicked.connect(self.show_question)

        # RIGHT: question detail
        self.detail_panel = QVBoxLayout()
        self.q_label = QLabel("")
        self.q_label.setWordWrap(True)
        self.detail_panel.addWidget(self.q_label)

        self.option_labels = []
        for _ in range(4):
            lbl = QLabel("")
            lbl.setWordWrap(True)
            self.option_labels.append(lbl)
            self.detail_panel.addWidget(lbl)

        self.answer_label = QLabel("")
        self.answer_label.setStyleSheet("font-weight: bold;")
        self.detail_panel.addWidget(self.answer_label)

        right_widget = QWidget()
        right_widget.setLayout(self.detail_panel)

        main_layout.addWidget(self.question_list, 2)
        main_layout.addWidget(right_widget, 3)

        self.setLayout(main_layout)

        self.populate_questions()

    def populate_questions(self):
        self.question_list.clear()

        for category, questions in self.bank.get("categories", {}).items():
            header = QListWidgetItem(f"[{category}]")
            header.setFlags(header.flags() & ~header.flags())
            self.question_list.addItem(header)

            for q in questions:
                item = QListWidgetItem(q["question"][:80])
                item.setData(1, q)
                self.question_list.addItem(item)

    def show_question(self, item):
        q = item.data(1)
        if not q:
            return

        self.q_label.setText(q["question"])

        for i, opt in enumerate(q["options"]):
            self.option_labels[i].setText(
                f"{chr(65+i)}. {opt}"
            )

        self.answer_label.setText(
            f"Correct Answer: {chr(65 + q['correct'])}"
        )

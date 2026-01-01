from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem, QLabel,
    QLineEdit, QPushButton, QComboBox,
    QMessageBox
)
from core.storage import load_bank, save_bank


class QuestionManager(QWidget):
    def __init__(self):
        super().__init__()
        self.bank = load_bank()
        self.current_question = None

        main = QVBoxLayout()

        # Top controls
        top = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search question...")
        self.search.textChanged.connect(self.refresh_list)

        self.category_filter = QComboBox()
        self.category_filter.addItem("All")
        self.category_filter.addItems(self.bank["categories"].keys())
        self.category_filter.currentTextChanged.connect(self.refresh_list)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_question)

        top.addWidget(self.search)
        top.addWidget(self.category_filter)
        top.addWidget(self.delete_btn)
        main.addLayout(top)

        # Body
        body = QHBoxLayout()

        self.list = QListWidget()
        self.list.itemClicked.connect(self.load_question)

        body.addWidget(self.list, 2)

        # Editor panel
        editor = QVBoxLayout()
        self.q_edit = QLineEdit()
        editor.addWidget(QLabel("Question"))
        editor.addWidget(self.q_edit)

        self.opt_edits = []
        for i in range(4):
            e = QLineEdit()
            editor.addWidget(QLabel(f"Option {chr(65+i)}"))
            editor.addWidget(e)
            self.opt_edits.append(e)

        self.correct = QComboBox()
        self.correct.addItems(["A", "B", "C", "D"])
        editor.addWidget(QLabel("Correct Option"))
        editor.addWidget(self.correct)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        editor.addWidget(self.save_btn)

        body.addLayout(editor, 3)
        main.addLayout(body)

        self.setLayout(main)
        self.refresh_list()

    def refresh_list(self):
        self.list.clear()
        text = self.search.text().lower()
        category = self.category_filter.currentText()

        for cat, questions in self.bank["categories"].items():
            if category != "All" and cat != category:
                continue

            for q in questions:
                if text and text not in q["question"].lower():
                    continue

                item = QListWidgetItem(q["question"][:80])
                item.setData(1, (cat, q))
                self.list.addItem(item)

    def load_question(self, item):
        cat, q = item.data(1)
        self.current_question = (cat, q)

        self.q_edit.setText(q["question"])
        for i, opt in enumerate(q["options"]):
            self.opt_edits[i].setText(opt)

        self.correct.setCurrentIndex(q["correct"])

    def save_changes(self):
        if not self.current_question:
            return

        _, q = self.current_question
        q["question"] = self.q_edit.text()
        q["options"] = [e.text() for e in self.opt_edits]
        q["correct"] = self.correct.currentIndex()

        save_bank(self.bank)
        QMessageBox.information(self, "Saved", "Question updated.")
        self.refresh_list()

    def delete_question(self):
        if not self.current_question:
            return

        cat, q = self.current_question
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Delete this question permanently?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.bank["categories"][cat].remove(q)
            save_bank(self.bank)
            self.current_question = None
            self.refresh_list()

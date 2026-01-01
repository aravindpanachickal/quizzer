from PyQt5.QtWidgets import (
    QMainWindow, QAction, QApplication
)
from ui.quiz_setup_dialog import QuizSetupDialog
from ui.question_editor import QuestionEditor
from ui.question_viewer import QuestionViewer
from ui.quiz_window import QuizWindow
from ui.question_manager import QuestionManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OMR Quiz Prep")
        self.resize(900, 600)

        menubar = self.menuBar()

        bank_menu = menubar.addMenu("Question Bank")
        quiz_menu = menubar.addMenu("Quiz")

        add_q = QAction("Add Question", self)
        start_quiz = QAction("Start Quiz", self)

        add_q.triggered.connect(self.open_editor)
        start_quiz.triggered.connect(self.open_quiz)

        bank_menu.addAction(add_q)
        quiz_menu.addAction(start_quiz)

        view_q = QAction("View Questions", self)
        view_q.triggered.connect(self.open_viewer)
        bank_menu.addAction(view_q)

    def open_editor(self):
        self.setCentralWidget(QuestionEditor())

    def open_quiz(self):
        dialog = QuizSetupDialog()

        if dialog.exec_():
            categories = dialog.get_selection()
            quiz = QuizWindow(categories)

            if not quiz.engine.has_questions():
                QMessageBox.warning(
                    self,
                    "No Questions",
                    "No questions available for this selection."
                )
                return

            self.setCentralWidget(quiz)
            
    def open_viewer(self):
        self.setCentralWidget(QuestionManager())



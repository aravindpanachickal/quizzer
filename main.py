import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.drive_backup import backup_to_drive

def on_exit():
    backup_to_drive("data/question_bank.json")

app = QApplication(sys.argv)
app.aboutToQuit.connect(on_exit)

window = MainWindow()
window.show()

sys.exit(app.exec_())

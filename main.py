import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow

# Import our Drive sync module
from core.drive_sync import download_json, upload_json

def main():
    # 1️⃣ Try to pull latest JSON from Drive
    try:
        success = download_json()
        if success:
            print("Question bank synced from Google Drive")
        else:
            print("No question bank found on Drive, using local file")
    except Exception as e:
        print("Failed to sync from Drive:", e)

    # 2️⃣ Start GUI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 3️⃣ Optional: auto-upload JSON on exit
    def on_exit():
        try:
            upload_json()
            print("Question bank uploaded to Drive")
        except Exception as e:
            print("Failed to upload JSON:", e)

    app.aboutToQuit.connect(on_exit)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


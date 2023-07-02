from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton
from PyQt5.QtCore import QThread

class ProgressBarThread(QThread):
    def __init__(self, progressbar):
        super().__init__()
        self.progressbar = progressbar

    def run(self):
        for i in range(101):
            self.progressbar.setValue(i)
            self.sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress Bar Example")
        self.setGeometry(300, 300, 400, 200)

        self.progressbar = QProgressBar(self)
        self.progressbar.setGeometry(30, 40, 340, 25)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(160, 100, 80, 30)
        self.start_button.clicked.connect(self.start_progressbar)

    def start_progressbar(self):
        thread = ProgressBarThread(self.progressbar)
        thread.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

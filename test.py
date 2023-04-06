
import sys
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow


class Communicate(QObject):
    closeApp = Signal()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.click)

        self.setWindowTitle('Emitting Signal')
        self.setGeometry(300, 300, 300, 200)
        self.show()
    
    def click(self):
        print('clicked')

    def mousePressEvent(self):
        self.c.closeApp.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
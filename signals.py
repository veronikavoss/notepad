
import sys
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication,QWidget,QMainWindow,QPlainTextEdit,QMenuBar



class FindAvailable(QObject):
    check = Signal()
    def __init__(self):
        super().__init__()

    def mousePressEvent(self,arg=None):
        self.check.emit()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Emitting Signal')
        self.menubar = QMenuBar(self)
        self.menubar.emit()
        self.setMenuBar(self.menubar)
        self.file_menu = self.menubar.addMenu('file')
        self.file_menu.addAction('find')
        
        self.text_edit = QPlainTextEdit(self)
        self.setCentralWidget(self.text_edit)
        
        self.findavailable = FindAvailable()
        self.findavailable.check.connect(self.click)
        
        self.show()
    
    def mousePressEvent(self,arg=None):
        self.findavailable.mousePressEvent()
    
    def click(self):
        print('clicked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
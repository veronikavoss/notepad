
import sys
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication,QWidget,QMainWindow,QPlainTextEdit,QMenuBar



class PasteAvailable(QObject):
    pasteAvailable = Signal()

class Communicate(QObject):
    closeApp = Signal()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.c = Communicate()
        # self.c.closeApp.connect(self.click)
        self.paste_available =  PasteAvailable()

        self.setWindowTitle('Emitting Signal')
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.addMenu('file')
        
        # self.cwidget = QWidget(self)
        self.text_edit = QPlainTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.paste_available.pasteAvailable.connect(self.click)
        self.show()
    
    def click(self):
        print('clicked')
        if self.text_edit.canPaste():
            print('paste')
        else:
            print('not paste')

    def mousePressEvent(self,arg=None):
        # self.c.closeApp.emit()
        self.paste_available.pasteAvailable.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
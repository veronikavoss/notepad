
# import sys
# from PySide6.QtCore import Signal, QObject
# from PySide6.QtWidgets import QApplication, QMainWindow


# class Communicate(QObject):
#     closeApp = Signal()

# class MyApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.c = Communicate()
#         self.c.closeApp.connect(self.click)

#         self.setWindowTitle('Emitting Signal')
#         self.setGeometry(300, 300, 300, 200)
#         self.show()
    
#     def click(self):
#         print('clicked')

#     def mousePressEvent(self):
#         self.c.closeApp.emit()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec())

from PySide6.QtWidgets import QApplication, QWidget,QTextEdit
from PySide6.QtGui import QClipboard
from PySide6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.clipboard = QApplication.clipboard()
        mimedata = self.clipboard.mimeData()
        print(mimedata.hasText())
        self.clipboard.selectionChanged.connect(self.on_selection_changed)
        self.textedit = QTextEdit(self)
        self.setWindowTitle('copy')
        
    def on_selection_changed(self):
        is_copy_available = False
        mimedata = self.clipboard.mimeData(mode=QClipboard.Selection)
        if mimedata.hasText():
            is_copy_available = True
        
        print(is_copy_available)

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()

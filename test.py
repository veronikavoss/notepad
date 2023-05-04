from PySide6.QtWidgets import QMainWindow,QPlainTextEdit,QApplication
from PySide6.QtGui import QTextDocument
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        self.text_edit = QPlainTextEdit(self)
        self.document = self.text_edit.document()
        self.setCentralWidget(self.text_edit)
    
    def count_text(self):
        text = self.text_edit.toPlainText()
        target_text = "Hello World!"
        count = text.count(target_text)
        print(f"{target_text} appears {count} times in the text.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
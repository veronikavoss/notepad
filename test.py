from PySide6.QtWidgets import QMainWindow, QApplication, QPlainTextEdit
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.textedit = QPlainTextEdit(self)
        self.textedit.setPlainText("Hello, world!")
        self.word_wrap_action = QAction('자동 줄 바꿈(W&)', self)
        self.word_wrap_action.setCheckable(True)
        self.word_wrap_action.setChecked(True)
        self.word_wrap_action.triggered.connect(self.toggle_word_wrap)
        self.addAction(self.word_wrap_action)
        self.setCentralWidget(self.textedit)

    def toggle_word_wrap(self, checked):
        wrap_mode = QPlainTextEdit.WidgetWidth if checked else QPlainTextEdit.NoWrap
        self.textedit.setWordWrapMode(wrap_mode)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

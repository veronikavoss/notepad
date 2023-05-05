from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QLineEdit, QWidget


class NumberLineEdit(QLineEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return:
            # 엔터 키 입력 시 focus 제거
            self.clearFocus()
        elif event.key() == Qt.Key_Backspace:
            # 백스페이스 키 입력 시 QLineEdit의 기본 동작 수행
            super().keyPressEvent(event)
        else:
            # 숫자만 입력 가능하도록 제한
            if event.text().isdigit():
                super().keyPressEvent(event)

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.lineedit = NumberLineEdit(self)
        self.lineedit.move(20, 20)
        self.lineedit.resize(200, 30)

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Number Line Edit')
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    app.exec_()

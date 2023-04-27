from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton,QVBoxLayout,QWidget
from PySide6.QtGui import QTextDocument,QTextCursor


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        qwidget = QWidget()
        self.setCentralWidget(qwidget)
        vertical_layout = QVBoxLayout(qwidget)

        # QTextEdit 위젯 생성 및 설정
        self.text_edit = QTextEdit(self)
        vertical_layout.addWidget(self.text_edit)

        # QPushButton 생성 및 설정
        self.button = QPushButton('Find Backward')
        self.button.clicked.connect(self.find_backward)
        vertical_layout.addWidget(self.button)
        self.setLayout(vertical_layout)

    def find_backward(self):
        # 검색 문자열과 검색 방향 옵션 설정
        text_to_find = 'example'
        flags = QTextDocument.FindBackward

        # 검색 수행
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        if not cursor.movePosition(QTextCursor.Previous, flags):
            return

        # 검색 결과 선택
        cursor.movePosition(QTextCursor.Next, flags)
        cursor.movePosition(QTextCursor.WordRight, flags)
        cursor.movePosition(QTextCursor.WordLeft, flags)
        cursor.select(QTextCursor.WordUnderCursor)

        # 검색 결과 표시
        self.text_edit.setTextCursor(cursor)

if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()

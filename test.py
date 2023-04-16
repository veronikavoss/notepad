from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QMessageBox

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")
        self.setGeometry(300, 300, 600, 400)

        # UI 위젯 생성
        self.text_edit = QTextEdit(self)
        self.find_line_edit = QLineEdit(self)
        self.find_button = QPushButton("Find", self)
        self.find_next_button = QPushButton("Find Next", self)
        self.find_previous_button = QPushButton("Find Previous", self)

        # 레이아웃 생성
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        sub_layout = QHBoxLayout()
        sub_layout.addWidget(QLabel("Find: "))
        sub_layout.addWidget(self.find_line_edit)
        sub_layout.addWidget(self.find_button)
        sub_layout.addWidget(self.find_next_button)
        sub_layout.addWidget(self.find_previous_button)
        main_layout.addLayout(sub_layout)
        main_layout.addWidget(self.text_edit)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 버튼 클릭 시 신호와 슬롯 연결
        self.find_button.clicked.connect(self.find_text)
        self.find_next_button.clicked.connect(self.find_next)
        self.find_previous_button.clicked.connect(self.find_previous)

    def find_text(self):
        # Find 버튼을 클릭하면, 텍스트 에디터에서 검색어를 찾습니다.
        text = self.text_edit.toPlainText()
        search_text = self.find_line_edit.text()
        index = text.find(search_text)
        if index == -1:
            # 검색어를 찾을 수 없으면 메시지 박스를 표시합니다.
            QMessageBox.information(self, "Information", "Cannot find '{}'."
                                            .format(search_text))
        else:
            # 검색어를 찾으면 해당 위치로 커서를 이동합니다.
            cursor = self.text_edit.textCursor()
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,len(search_text))
            self.text_edit.setTextCursor(cursor)

    def find_next(self):
        # Find Next 버튼을 클릭하면, 다음 검색 결과를 찾습니다.
        text = self.text_edit.toPlainText()
        search_text = self.find_line_edit.text()
        cursor = self.text_edit.textCursor()
        index = text.find(search_text, cursor.position() + 1)
        if index == -1:
            # 검색어를 찾을 수 없으면 메시지 박스를 표시합니다.
            QMessageBox.information(self, "Information", "Cannot find '{}'."
                                            .format(search_text))
        else:
            # 검색어를 찾으면 해당 위치로 커서를 이동합니다.
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,len(search_text))
            self.text_edit.setTextCursor(cursor)

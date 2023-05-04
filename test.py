from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PySide6.QtGui import QIntValidator

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # QLineEdit 위젯 생성
        self.lineedit = QLineEdit(self)

        # QIntValidator 생성
        validator = QIntValidator()

        # QLineEdit 위젯에 QIntValidator 설정
        self.lineedit.setValidator(validator)

        # 레이아웃 생성
        layout = QVBoxLayout()
        layout.addWidget(self.lineedit)

        # 윈도우에 레이아웃 설정
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

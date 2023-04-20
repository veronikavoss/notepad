from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QFont

app = QApplication([])
window = QMainWindow()
button = QPushButton("Click me!")
font = QFont()
font.setPointSize(20)  # 글자 크기를 20으로 설정
font.setBold(True)  # Bold 스타일로 설정
font.setItalic(True)  # Italic 스타일로 설정
font.setUnderline(True)  # Underline 스타일로 설정
font.setStrikeOut(True)  # Strikeout 스타일로 설정
font.setFamily("Helvetica")  # 폰트 패밀리를 Helvetica로 설정
font.setLetterSpacing(QFont.AbsoluteSpacing, 2)  # 글자 간격을 2px로 설정
font.setWordSpacing(5)  # 단어 간격을 5px로 설정
font.setCapitalization(QFont.AllUppercase)  # 글자를 모두 대문자로 설정
font.setKerning(True)  # 캐릭터 간격을 조정
font.setStyleStrategy(QFont.PreferAntialias)  # 안티 앨리어싱 적용
# font.setColor("blue")  # 글자색을 파란색으로 설정
button.setFont(font)
window.setCentralWidget(button)
window.show()
app.exec()
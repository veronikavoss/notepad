from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QLineEdit

app = QApplication()

# QLineEdit 생성
line_edit = QLineEdit()

# QPalette 생성
palette = QPalette()

# 선택된 항목 글자색 설정
palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255)) # 흰색으로 설정

# 선택된 항목이 비활성화될 때의 글자색 설정
palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0)) # 회색으로 설정

# QLineEdit의 palette 설정
line_edit.setPalette(palette)

# QLineEdit 표시
line_edit.show()

# 창을 비활성화하고 선택된 항목이 비활성화될 때의 글자색 표시
line_edit.setEnabled(True)

# 이벤트 루프 시작
app.exec()

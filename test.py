from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("안녕하세요!")

# 포맷 문자열을 사용하여 폰트 스타일 적용
font_family = "나눔고딕"
font_size = 18
font_style = "italic"
style_sheet = "font-family: {0}; font-size: {1}px; font-style: {2};".format(font_family, font_size, font_style)

label.setStyleSheet(style_sheet)

label.show()
app.exec()

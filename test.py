from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QScreen

app = QApplication()
desktop = QScreen()
screen_rect = desktop.geometry()
width, height = screen_rect.width(), screen_rect.height()
print(f"현재 화면 크기: {width} x {height}")

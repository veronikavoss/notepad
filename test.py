from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 메뉴 생성
        menubar = self.menuBar()
        menu=menubar.addMenu("File")

        # 메뉴 항목 생성
        action_new = QAction("New", self)
        action_open = QAction("Open", self)
        action_save = QAction("Save", self)

        # 메뉴에 항목 추가
        menu.addAction(action_new)
        menu.addAction(action_open)
        menu.addAction(action_save)

        # 시그널 연결
        menu.aboutToShow.connect(lambda:print('m'))
        menu.triggered.connect(self.onMenuTriggered)

    def onMenuTriggered(self, action):
        print(action.text() + " is selected.")

app = QApplication([])
window = MyWindow()
window.show()
app.exec()

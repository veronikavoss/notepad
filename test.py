from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListView, QLabel
import sys
from PySide6.QtGui import QGuiApplication, QListView

# QGuiApplication 클래스를 생성합니다.
app = QGuiApplication(sys.argv)

# ListView 위젯을 생성합니다.
listView = QListView()

# ListView 위젯에 모델을 설정합니다.
model = QStringListModel()
model.appendRow("Item 1")
model.appendRow("Item 2")
model.appendRow("Item 3")
listView.setModel(model)

# ListView 위젯을 화면에 표시합니다.
listView.show()

# ListView 위젯의 currentChanged() 시그널에 연결합니다.
def on_currentChanged(current_index):
  print(current_index)
listView.currentChanged.connect(on_currentChanged)
from PySide6.QtWidgets import QListView

list_view = QListView()
list_view.selectionModel().selectionChanged.connect(your_slot)

# QGuiApplication 종료
app.exec()

from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtWidgets import QApplication, QMainWindow, QListView

app = QApplication([])

# QMainWindow나 QDialog 등에 ListView가 있는 경우
window = QMainWindow()
list_view = QListView(window)
window.setCentralWidget(list_view)

# 아이템 데이터 생성
item_data = ["Item 1", "Item 2", "Item 3"]

# 아이템 모델 생성
model = QStringListModel(item_data)

# ListView에 모델 설정
list_view.setModel(model)

# 아이템 선택 이벤트 핸들러
def item_selected(index):
    selected_indexes = list_view.selectedIndexes()
    if selected_indexes:
        selected_index = selected_indexes[0]
        selected_text = model.data(selected_index, Qt.DisplayRole)
        print("Selected Item:", selected_text)

list_view.clicked.connect(item_selected)

window.show()
app.exec()

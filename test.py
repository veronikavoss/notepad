from PySide6.QtCore import Qt,QStringListModel
from PySide6.QtWidgets import QApplication, QListView

app = QApplication([])

# 문자열 리스트 생성
string_list = ["Item 1", "Item 2", "Item 3", "Item 4"]

# QStringListModel 생성 및 설정
model = QStringListModel()
model.setStringList(string_list)

# 리스트뷰에 모델 설정
list_view = QListView()
list_view.setModel(model)

# 특정 텍스트로 인덱스 찾기
search_text = "Item 3"
indexes = model.match(model.index(0), Qt.DisplayRole, search_text, -1, Qt.MatchExactly)
if indexes:
    index = indexes[0]
    print("Index found:", index.row())

app.exec()

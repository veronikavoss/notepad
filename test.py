from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QListView, QApplication

class HighlightDetectListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.selectionModel().selectionChanged.connect(self.handle_selection_changed)

    def handle_selection_changed(self, selected, deselected):
        for index in selected.indexes():
            if index.flags() & Qt.ItemIsSelected:
                print("Selected item:", index.data(Qt.DisplayRole))

if __name__ == '__main__':
    app = QApplication([])
    list_view = HighlightDetectListView()
    # 리스트뷰 설정 및 아이템 추가 등의 코드 작성
    list_view.show()
    app.exec()


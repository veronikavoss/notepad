from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListView

class FontListWidget(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)

        font_families = QFontDatabase.families()

        model = QStandardItemModel()
        self.setModel(model)

        for family in font_families:
            item = QStandardItem(family)
            item.setFont(QFont(family, 12))  # Apply the font
            model.appendRow(item)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Font List Example")

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        font_list = FontListWidget(self)

        layout.addWidget(font_list)

        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


import sys
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QUndoStack,QUndoCommand
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

class MyTextEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.undoStack = QUndoStack(self)
        self.undoStack.setUndoLimit(10) # 최대 10개의 undo 명령만 기억합니다.
        self.document().contentsChanged.connect(self.onChange)

    def onChange(self):
        # 컨텐츠가 변경되면 undoStack에 push합니다.
        self.undoStack.push(MyTextEditState(self.document()))

class MyTextEditState(QUndoCommand):
    def __init__(self, document):
        super().__init__()
        self.oldText = document.toPlainText()
        self.newText = None

    def redo(self):
        self.setText(self.newText)

    def undo(self):
        self.setText(self.oldText)

    def setText(self, text):
        self.newText = text
        self.document().setPlainText(text)

    def mergeWith(self, other):
        if not isinstance(other, MyTextEditState):
            return False
        if other.newText == self.oldText:
            self.newText = other.newText
            return True
        return False

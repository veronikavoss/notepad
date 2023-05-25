from PySide6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PySide6.QtCore import QEvent,Qt

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        self.font_lineedit = QLineEdit(self)
        self.font_lineedit.setText('1')
        self.font_style_lineedit = QLineEdit(self)
        self.font_style_lineedit.setText('2')
        self.font_size_lineedit = QLineEdit(self)
        self.font_size_lineedit.setText('3')
        
        layout.addWidget(self.font_lineedit)
        layout.addWidget(self.font_style_lineedit)
        layout.addWidget(self.font_size_lineedit)
        
        self.font_lineedit.installEventFilter(self)
        self.font_style_lineedit.installEventFilter(self)
        self.font_size_lineedit.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.font_lineedit and event.type() == QEvent.FocusOut:
            print("LineEdit lost focus")
        elif obj == self.font_lineedit and event.type() == QEvent.FocusIn:
            self.font_lineedit_focus_in = True
            print("font_lineedit_focus_in",self.font_lineedit_focus_in)
            self.font_style_lineedit.deselect()
            self.font_size_lineedit.deselect()
        
        if obj == self.font_style_lineedit and event.type() == QEvent.FocusOut:
            print("font_style_lineedit lost focus")
        elif obj == self.font_style_lineedit and event.type() == QEvent.FocusIn:
            self.font_style_lineedit_focus_in = True
            print("font_style_lineedit_focus_in",self.font_style_lineedit_focus_in)
            self.font_lineedit.deselect()
            self.font_size_lineedit.deselect()
        
        # lineedit mouse selection
        if obj == self.font_lineedit and event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.font_lineedit_focus_in:
                    self.font_lineedit.selectAll()
                    self.font_lineedit_focus_in = False
                    return True
        elif obj == self.font_style_lineedit and event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.font_style_lineedit_focus_in:
                    self.font_style_lineedit.selectAll()
                    self.font_style_lineedit_focus_in = False
                    return True
        # elif obj == self.font_size_lineedit and event.type() == QEvent.MouseButtonPress:
        #     if event.button() == Qt.LeftButton:
        #         if self.font_size_lineedit_focus_in:
        #             self.font_size_lineedit.selectAll()
        #             self.font_size_lineedit_focus_in = False
        #             return True
        
        return super().eventFilter(obj, event)

app = QApplication([])

widget = MyWidget()
widget.show()

app.exec()

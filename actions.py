from PySide6.QtWidgets import QFileDialog
import os

class SetActions:
    def new(self):
        pass
    
    def new_window(self):
        pass
    
    def open(self):
        title = self.windowTitle()
        self.file_name = QFileDialog.getOpenFileName(self)
        print('file_name',os.path.join(os.path.basename(self.file_name[0])))
        try:
            self.setWindowTitle(os.path.join(os.path.basename(self.file_name[0])) + ' - Windows 메모장')
            with open(self.file_name[0],'r',encoding='UTF8') as r:
                text = r.read()
            self.plain_text_edit.setPlainText(text)
            self.original_text = self.plain_text_edit.toPlainText()
            print(self.original_text)
        except:
            self.setWindowTitle(title)
    
    def save(self):
        self.file_name = QFileDialog.getSaveFileName(self)
        self.get_text = self.plain_text_edit.toPlainText()
        with open(self.file_name[0],'w',encoding='UTF8') as w:
            w.write(self.get_text)
            print(self.file_name[0])
        self.setWindowTitle(os.path.join(os.path.basename(self.file_name[0])) + ' - Windows 메모장')
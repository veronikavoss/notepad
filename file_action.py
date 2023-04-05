from PySide6.QtWidgets import QFileDialog
import os

class FileAction:
    def __init__(self,main,plain,name):
        self.main = main
        self.plain_text = plain
        self.file_name = name
    
    def new(self):
        pass
    
    def new_window(self):
        pass
    
    def open(self):
        self.file_name = QFileDialog.getOpenFileName(self.main)
        print('file_name',os.path.join(os.path.basename(self.file_name[0])))
        self.main.setWindowTitle(os.path.join(os.path.basename(self.file_name[0])) + ' - Windows 메모장')
        
        with open(self.file_name[0],'r',encoding='UTF8') as r:
            text = r.read()
        self.plain_text.setPlainText(text)
    
    def save(self):
        self.file_name = QFileDialog.getSaveFileName(self.main)
        self.get_text = self.plain_text.toPlainText()
        with open(self.file_name[0],'w',encoding='UTF8') as w:
            w.write(self.get_text)
            print(self.file_name[0])
        self.main.setWindowTitle(os.path.join(os.path.basename(self.file_name[0])) + ' - Windows 메모장')
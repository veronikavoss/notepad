from PySide6.QtWidgets import QFileDialog

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
        print('file_name',self.file_name[0])
        self.main.setWindowTitle(self.file_name[0] + ' - Windows 메모장')
        
        with open(self.file_name[0],'r',encoding='UTF8') as r:
            text = r.read()
            print(text)
        self.plain_text.setPlainText(text)
    
    def save(self):
        self.file_name = QFileDialog.getSaveFileName(self.main)
        print('file_name',self.file_name[0])
        with open(self.file_name[0],'w',encoding='UTF8') as w:
            text = w.w()
            print(text)
        self.plain_text.setPlainText(text)
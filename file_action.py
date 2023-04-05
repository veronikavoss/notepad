from PySide6.QtWidgets import QFileDialog

class FileAction:
    def __init__(self,main):
        # self.new()
        # self.new_window()
        self.main = main
    
    def open(self):
        file_name = QFileDialog.getOpenFileName(self.main)
        print('file_name',file_name[0])
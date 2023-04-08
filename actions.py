from PySide6.QtWidgets import QFileDialog,QMessageBox
import os

class SetActions:
    def new(self):
        self.plain_text_edit.clear()
    
    def new_window(self):
        self.save_messagebox()
    
    def open(self):
        self.previous_filename = self.windowTitle()
        if not self.modify:
            print(self.file_name)
            self.file_name = QFileDialog.getOpenFileName(self,'열기','',self.filter_option)[0]
            if self.file_name:
                try:
                    with open(self.file_name,'r',encoding='ansi') as r:
                        text = r.read()
                        self.original_text = text
                        r.close()
                except Exception as e:
                    print(e)
                    # self.setWindowTitle(self.previous_filename)
                else:
                    self.plain_text_edit.setPlainText(text)
            else:
                self.file_name = self.previous_filename
        else:
            self.save_messagebox()
    
    def save_messagebox(self):
        messagebox=QMessageBox()
        messagebox.setWindowTitle('메모장')
        messagebox.setText('변경 내용을 {}에 저장 하시겠습니까?'.format(
            os.path.basename(self.file_name) if self.file_name else '제목 없음'))
        messagebox.addButton('저장(S)',QMessageBox.YesRole)
        messagebox.addButton('저장 안 함(N)',QMessageBox.NoRole)
        messagebox.addButton('취소',QMessageBox.RejectRole)
        self.get_messagebox_button=messagebox.exec()
    
    def save(self):
        self.file_name = QFileDialog.getSaveFileName(self)
        self.get_text = self.plain_text_edit.toPlainText()
        with open(self.file_name[0],'w',encoding='UTF8') as w:
            w.write(self.get_text)
            print(self.file_name[0])
        self.setWindowTitle(os.path.join(os.path.basename(self.file_name[0])) + ' - Windows 메모장')
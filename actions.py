from PySide6.QtWidgets import QFileDialog,QMessageBox
import os

class SetActions:
    def new(self):
        if self.modify:
            self.save_messagebox()
        else:
            self.text_edit.clear()
    
    # def new_window(self,main_window):
    #     new_window = main_window
    #     self.windows.append(new_window)
    #     new_window.show()
    
    def open(self):
        if not self.previous_filename:
            self.previous_filename = self.windowTitle()
        if not self.modify:
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
                    self.text_edit.setPlainText(text)
                    self.previous_filename = self.file_name
                    print(self.previous_filename)
                    print(self.windowTitle())
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
        self.get_messagebox_button = messagebox.exec()
        self.set_messagebox_button()
    
    def set_messagebox_button(self):
        if self.get_messagebox_button == 0:
            if self.file_name == '제목 없음':
                print('save as')
                self.save_as()
            else:
                print('save')
                self.save()
        elif self.get_messagebox_button == 1:
            print('no')
        elif self.get_messagebox_button == 2:
            print('cancel')
    
    def save(self):
        print(self.file_name)
        if self.file_name == '제목 없음':
            self.save_as()
        else:
            if self.modify:
                try:
                    with open(self.file_name,'w',encoding='UTF8') as w:
                        w.write(self.text_edit.toPlainText())
                        w.close()
                except Exception as e:
                    print(e)
                else:
                    print(w)
                    self.original_text = self.text_edit.toPlainText()
                    self.checking_modify_document()
            else:
                return
    
    def save_as(self):
        if not self.previous_filename:
            self.previous_filename = self.windowTitle()
        self.file_name = QFileDialog.getSaveFileName(self,'다른 이름으로 저장','',self.filter_option)[0]
        if self.file_name:
            try:
                with open(self.file_name,'w',encoding='UTF8') as w:
                    w.write(self.text_edit.toPlainText())
                    
            except Exception as e:
                print(e)
            else:
                print(w)
                w.close()
                self.original_text = self.text_edit.toPlainText()
                self.checking_modify_document()
        else:
            self.file_name = self.previous_filename
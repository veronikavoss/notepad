from PySide6.QtWidgets import QFileDialog,QMessageBox
from PySide6.QtPrintSupport import QPageSetupDialog,QPrintDialog,QPrinter
from PySide6.QtGui import QIcon,QFont
import os,chardet

class SetActions:
    # file action
    def new(self):
        if self.modify:
            self.save_status = 'new'
            self.run_messagebox_button()
            print(self.save_status)
        else:
            if self.file_name != '제목 없음':
                self.save_status = 'new'
                self.file_name = '제목 없음'
                self.text_edit.clear()
                self.original_text = self.text_edit.toPlainText()
                self.checking_modify_document()
                print(self.save_status)
    
    def open(self):
        if not self.previous_filename:
            self.previous_filename = self.windowTitle()
        if not self.modify or self.save_status == 'not save':
            self.save_status = 'open'
            self.file_name = QFileDialog.getOpenFileName(self,'열기','',self.filter_option)[0]
            print(self.file_name)
            if self.file_name:
                # auto encoding search
                with open(self.file_name,'rb') as r:
                    rawdata = r.read()
                    result = chardet.detect(rawdata)
                    self.encoding = result["encoding"]
                    print(self.encoding)
                try:
                    with open(self.file_name,'r',encoding=self.encoding) as r:
                        text = r.read()
                        self.original_text = text
                        r.close()
                except Exception as e:
                    print(e)
                else:
                    self.text_edit.setPlainText(text)
                    self.previous_filename = self.file_name
                    self.save_status = 'opened'
                    self.encoding_label.setText(self.encoding.upper())
                    print(self.save_status)
            else:
                self.save_status = 'open canceled'
                self.file_name = self.previous_filename
                print(self.save_status)
        else:
            self.save_status = 'open'
            print(self.save_status)
            self.run_messagebox_button()
    
    def save(self):
        if self.file_name == '제목 없음':
            self.save_as()
        else:
            if self.modify:
                try:
                    self.save_status = 'save'
                    with open(self.file_name,'w',encoding='UTF8') as w:
                        w.write(self.text_edit.toPlainText())
                        w.close()
                        print(self.save_status)
                except Exception as e:
                    print(e)
                else:
                    self.original_text = self.text_edit.toPlainText()
                    self.checking_modify_document()
                    self.save_status = 'saved'
                    print(self.save_status)
            else:
                return
    
    def save_as(self):
        if not self.previous_filename:
            self.previous_filename = self.windowTitle()
        self.file_name = QFileDialog.getSaveFileName(self,'다른 이름으로 저장',f'{self.file_name}',self.filter_option)[0]
        if self.file_name:
            try:
                self.save_status = 'save as'
                with open(self.file_name,'w',encoding='UTF8') as w:
                    w.write(self.text_edit.toPlainText())
                    w.close()
            except Exception as e:
                print(e)
            else:
                self.original_text = self.text_edit.toPlainText()
                self.checking_modify_document()
                self.save_status = 'saved as'
                print(self.save_status)
        else:
            self.save_status = 'not saved as'
            self.file_name = self.previous_filename
            if self.closed:
                self.close_event.ignore()
            print(self.save_status)
    
    def set_save_messagebox(self):
        font = QFont()
        font.setPointSize(12)
        messagebox=QMessageBox()
        messagebox.setFont(font)
        messagebox.setWindowTitle('메모장')
        messagebox.setText(f'변경 내용을 {self.file_name}에 저장 하시겠습니까?')
        messagebox.setStyleSheet('color: #003399')
        messagebox.addButton('저장(S)',QMessageBox.YesRole).setStyleSheet('color: black')
        messagebox.addButton('저장 안 함(N)',QMessageBox.NoRole).setStyleSheet('color: black')
        messagebox.addButton('취소',QMessageBox.RejectRole).setStyleSheet('color: black')
        self.get_messagebox_button = messagebox.exec()
    
    def run_messagebox_button(self):
        self.set_save_messagebox()
        
        if self.save_status == 'new':
            print(self.save_status)
            if self.get_messagebox_button == 0:
                print(self.file_name)
                if self.file_name == '제목 없음':
                    print('save as')
                    self.save_as()
                    self.new()
                else:
                    print('save')
                    self.save()
                    self.new()
            elif self.get_messagebox_button == 1:
                self.text_edit.clear()
                self.original_text = self.text_edit.toPlainText()
                self.file_name = '제목 없음'
                self.checking_modify_document()
            elif self.get_messagebox_button == 2:
                self.save_status = 'new canceled'
        
        elif self.save_status == 'open':
            print(self.save_status)
            if self.get_messagebox_button == 0:
                print(self.file_name)
                if self.file_name == '제목 없음':
                    print(self.save_status)
                    self.save_as()
                    self.open()
                else:
                    print(self.save_status)
                    self.save()
                    self.open()
            elif self.get_messagebox_button == 1:
                self.save_status = 'not save'
                print(self.save_status)
                self.open()
            elif self.get_messagebox_button == 2:
                self.save_status = 'open canceled'
                print(self.save_status)
        
        elif self.save_status == 'close':
            print(self.save_status)
            
            if self.get_messagebox_button == 0:
                print(self.file_name)
                if self.file_name == '제목 없음':
                    print(self.save_status)
                    self.save_as()
                else:
                    print(self.save_status)
                    self.save()
            elif self.get_messagebox_button == 1:
                self.save_status = 'closed'
                print(self.save_status)
            elif self.get_messagebox_button == 2:
                self.save_status = 'close canceled'
                self.close_event.ignore()
                print(self.save_status)
    
    def setup_page(self):
        printer = QPrinter()
        page_setup_dialog = QPageSetupDialog(printer)
        if page_setup_dialog.exec() == QPageSetupDialog.Accepted:
            printer.setPageSize(page_setup_dialog.pageSetup().pageSize())
            printer.setOrientation(page_setup_dialog.pageSetup().orientation())
            printer.setPageMargins(page_setup_dialog.pageMargins())
    
    def setup_printer(self):
        if QPrintDialog().exec():
            self.text_edit.print(QPrintDialog.printer())
    
    # edit action
    def delete(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return
        cursor.removeSelectedText()
    
    # slot
    def show_edit_menu(self):
        self.paste_action.setEnabled(self.text_edit.canPaste())
        
        if self.text_edit.toPlainText():
            self.find_action.setEnabled(True)
            self.find_next_action.setEnabled(True)
            self.find_previous_action.setEnabled(True)
        else:
            self.find_action.setEnabled(False)
            self.find_next_action.setEnabled(False)
            self.find_previous_action.setEnabled(False)
    
    # def undo_available(self,available):
    #     self.undo_action.setEnabled(available)
    
    # def redo_available(self,available):
    #     self.redo_action.setEnabled(available)
    
    def select_available(self,yes):
        self.cut_action.setEnabled(yes)
        self.copy_action.setEnabled(yes)
        self.delete_action.setEnabled(yes)
    
    def line_edit_text_changer(self,text):
        if text:
            self.find_next_button.setEnabled(True)
        else:
            self.find_next_button.setEnabled(False)
    
    # view action
    def set_zoom_in(self):
        font = self.text_edit.font()
        zoom_value = 1.1
        font_size = font.pointSizeF() * zoom_value  # 확대 비율 설정
        font.setPointSizeF(font_size)
        self.text_edit.setFont(font)
        self.default_zoom += 10
        self.zoom_label.setText(f'{self.default_zoom}%')
    
    def set_zoom_out(self):
        font = self.text_edit.font()
        zoom_value = 0.9
        font_size = font.pointSizeF() * zoom_value  # 축소 비율 설정
        font.setPointSizeF(font_size)
        self.text_edit.setFont(font)
        self.default_zoom -= 10
        self.zoom_label.setText(f'{self.default_zoom}%')
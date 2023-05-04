from PySide6.QtWidgets import QFileDialog,QMessageBox
from PySide6.QtWidgets import (
    QGridLayout,QDialog,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,
    QCheckBox,QRadioButton,QGroupBox,QMessageBox)
from PySide6.QtGui import QFont,QTextDocument,QTextCursor
from PySide6.QtPrintSupport import QPageSetupDialog,QPrintDialog,QPrinter
from PySide6.QtGui import QIcon,QFont
import os,chardet,json

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

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
    def set_undo_action(self):
        self.text_edit.undo()
        if self.find_status == 'replace':
            self.text_edit.selectAll()
        self.find_status = ''
    
    def delete(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return
        cursor.removeSelectedText()
    
    def set_find_action(self):
        # init
        self.find_status = 'find'
        self.find_next_action_isrun = True
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        
        # ui
        self.find_window = QDialog(self)
        self.find_window.setWindowTitle('찾기')
        self.find_window.setFixedSize(392,156)
        
        # layout
        grid_layout = QGridLayout(self.find_window)
        horizon_lineedit_layout = QHBoxLayout()
        vertical_button_layout = QVBoxLayout()
        vertical_checkbox_layout = QVBoxLayout()
        direction_groupbox = QGroupBox('방향')
        direction_groupbox.setMaximumHeight(60)
        horizon_direction_layout = QHBoxLayout()
        
        # widget
        label = QLabel('찾을 내용 ')
        self.find_line_edit = QLineEdit()
        self.find_line_edit.setPalette(self.palette)
        if selected_text:
            self.keyword_to_find = selected_text
        else:
            self.keyword_to_find = self.config['find_keyword']
        self.find_line_edit.setText(self.keyword_to_find)
        self.find_line_edit.selectAll()
        self.find_line_edit.textChanged.connect(self.line_edit_text_changer)
        
        self.find_next_button = QPushButton('다음 찾기(&F)')
        if self.find_line_edit.text():
            self.find_next_button.setEnabled(True)
        else:
            self.find_next_button.setEnabled(False)
        self.find_next_button.clicked.connect(self.set_find_next_button)
        
        find_cancel_button = QPushButton('취소')
        find_cancel_button.clicked.connect(self.set_find_cancel_button)
        
        self.radiobox_up = QRadioButton('위로(&U)')
        self.radiobox_up.setMaximumWidth(60)
        self.radiobox_down = QRadioButton('아래로(&D)')
        if self.config['find_upndown'] == 'down':
            self.radiobox_down.setChecked(True)
        else:
            self.radiobox_up.setChecked(True)
        
        self.case_sensitivity_checkbox = QCheckBox('대/소문자 구분(&C)')
        if self.config['case_sensitivity'] == 'no':
            self.case_sensitivity_checkbox.setChecked(False)
        else:
            self.case_sensitivity_checkbox.setChecked(True)
        
        self.wrap_around_checkbox = QCheckBox('주위에 배치(&R)')
        if self.config['wrap_around'] == 'no':
            self.wrap_around_checkbox.setChecked(False)
        else:
            self.wrap_around_checkbox.setChecked(True)
        
        # add widget
        horizon_lineedit_layout.addWidget(label)
        horizon_lineedit_layout.addWidget(self.find_line_edit)
        grid_layout.addLayout(horizon_lineedit_layout,0,0,1,3)
        
        grid_layout.addWidget(self.find_next_button,0,4)
        grid_layout.addWidget(find_cancel_button,1,4)
        
        vertical_checkbox_layout.addWidget(self.case_sensitivity_checkbox)
        vertical_checkbox_layout.addWidget(self.wrap_around_checkbox)
        grid_layout.addLayout(vertical_checkbox_layout,2,0)
        
        horizon_direction_layout.addWidget(self.radiobox_up)
        horizon_direction_layout.addWidget(self.radiobox_down)
        direction_groupbox.setLayout(horizon_direction_layout)
        grid_layout.addWidget(direction_groupbox,1,1,2,1)
        
        # self.find_window.setLayout(grid_layout)
        
        # self.find_window.setAttribute(Qt.WA_DeleteOnClose)
        self.find_window.closeEvent = self.set_find_cancel_button
        self.find_window.show()
    
    def set_find_next_button(self,replace=None):
        document = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        cursor_position = cursor.position()
        self.keyword_to_find = self.find_line_edit.text()
        
        if self.find_status == 'find':
            self.when_find(document,cursor,cursor_position,self.keyword_to_find)
        elif self.find_status == 'replace':
            self.when_replace(document,cursor,cursor_position,self.keyword_to_find,replace)
    
    def when_find(self,document,cursor,cursor_position,keyword_to_find):
        if self.radiobox_down.isChecked():
            if self.case_sensitivity_checkbox.isChecked():
                flag = QTextDocument.FindCaseSensitively
                cursor = document.find(keyword_to_find,cursor_position,flag)
            else:
                cursor = document.find(keyword_to_find,cursor_position)
        else:
            if cursor.selectedText():
                start_position = cursor_position - len(keyword_to_find)
            else:
                start_position = cursor_position
            
            if self.case_sensitivity_checkbox.isChecked():
                flag = QTextDocument.FindBackward | QTextDocument.FindCaseSensitively
                cursor = document.find(keyword_to_find,start_position,flag)
            else:
                flag = QTextDocument.FindBackward
                cursor = document.find(keyword_to_find,start_position,flag)
        
        if not cursor.isNull():
            self.text_edit.setTextCursor(cursor)
        else:
            if self.wrap_around_checkbox.isChecked():
                if self.radiobox_down.isChecked():
                    if self.case_sensitivity_checkbox.isChecked():
                        flag = QTextDocument.FindCaseSensitively
                        cursor = document.find(keyword_to_find,0,flag)
                    else:
                        cursor = document.find(keyword_to_find,0)
                else:
                    end_index = document.characterCount() - 1
                    if end_index != -1:
                        if self.case_sensitivity_checkbox.isChecked():
                            flag = QTextDocument.FindBackward | QTextDocument.FindCaseSensitively
                            cursor = document.find(keyword_to_find,end_index,flag)
                        else:
                            flag = QTextDocument.FindBackward
                    cursor = document.find(keyword_to_find,end_index,flag)
                
                self.text_edit.setTextCursor(cursor)
            else:
                QMessageBox.information(self, '메모장', f'"{keyword_to_find}"을(를) 찾을 수 없습니다.')
    
    def when_replace(self,document,cursor,cursor_position,keyword_to_find,replace):
        if self.case_sensitivity_checkbox.isChecked():
            flag = QTextDocument.FindCaseSensitively
            cursor = document.find(keyword_to_find,cursor_position,flag)
        else:
            cursor = document.find(keyword_to_find,cursor_position)
        
        if not cursor.isNull():
            print(1)
            self.text_edit.setTextCursor(cursor)
        else:
            print(0)
            if self.wrap_around_checkbox.isChecked():
                if self.case_sensitivity_checkbox.isChecked():
                    flag = QTextDocument.FindCaseSensitively
                    cursor = document.find(keyword_to_find,0,flag)
                else:
                    cursor = document.find(keyword_to_find,0)
                
                self.text_edit.setTextCursor(cursor)
                
                if not self.text_edit.textCursor().selectedText():
                    flag = QTextDocument.FindBackward
                    cursor = document.find(self.keyword_to_replace,cursor_position,flag)
                    self.text_edit.setTextCursor(cursor)
                    QMessageBox.information(self, '메모장', f'"{keyword_to_find}"을(를) 찾을 수 없습니다.')
            else:
                if replace:
                    flag = QTextDocument.FindBackward
                    cursor = document.find(self.keyword_to_replace,cursor_position,flag)
                    self.text_edit.setTextCursor(cursor)
                    QMessageBox.information(self, '메모장', f'"{keyword_to_find}"을(를) 찾을 수 없습니다.')
                else:
                    QMessageBox.information(self, '메모장', f'"{keyword_to_find}"을(를) 찾을 수 없습니다.')
    
    def set_find_next_action(self):
        self.config['find_upndown'] = 'down'
        if self.find_next_action_isrun:
            self.set_find_next_button()
        else:
            self.set_find_action()
    
    def set_find_previous_action(self):
        self.config['find_upndown'] = 'up'
        if self.find_next_action_isrun:
            self.set_find_next_button()
        else:
            self.set_find_action()
    
    def set_replace_action(self):
        # init
        self.find_status = 'replace'
        self.find_next_action_isrun = True
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        
        # ui
        self.replace_window = QDialog(self)
        self.replace_window.setWindowTitle('바꾸기')
        self.replace_window.setFixedSize(388,198)
        
        # layout
        grid_layout = QGridLayout(self.replace_window)
        
        # widget
        find_label = QLabel('찾을 내용(N):')
        self.find_line_edit = QLineEdit()
        self.find_line_edit.setPalette(self.palette)
        if selected_text:
            self.keyword_to_find = selected_text
        else:
            self.keyword_to_find = self.config['find_keyword']
        self.find_line_edit.setText(self.keyword_to_find)
        self.find_line_edit.selectAll()
        self.find_line_edit.textChanged.connect(self.line_edit_text_changer)
        
        replace_label = QLabel('바꿀 내용(P):')
        self.replace_line_edit = QLineEdit()
        self.replace_line_edit.setPalette(self.palette)
        self.keyword_to_replace = self.config['replace_keyword']
        self.replace_line_edit.setText(self.keyword_to_replace)
        
        self.find_next_button = QPushButton('다음 찾기(&F)')
        if self.find_line_edit.text():
            self.find_next_button.setEnabled(True)
        else:
            self.find_next_button.setEnabled(False)
        self.find_next_button.clicked.connect(self.set_find_next_button)
        
        self.replace_button = QPushButton('바꾸기(&R)')
        self.replace_button.clicked.connect(self.set_replace_button)
        
        self.replace_all_button = QPushButton('모두 바꾸기(&A)')
        self.replace_all_button.clicked.connect(self.set_replace_all_button)
        
        find_cancel_button = QPushButton('취소')
        find_cancel_button.clicked.connect(self.set_find_cancel_button)
        
        self.case_sensitivity_checkbox = QCheckBox('대/소문자 구분(&C)')
        if self.config['case_sensitivity'] == 'no':
            self.case_sensitivity_checkbox.setChecked(False)
        else:
            self.case_sensitivity_checkbox.setChecked(True)
        
        self.wrap_around_checkbox = QCheckBox('주위에 배치(&R)')
        if self.config['wrap_around'] == 'no':
            self.wrap_around_checkbox.setChecked(False)
        else:
            self.wrap_around_checkbox.setChecked(True)
        
        # add widget
        grid_layout.addWidget(find_label,0,0)
        grid_layout.addWidget(self.find_line_edit,0,1,1,3)
        grid_layout.addWidget(replace_label,1,0)
        grid_layout.addWidget(self.replace_line_edit,1,1,1,3)
        
        grid_layout.addWidget(self.find_next_button,0,4)
        grid_layout.addWidget(self.replace_button,1,4)
        grid_layout.addWidget(self.replace_all_button,2,4)
        grid_layout.addWidget(find_cancel_button,3,4)
        
        grid_layout.addWidget(self.case_sensitivity_checkbox,3,0,1,2)
        grid_layout.addWidget(self.wrap_around_checkbox,4,0,1,2)
        
        # self.replace_window.setAttribute(Qt.WA_DeleteOnClose)
        self.replace_window.closeEvent = self.set_find_cancel_button
        self.replace_window.show()
    
    def set_replace_button(self):
        replace = None
        cursor = self.text_edit.textCursor()
        self.keyword_to_find = self.find_line_edit.text()
        self.keyword_to_replace = self.replace_line_edit.text()
        if cursor.selectedText():
            if cursor.selectedText() == self.keyword_to_find:
                cursor.insertText(self.keyword_to_replace)
                self.set_find_next_button(replace=True)
            else:
                if not self.case_sensitivity_checkbox.isChecked():
                    cursor.insertText(self.keyword_to_replace)
                    self.set_find_next_button(replace=True)
                else:
                    self.set_find_next_button(replace=False)
        else:
            self.set_find_next_button(replace=False)
    
    def set_replace_all_button(self):
        text = self.text_edit.toPlainText()
        self.find_keyword = self.find_line_edit.text()
        self.replace_keyword = self.replace_line_edit.text()
        new_text = text.replace(self.find_keyword, self.replace_keyword)
        
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()
        cursor.insertText(new_text)
        cursor.endEditBlock()
    
    def set_find_cancel_button(self,event):
        
        self.config['find_keyword'] = self.find_line_edit.text()
        if not self.find_line_edit.text():
            self.find_next_action_isrun = False
        
        self.config['replace_keyword'] = self.replace_line_edit.text()
        
        if self.find_status == 'find':
            if self.radiobox_down.isChecked():
                self.config['find_upndown'] = 'down'
            else:
                self.config['find_upndown'] = 'up'
        
        if self.case_sensitivity_checkbox.isChecked():
            self.config['case_sensitivity'] = 'yes'
        else:
            self.config['case_sensitivity'] = 'no'
        
        if self.wrap_around_checkbox.isChecked():
            self.config['wrap_around'] = 'yes'
        else:
            self.config['wrap_around'] = 'no'
        
        with open(str(os.path.join(CURRENT_PATH,'config.json')),'w') as w:
            json.dump(self.config,w,indent=4)
        
        if self.find_status == 'find':
            self.find_window.close()
        elif self.find_status == 'replace':
            self.replace_window.close()
    
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
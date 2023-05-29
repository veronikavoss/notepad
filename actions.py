from PySide6.QtWidgets import (
    QApplication,QMainWindow,QFrame,QPlainTextEdit,QMenuBar,QMenu,QStatusBar,
    QGridLayout,QDialog,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QCheckBox,QRadioButton,
    QGroupBox,QMessageBox,QDialogButtonBox,QListView,QComboBox,QToolTip,QFileDialog,QAbstractItemView)

from PySide6.QtGui import (
    QFont,QTextDocument,QTextCursor,QIntValidator,QKeyEvent,QKeySequence,QTextOption,
    QAction,QIcon,QColor,QPalette,QDesktopServices,QFontDatabase,QStandardItemModel,QStandardItem)

from PySide6.QtCore import Qt,QPoint,QDateTime,QTime,QUrl,QStringListModel,QSize,QItemSelectionModel,QEvent,QLocale

from PySide6.QtPrintSupport import QPageSetupDialog,QPrintDialog,QPrinter

import sys,os,chardet,json

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
        self.find_list_lineedit = QLineEdit()
        self.find_list_lineedit.setMaxLength(128)
        self.find_list_lineedit.setPalette(self.palette)
        if selected_text:
            self.keyword_to_find = selected_text
        else:
            self.keyword_to_find = self.config['find_keyword']
        self.find_list_lineedit.setText(self.keyword_to_find)
        self.find_list_lineedit.selectAll()
        self.find_list_lineedit.textChanged.connect(self.line_edit_text_changer)
        
        self.find_next_button = QPushButton('다음 찾기(&F)')
        if self.find_list_lineedit.text():
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
        horizon_lineedit_layout.addWidget(self.find_list_lineedit)
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
        self.keyword_to_find = self.find_list_lineedit.text()
        
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
                if self.keyword_to_find in self.text_edit.toPlainText():
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
        self.find_list_lineedit = QLineEdit()
        self.find_list_lineedit.setPalette(self.palette)
        if selected_text:
            self.keyword_to_find = selected_text
        else:
            self.keyword_to_find = self.config['find_keyword']
        self.find_list_lineedit.setText(self.keyword_to_find)
        self.find_list_lineedit.selectAll()
        self.find_list_lineedit.textChanged.connect(self.line_edit_text_changer)
        
        replace_label = QLabel('바꿀 내용(P):')
        self.replace_line_edit = QLineEdit()
        self.replace_line_edit.setPalette(self.palette)
        self.keyword_to_replace = self.config['replace_keyword']
        self.replace_line_edit.setText(self.keyword_to_replace)
        
        self.find_next_button = QPushButton('다음 찾기(&F)')
        if self.find_list_lineedit.text():
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
        grid_layout.addWidget(self.find_list_lineedit,0,1,1,3)
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
        self.keyword_to_find = self.find_list_lineedit.text()
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
        self.find_keyword = self.find_list_lineedit.text()
        self.replace_keyword = self.replace_line_edit.text()
        new_text = text.replace(self.find_keyword, self.replace_keyword)
        
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()
        cursor.insertText(new_text)
        cursor.endEditBlock()
    
    def set_find_cancel_button(self,event):
        self.config['find_keyword'] = self.find_list_lineedit.text()
        if not self.find_list_lineedit.text():
            self.find_next_action_isrun = False
        
        if self.find_status == 'replace':
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
    
    def set_go_to_action(self):
        self.go_to_window = QDialog(self)
        self.go_to_window.setWindowTitle('줄 이동')
        self.go_to_window.setFixedSize(234,134)
        self.go_to_window.setModal(True)
        
        label = QLabel('줄 번호(L):')
        label.setAlignment(Qt.AlignTop)
        label.setMaximumHeight(20)
        
        self.go_to_lineedit = QLineEdit()
        self.go_to_lineedit.setMaximumHeight(30)
        self.go_to_lineedit.setText(str(self.go_to_line_number))
        self.go_to_lineedit.selectAll()
        self.go_to_lineedit.keyPressEvent = self.checking_modify_go_to_line
        
        go_to_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        go_to_button_box.accepted.connect(self.go_to_window.accept)
        go_to_button_box.rejected.connect(self.go_to_window.reject)
        
        self.go_to_button = go_to_button_box.button(QDialogButtonBox.Ok)
        self.go_to_button.setText('이동')
        self.go_to_button.clicked.connect(self.set_go_to_button)
        
        self.go_to_cancel_button = go_to_button_box.button(QDialogButtonBox.Cancel)
        self.go_to_cancel_button.setText('취소')
        
        go_to_layout = QVBoxLayout()
        go_to_layout.addWidget(label)
        go_to_layout.addWidget(self.go_to_lineedit)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(go_to_button_box)
        go_to_layout.addLayout(button_layout)
        
        self.go_to_window.setLayout(go_to_layout)
        self.go_to_window.show()
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return:
            # 엔터 키 입력 시 focus 제거
            self.clearFocus()
        elif event.key() == Qt.Key_Backspace:
            # 백스페이스 키 입력 시 QLineEdit의 기본 동작 수행
            super().keyPressEvent(event)
        else:
            # 숫자만 입력 가능하도록 제한
            if event.text().isdigit():
                super().keyPressEvent(event)
    
    def checking_modify_go_to_line(self, event: QKeyEvent):
        key = event.key()
        key_name = QKeySequence(key).toString()
        isdigit = key_name.isdigit()
        validator = QIntValidator()
        keys = [
            Qt.Key_Backspace,Qt.Key_Left,Qt.Key_Right,Qt.Key_Delete,Qt.Key_Home,Qt.Key_End,
            Qt.Key_A,Qt.Key_Control,Qt.Key_Shift]
        
        for key in keys:
            if event.key() == key:
                QLineEdit.keyPressEvent(self.go_to_lineedit, event)
                QToolTip.hideText()
        
        if event.key() == Qt.Key_Escape:
            QLineEdit.keyPressEvent(self.go_to_lineedit, event)
            self.go_to_window.close()
        elif event.key() == Qt.Key_Return:
            QLineEdit.keyPressEvent(self.go_to_lineedit, event)
            self.go_to_button.click()
        elif isdigit:
            QLineEdit.keyPressEvent(self.go_to_lineedit, event)
            QToolTip.hideText()
        else:
            if event.key() not in keys:
                self.go_to_lineedit.setValidator(validator)
                QToolTip.showText(self.go_to_lineedit.mapToGlobal(QPoint(0, 0)), "허용되지 않는 문자\n여기에는 숫자만 입력할 수 있습니다.")
        event.accept()
    
    def set_go_to_button(self):
        # init
        go_to_line_number = self.go_to_lineedit.text()
        text_edit = self.text_edit
        cursor = text_edit.textCursor()
        all_line_number = text_edit.document().blockCount()
        
        if  int(go_to_line_number) < 1 or int(go_to_line_number) > all_line_number:
            messagebox = QMessageBox(self.go_to_window)
            messagebox.setWindowTitle('메모장 - 줄 이동')
            messagebox.setText('줄 번호가 전체 줄 수를 넘습니다.')
            messagebox.show()
        else:
            cursor.setPosition(text_edit.document().findBlockByLineNumber(int(go_to_line_number)-1).position())
            text_edit.setTextCursor(cursor)
            self.go_to_line_number = self.go_to_lineedit.text()
    
    def set_time_data_action(self):
        now = QDateTime.currentDateTime()
        date = now.date().toString(Qt.ISODate)
        time = QTime.currentTime()
        hour = QTime.currentTime().hour()
        minute = time.minute()
        if hour < 12:
            ampm = '오전'
        else:
            ampm = '오후'
            hour = hour-12
        time_date = f'{ampm} {hour}:{minute} {date}'
        
        self.text_edit.insertPlainText(time_date)
    
    # edit slot
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
        
        self.go_to_action.setDisabled(self.word_wrap_action.isChecked())
    
    def select_available(self,yes):
        self.cut_action.setEnabled(yes)
        self.copy_action.setEnabled(yes)
        self.delete_action.setEnabled(yes)
    
    def line_edit_text_changer(self,text):
        if text:
            self.find_next_button.setEnabled(True)
        else:
            self.find_next_button.setEnabled(False)
    
    # format action
    def set_word_wrap_action(self, checked):
        wrap_mode = QTextOption.WrapAtWordBoundaryOrAnywhere if checked else QTextOption.NoWrap
        self.text_edit.setWordWrapMode(wrap_mode)
    
    def set_font(self):
        font_window = QDialog(self)
        font_window.setModal(True)
        font_window.setWindowTitle('글꼴')
        font_window.setFixedSize(404,486)
        self.current_font = self.config['font_family']['font']
        self.current_font_style = self.config['font_family']['style']
        self.current_font_size = self.config['font_family']['size']
        self.font_lineedit_focus_in = None
        self.font_style_lineedit_focus_in = None
        self.font_size_lineedit_focus_in = None
        
        # widget settings
        font_label = QLabel('글꼴(F):') # label
        self.font_lineedit = QLineEdit() # lineedit
        self.font_list = QListView() # list
        self.set_font_widget(font_label, self.font_lineedit, self.font_list, 160)
        self.font_list_model = QStandardItemModel()
        self.font_list.setModel(self.font_list_model)
        self.font_list_selectionmodel = self.font_list.selectionModel()
        
        font_script_label = QLabel('스크립트(R):')
        self.font_script_combobox = QComboBox()
        
        self.font_list_selectionmodel.selectionChanged.connect(self.set_font_list_item_selected)
        
        font_style_label = QLabel('글꼴 스타일(Y):')
        self.font_style_lineedit = QLineEdit()
        self.font_style_list = QListView()
        self.set_font_widget(font_style_label, self.font_style_lineedit, self.font_style_list, 120)
        self.font_style_list_model = QStandardItemModel()
        self.font_style_list.setModel(self.font_style_list_model)
        self.font_style_list_selectionmodel = self.font_style_list.selectionModel()
        
        font_size_label = QLabel('크기(S):')
        self.font_size_lineedit = QLineEdit()
        self.font_size_list = QListView()
        self.set_font_widget(font_size_label, self.font_size_lineedit, self.font_size_list, 60)
        self.font_size_list_model = QStringListModel()
        self.font_size_list.setModel(self.font_size_list_model)
        self.font_size_list_selectionmodel = self.font_size_list.selectionModel()
        
        self.set_font_list()
        
        font_preview_groupbox = QGroupBox('보기')
        font_preview_groupbox.setMaximumHeight(100)
        self.font_preview_label = QLabel()
        self.font_preview_label.setMargin(5)
        self.font_preview_label.setText('AaBbYyZz')
        font = self.config['font_family']['font']
        style = self.config['font_family']['style']
        size = self.config['font_family']['size']
        self.font_preview_label.setFont(self.set_font_style(font,style,size))
        self.font_preview_label.setAlignment(Qt.AlignCenter)
        font_preview_groupbox_layout = QVBoxLayout(font_preview_groupbox)
        font_preview_groupbox_layout.addWidget(self.font_preview_label)
        
        show_more_fonts_label = QLabel()
        show_more_fonts_label.setText('<a href="ms-settings:fonts">다른 글꼴 표시</a>')
        show_more_fonts_label.setOpenExternalLinks(False)  # 하이퍼링크를 외부 브라우저에서 열지 않도록 설정
        show_more_fonts_label.linkActivated.connect(self.show_more_fonts)
        
        font_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        font_button_box.accepted.connect(font_window.accept)
        font_button_box.rejected.connect(font_window.reject)
        
        self.font_ok_button = font_button_box.button(QDialogButtonBox.Ok)
        self.font_ok_button.setText('확인')
        self.font_ok_button.clicked.connect(self.set_font_ok_button)
        
        self.font_cancel_button = font_button_box.button(QDialogButtonBox.Cancel)
        self.font_cancel_button.setText('취소')
        
        # event signals
        self.font_lineedit.installEventFilter(self)
        self.font_list.installEventFilter(self)
        self.font_style_lineedit.installEventFilter(self)
        self.font_size_lineedit.installEventFilter(self)
        
        self.font_list.mouseDoubleClickEvent = lambda event: self.mouseDoubleClickEvent(event)
        self.font_style_list.mouseDoubleClickEvent = lambda event: self.mouseDoubleClickEvent(event)
        self.font_size_list.mouseDoubleClickEvent = lambda event: self.mouseDoubleClickEvent(event)
        
        self.font_list.clicked.connect(self.set_font_list_mouse_event)
        self.font_style_list.clicked.connect(self.set_font_style_mouse_event)
        self.font_size_list.clicked.connect(self.set_font_size_mouse_event)
        self.font_style_list_selectionmodel.selectionChanged.connect(self.set_font_style_list_item_selected)
        self.font_size_list_selectionmodel.selectionChanged.connect(self.set_font_size_list_item_selected)
        
        # layout setting
        font_window_layout = QVBoxLayout()
        font_window.setLayout(font_window_layout)
        
        horizon_layout = QHBoxLayout()
        font_window_layout.addLayout(horizon_layout)
        
        font_layout = QVBoxLayout()
        font_layout.setSpacing(0)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_lineedit)
        font_layout.addWidget(self.font_list)
        font_style_layout = QVBoxLayout()
        font_style_layout.setSpacing(0)
        font_style_layout.addWidget(font_style_label)
        font_style_layout.addWidget(self.font_style_lineedit)
        font_style_layout.addWidget(self.font_style_list)
        font_size_layout = QVBoxLayout()
        font_size_layout.setSpacing(0)
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_lineedit)
        font_size_layout.addWidget(self.font_size_list)
        
        horizon_layout.addLayout(font_layout)
        horizon_layout.addLayout(font_style_layout)
        horizon_layout.addLayout(font_size_layout)
        horizon_layout.setContentsMargins(4,4,4,0)
        horizon_layout.setSpacing(14)
        
        font_preview_layout = QVBoxLayout()
        font_preview_layout.addWidget(font_preview_groupbox)
        font_preview_layout.addWidget(font_script_label)
        font_preview_layout.addWidget(self.font_script_combobox)
        font_preview_layout.setContentsMargins(178,4,4,0)
        
        button_layout = QHBoxLayout()
        # button_layout.setAlignment(Qt.AlignBottom)
        button_layout.addStretch(2)
        button_layout.addWidget(font_button_box)
        
        font_window_layout.addLayout(font_preview_layout)
        font_window_layout.addStretch(1)
        font_window_layout.addWidget(show_more_fonts_label)
        font_window_layout.addLayout(button_layout)
        
        font_window.show()
    
    def set_font_widget(self,label,lineedit,list,size):
        label.setMaximumWidth(size)
        lineedit.setMaximumWidth(size)
        list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list.setMaximumSize(size,145)
    
    def show_more_fonts(self):
        url = QUrl("ms-settings:fonts")
        QDesktopServices.openUrl(url)
    
    def set_font_list(self):
        font_families = QFontDatabase.families()
        
        black_list = ['Fixedsys','Modern','MS Serif','MS Sans Serif','Roman','Script','Small Fonts','System','Terminal']
        self.all_styles = []
        temp_all_styles = []
        self.font_languages = {}
        
        for font_family in font_families:
            if not QFontDatabase.pointSizes(font_family):
                black_list.append(font_family)
            
            temp_all_styles.append(QFontDatabase.styles(font_family))
            item = QStandardItem(font_family)
            if font_family not in black_list:
                item.setFont(QFont(font_family, 12)) # Apply the font
                item.setSizeHint(QSize(100,20))
                self.font_list_model.appendRow(item)
            
            font_languages = QFontDatabase.writingSystems(font_family)
            value = []
            for language in font_languages:
                script = str(language).split('.')[1]
                value.append(script)
            self.font_languages[font_family] = value
        
        for styles in set(map(tuple,temp_all_styles)):
            for style in styles:
                self.all_styles.append(style)
        
        current_font = self.config['font_family']['font']
        font_select_item = self.font_list_model.findItems(current_font, Qt.MatchExactly) # MatchFixedString
        for item in font_select_item:
            selected_font_list_item_text = item.text()
            index = item.index()
            self.font_list_selectionmodel.select(index,QItemSelectionModel.Select)
            self.font_list.scrollTo(index, QAbstractItemView.PositionAtCenter)
        
        self.font_lineedit.setText(selected_font_list_item_text)
        self.font_lineedit.selectAll()
    
    def set_font_list_item_selected(self, selected, deselected):
        self.font_style_list_model.clear()
        self.font_script_combobox.clear()
        selected_font_list_item = selected
        selected_font_list_item_index = selected_font_list_item.indexes()[0]
        selected_font_list_item_text = selected_font_list_item_index.data(Qt.DisplayRole)
        
        # append style list
        font_style_list = [style for style in QFontDatabase.styles(selected_font_list_item_text)]
        # print(font_style_list)
        for style_name in font_style_list:
            item = QStandardItem(style_name)
            font = selected_font_list_item_text
            style = style_name
            item.setFont(self.set_font_style(font,style,12))  # Apply the font style
            item.setSizeHint(QSize(100,20))
            self.font_style_list_model.appendRow(item)
        
        # append size list
        font_size_list = [size for size in QFontDatabase.pointSizes(selected_font_list_item_text)]
        # print(font_size_list)
        self.font_size_list_model.setStringList((str(size) for size in font_size_list))
        
        # select style
        font_style_selected_item = self.font_style_list.selectedIndexes()
        font_match_style_item = self.font_style_list_model.findItems(self.current_font_style, Qt.MatchExactly) # MatchFixedString
        
        if not font_match_style_item:
            if font_match_style_item != self.current_font_style:
                self.font_style_list.setCurrentIndex(self.font_style_list_model.index(0,0))
                selected_style_list_item_text = self.font_style_list_model.itemFromIndex(self.font_style_list_model.index(0,0)).text()
                self.current_font_style = selected_style_list_item_text
        else:
            for item in font_match_style_item:
                selected_style_list_item_text = item.text()
                index = item.index()
                self.font_style_list_selectionmodel.select(index,QItemSelectionModel.Select)
                selected_style_item_text = self.font_style_list_model.itemFromIndex(index).text()
                self.font_style_list.scrollTo(index, QAbstractItemView.PositionAtCenter)
        
        # select size
        # 리스트에서 문자열 찾아 인덱스 가져오기
        indexes = self.font_size_list_model.match(
            self.font_size_list_model.index(0), Qt.DisplayRole, self.current_font_size, -1, Qt.MatchExactly)
        
        if indexes:
            # 찾은 인덱스로 선택하기
            index = indexes[0]
            self.font_size_list.setCurrentIndex(index)
            selected_size_list_item_text = index.data()
        else:
            # 인덱스 0을 선택하고 선택된 값 가져오기
            self.font_size_list.setCurrentIndex(self.font_size_list_model.index(0))
            selected_size_list_item_index = self.font_size_list.selectedIndexes()[0]
            selected_size_list_item_text = self.font_size_list_model.data(selected_size_list_item_index,Qt.DisplayRole)
        
        self.font_lineedit.setText(selected_font_list_item_text)
        self.font_lineedit.selectAll()
        self.font_style_lineedit.setText(selected_style_list_item_text)
        self.font_size_lineedit.setText(selected_size_list_item_text)
        self.font_script_combobox.addItems(self.font_languages[selected_font_list_item_text])
        self.current_font = selected_font_list_item_text
    
    def set_font_style_list_item_selected(self, selected, deselected):
        if not selected.indexes(): # 선택된 항목이 없는 경우
            self.font_lineedit.deselect()
            if deselected.indexes():
                self.font_style_list_selectionmodel.select(deselected.indexes()[0],QItemSelectionModel.Select)
        else:
            selected_font_style_list_item_index = selected.indexes()[0]
            selected_font_style_list_item_text = selected_font_style_list_item_index.data(Qt.DisplayRole)
            self.current_font_style = selected_font_style_list_item_text
            
            font = self.current_font
            style = self.current_font_style
            size = self.current_font_size
            self.font_style_lineedit.setText(style)
            self.font_style_lineedit.selectAll()
            self.font_preview_label.setFont(self.set_font_style(font,style,size))
    
    def set_font_style(self,font,style,size):
        font = QFont(font,int(size))
        if style == 'Normal' or style == 'Regular':
            font.setStyle(QFont.StyleNormal)
        elif style == 'Bold':
            font.setBold(True)
        elif style == 'Bold Italic':
            font.setBold(True)
            font.setItalic(True)
        elif style == 'Bold SemiCondensed':
            font.setBold(True)
            font.setLetterSpacing(QFont.PercentageSpacing, 90)
        elif style == 'SemiBold':
            font.setWeight(QFont.DemiBold)
        elif style == 'SemiBold Condensed':
            font.setWeight(QFont.DemiBold)
            font.setLetterSpacing(QFont.PercentageSpacing, 80)
        elif style == 'SemiBold SemiCondensed':
            font.setWeight(QFont.DemiBold)
            font.setLetterSpacing(QFont.PercentageSpacing, 90)
        elif style == 'Italic':
            font.setItalic(True)
        elif style == 'Narrow' or style == 'Condensed':
            font.setLetterSpacing(QFont.PercentageSpacing, 80)
        elif style == 'Narrow Bold' or style == 'Bold Condensed':
            font.setBold(True)
            font.setLetterSpacing(QFont.PercentageSpacing, 80)
        elif style == 'Narrow Bold Italic' or style == 'Condensed Bold Italic':
            font.setBold(True)
            font.setItalic(True)
            font.setLetterSpacing(QFont.PercentageSpacing, 80)
        elif style == 'Narrow Italic' or style == 'Condensed Italic':
            font.setItalic(True)
            font.setLetterSpacing(QFont.PercentageSpacing, 80)
        elif style == 'SemiCondensed':
            font.setLetterSpacing(QFont.PercentageSpacing, 90)
        elif style == 'Light':
            font.setWeight(QFont.ExtraLight)
        elif style == 'Light Condensed':
            font.setWeight(QFont.ExtraLight)
            font.setLetterSpacing(QFont.PercentageSpacing, 80)
        elif style == 'Light SemiCondensed':
            font.setWeight(QFont.ExtraLight)
            font.setLetterSpacing(QFont.PercentageSpacing, 90)
        elif style == 'SemiLight':
            # font.setWeight(QFont.Light + ((QFont.Normal - QFont.Light) * 2) // 3)  # SemiLight 스타일로 폰트 굵기 설정
            font.setWeight(QFont.Light)
        elif style == 'SemiLight SemiCondensed':
            font.setWeight(QFont.Light)
            font.setLetterSpacing(QFont.PercentageSpacing, 90)
        elif style == 'Black':
            font.setWeight(QFont.Black)
        else:
            font.setStyle(QFont.StyleNormal)
        
        return font
    
    def set_font_size_list_item_selected(self, selected, deselected):
        if selected.indexes():
            selected_font_size_list_item_index = selected.indexes()[0]
            selected_font_size_list_item_text = selected_font_size_list_item_index.data(Qt.DisplayRole)
            self.current_font_size = selected_font_size_list_item_text
            
            font = self.current_font
            style = self.current_font_style
            size = self.current_font_size
            self.font_size_lineedit.setText(size)
            self.font_size_lineedit.selectAll()
            self.font_preview_label.setFont(self.set_font_style(font,style,size))
        else:
            self.font_style_lineedit.deselect()
            if deselected.indexes():
                self.font_size_list.setCurrentIndex(deselected.indexes()[0])
    
    def set_font_list_mouse_event(self,event):
        self.font_lineedit.selectAll()
        self.font_style_lineedit.deselect()
        self.font_size_lineedit.deselect()
    
    def set_font_style_mouse_event(self,event):
        self.font_style_lineedit.selectAll()
        self.font_lineedit.deselect()
        self.font_size_lineedit.deselect()
    
    def set_font_size_mouse_event(self,event):
        self.font_size_lineedit.selectAll()
        self.font_lineedit.deselect()
        self.font_style_lineedit.deselect()
    
    def set_font_ok_button(self):
        font = self.config['font_family']['font'] = self.current_font
        style = self.config['font_family']['style'] = self.current_font_style
        size = self.config['font_family']['size'] = self.current_font_size
        self.text_edit.setFont(self.set_font_style(font,style,size))
    
    # view action
    def set_zoom_in(self):
        font = self.text_edit.font()
        zoom_value = 1.1
        font_size = font.pointSizeF() * zoom_value  # 확대 비율 설정
        font.setPointSizeF(font_size)
        self.text_edit.setFont(font)
        self.default_zoom += 10
        self.zoom_label.setText(f'{self.default_zoom}%')
        print(font_size)
    
    def set_zoom_out(self):
        font = self.text_edit.font()
        zoom_value = 0.9
        font_size = font.pointSizeF() * zoom_value  # 축소 비율 설정
        font.setPointSizeF(font_size)
        self.text_edit.setFont(font)
        self.default_zoom -= 10
        self.zoom_label.setText(f'{self.default_zoom}%')
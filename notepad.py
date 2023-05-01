import sys,os,json
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QGridLayout,QFrame,
    QPlainTextEdit,QMenuBar,QMenu,QStatusBar,
    QDialog,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QCheckBox,QRadioButton,QGroupBox,QMessageBox)
from PySide6.QtGui import QAction,QIcon,QFont,QColor,QPalette,QTextDocument
from PySide6.QtCore import Qt

from actions import SetActions

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow,SetActions):
    def __init__(self):
        QMainWindow.__init__(self)
        self.set_init()
        self.set_ui()
        # self.test()
        self.show()
    
    def set_init(self):
        self.file_name = '제목 없음'
        self.previous_filename = self.file_name
        self.window_title = self.file_name + ' - Windows 메모장'
        self.modify = False
        self.filter_option='텍스트 문서(*.txt);;모든 파일 (*.*)'
        self.windows = []
        self.save_status = ''
        self.closed = False
        self.default_zoom = 100
        self.encoding = 'UTF-8'
        self.find_next_action_isrun = False
        self.find_status = ''
        
        self.setWindowIcon(QIcon('./image/notepad_icon.png'))
        self.setWindowTitle(self.window_title)
        self.set_config()
        
        # selected color
        self.palette = QPalette()
        self.palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        self.palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    def set_ui(self):
        self.set_text_edit()
        self.set_menu()
        self.set_statusbar()
    
    def set_config(self):
        config_json = None
        self.config = {
            'geometry':[],
            'find_keyword':'',
            'replace_keyword':'',
            'find_upndown':'',
            'case_sensitivity':'',
            'wrap_around':''}
        
        try:
            with open(str(os.path.join(CURRENT_PATH,'config.json')),'r') as r:
                config_json = json.load(r)
        except FileNotFoundError:
            with open(str(os.path.join(CURRENT_PATH,'config.json')),'w') as w:
                json.dump(self.config,w,indent=4)
                config_json = self.config
        else:
            for key in self.config.keys():
                if key not in config_json:
                    config_json[key] = ''
        
        if config_json['geometry']:
            geometry = config_json['geometry']
            self.setGeometry(geometry[0],geometry[1],geometry[2],geometry[3])
        else:
            self.setGeometry(0,30,1280,720)
        
        self.config['find_keyword'] = config_json['find_keyword']
        
        if config_json['find_upndown']:
            self.config['find_upndown'] = config_json['find_upndown']
        else:
            self.config['find_upndown'] = 'down'
        
        if config_json['case_sensitivity']:
            self.config['case_sensitivity'] = config_json['case_sensitivity']
        else:
            self.config['case_sensitivity'] = 'no'
        
        if config_json['wrap_around']:
            self.config['wrap_around'] = config_json['wrap_around']
        else:
            self.config['wrap_around'] = 'no'
        print(self.config)
    
    def set_text_edit(self):
        self.text_edit = QPlainTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_edit.setFrameShape(QFrame.NoFrame)
        self.original_text = self.text_edit.toPlainText()
        self.text_edit.setPalette(self.palette)
        
        # signal
        self.text_edit.cursorPositionChanged.connect(self.set_cursor_position)
        self.text_edit.textChanged.connect(self.checking_modify_document)
        self.text_edit.undoAvailable.connect(lambda available:self.undo_action.setEnabled(available))
        self.text_edit.redoAvailable.connect(lambda available:self.redo_action.setEnabled(available))
        self.text_edit.copyAvailable.connect(self.select_available)
    
    def checking_modify_document(self):
        if self.original_text != self.text_edit.toPlainText():
            print('modify')
            self.setWindowTitle(f'*{os.path.basename(self.file_name)}' + ' - Windows 메모장')
            self.modify = True
        elif self.original_text == self.text_edit.toPlainText():
            print('no modify')
            self.setWindowTitle(f'{os.path.basename(self.file_name)}' + ' - Windows 메모장')
            self.modify = False
    
    def set_menu(self):
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        
        self.file_menu = QMenu(self.menubar)
        self.file_menu.setTitle('파일(&F)')
        self.menubar.addMenu(self.file_menu)
        self.set_file_action()
        
        self.edit_menu = QMenu(self.menubar)
        self.edit_menu.setTitle('편집(&E)')
        self.menubar.addMenu(self.edit_menu)
        self.set_edit_action()
        
        self.format_menu = QMenu(self.menubar)
        self.format_menu.setTitle('서식(&O)')
        self.menubar.addMenu(self.format_menu)
        self.set_format_action()
        
        self.view_menu = QMenu(self.menubar)
        self.view_menu.setTitle('보기(&V)')
        self.menubar.addMenu(self.view_menu)
        self.set_view_action()
        
        self.help_menu = QMenu(self.menubar)
        self.help_menu.setTitle('도움말(&H)')
        self.menubar.addMenu(self.help_menu)
        self.set_help_action()
    
    def set_file_action(self):
        self.new_action = QAction('새로 만들기(&N)')
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.triggered.connect(self.new)
        
        self.new_window_action = QAction('새 창(&W)')
        self.new_window_action.setShortcut('Ctrl+Shift+N')
        self.new_window_action.triggered.connect(self.new_window)
        
        self.open_action = QAction('열기(&O)...')
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.open)
        
        self.save_action = QAction('저장(&S)')
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save)
        
        self.saveas_action = QAction('다른 이름으로 저장(&A)...')
        self.saveas_action.setShortcut('Ctrl+Shift+S')
        self.saveas_action.triggered.connect(self.save_as)
        
        file_separator1 = self.file_menu.addSeparator()
        
        self.page_action = QAction('페이지 설정(&U)...')
        self.page_action.triggered.connect(self.setup_page)
        
        self.print_action = QAction('인쇄(&P)...')
        self.print_action.setShortcut('Ctrl+P')
        self.print_action.triggered.connect(self.setup_printer)
        
        file_separator2 = self.file_menu.addSeparator()
        
        self.exit_action = QAction('끝내기(&X)')
        self.exit_action.triggered.connect(self.close)
        
        self.file_menu.addActions([
            self.new_action,
            self.new_window_action,
            self.open_action,
            self.save_action,
            self.saveas_action,
            file_separator1,
            self.page_action,
            self.print_action,
            file_separator2,
            self.exit_action
            ])
    
    def set_edit_action(self):
        self.edit_menu.aboutToShow.connect(self.show_edit_menu)
        
        self.undo_action = QAction('실행 취소(&U)')
        self.undo_action.setShortcut('Ctrl+Z')
        self.undo_action.setDisabled(True)
        self.undo_action.triggered.connect(self.text_edit.undo)
        
        self.redo_action = QAction('다시 실행(&Y)')
        self.redo_action.setShortcut('Ctrl+Y')
        self.redo_action.setDisabled(True)
        self.redo_action.triggered.connect(self.text_edit.redo)
        
        separator1 = self.edit_menu.addSeparator()
        
        self.cut_action = QAction('잘라내기(&T)')
        self.cut_action.setShortcut('Ctrl+X')
        self.cut_action.setDisabled(True)
        self.cut_action.triggered.connect(self.text_edit.cut)
        
        self.copy_action = QAction('복사(&C)')
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.setDisabled(True)
        self.copy_action.triggered.connect(self.text_edit.copy)
        
        self.paste_action = QAction('붙여넣기(&P)')
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.triggered.connect(self.text_edit.paste)
        
        self.delete_action = QAction('삭제(&D)')
        self.delete_action.setShortcut('Del')
        self.delete_action.setDisabled(True)
        self.delete_action.triggered.connect(self.delete)
        
        separator2 = self.edit_menu.addSeparator()
        
        self.bing_action = QAction('Bing으로 검색(&S)...')
        self.bing_action.setShortcut('Ctrl+E')
        
        self.find_action = QAction('찾기(&F)...')
        self.find_action.triggered.connect(self.set_find_action)
        
        self.find_next_action = QAction('다음 찾기(&N)')
        self.find_next_action.setShortcut('F3')
        self.find_next_action.triggered.connect(self.set_find_next_action)
        
        self.find_previous_action = QAction('이전 찾기(&V)')
        self.find_previous_action.setShortcut('Shift+F3')
        self.find_previous_action.triggered.connect(self.set_find_previous_action)
        
        self.replace_action = QAction('바꾸기(&R)...')
        self.replace_action.setShortcut('Ctrl+H')
        self.replace_action.triggered.connect(self.set_replace_action)
        
        self.go_to_action = QAction('이동(&G)...')
        self.go_to_action.setShortcut('Ctrl+G')
        
        separator3 = self.edit_menu.addSeparator()
        
        self.select_all_action = QAction('모두 선택(&A)')
        self.select_all_action.setShortcut('Ctrl+A')
        
        self.time_date_action = QAction('시간/날짜(&D)')
        self.time_date_action.setShortcut('F5')
        
        self.edit_menu.addActions([
            self.undo_action,
            self.redo_action,
            separator1,
            self.cut_action,
            self.copy_action,
            self.paste_action,
            self.delete_action,
            separator2,
            self.bing_action,
            self.find_action,
            self.find_next_action,
            self.find_previous_action,
            self.replace_action,
            self.go_to_action,
            separator3,
            self.select_all_action,
            self.time_date_action
        ])
    
    def set_format_action(self):
        self.word_wrap_action = QAction('자동 줄 바꿈(W&)')
        self.word_wrap_action.setCheckable(True)
        self.word_wrap_action.setChecked(True)
        
        self.set_font_action = QAction('글꼴(F&)...')
        self.set_font_action.setShortcut('Ctrl+Shift+')
        
        self.format_menu.addActions([self.word_wrap_action,self.set_font_action])
    
    def set_view_action(self):
        self.zoom_action = self.view_menu.addMenu('확대하기/축소하기')
        
        self.zoom_in = QAction('확대(&I)')
        self.zoom_in.setShortcut('Ctrl++')
        self.zoom_in.triggered.connect(self.set_zoom_in)
        
        self.zoom_out = QAction('축소(&O)')
        self.zoom_out.setShortcut('Ctrl+-')
        self.zoom_out.triggered.connect(self.set_zoom_out)
        
        self.restore_default_zoom = QAction('확대하기/축소하기 기본값 복원(&)')
        self.restore_default_zoom.setShortcut('Ctrl+0')
        self.restore_default_zoom.triggered.connect(lambda:print())
        
        self.status_bar_action = QAction('상태 표시줄(S&)')
        self.status_bar_action.setCheckable(True)
        self.status_bar_action.setChecked(True)
        
        self.view_menu.addMenu(self.zoom_action)
        self.zoom_action.addActions([
            self.zoom_in,self.zoom_out,self.restore_default_zoom])
        self.view_menu.addAction(self.status_bar_action)
    
    def set_help_action(self):
        self.view_help_action = QAction('도움말 보기(H&)')
        
        self.send_feedback_action = QAction('피드백 보내기(F&)')
        
        separator = self.help_menu.addSeparator()
        
        self.about_notepad_action = QAction('메모장 정보(A&)')
        
        self.help_menu.addActions([
            self.view_help_action,
            self.send_feedback_action,
            separator,
            self.about_notepad_action])
    
    def set_statusbar(self):
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
        separator1 = QLabel('')
        separator1.setAlignment(Qt.AlignRight)
        self.statusbar.addPermanentWidget(separator1)
        
        self.cursor_position_label = QLabel()
        self.cursor_position_label.setAlignment(Qt.AlignLeft)
        self.cursor_position_label.setMinimumWidth(130)
        self.statusbar.addPermanentWidget(self.cursor_position_label)
        self.set_cursor_position()
        
        self.zoom_label = QLabel(f'{self.default_zoom}%')
        self.zoom_label.setMinimumWidth(45)
        self.statusbar.addPermanentWidget(self.zoom_label)
        
        self.eol_label = QLabel('Windows (CRLF)')
        self.eol_label.setMinimumWidth(120)
        self.statusbar.addPermanentWidget(self.eol_label)
        
        self.encoding_label = QLabel(self.encoding)
        self.encoding_label.setMinimumWidth(90)
        self.statusbar.addPermanentWidget(self.encoding_label)
    
    def set_cursor_position(self):
        cursor = self.text_edit.textCursor()
        cursor_position = cursor.blockNumber()+1,cursor.columnNumber()+1
        self.cursor_position_label.setText(f'Ln {cursor_position[0]}, Col {cursor_position[1]}')
    
    def new_window(self):
        new_window = MainWindow()
        self.windows.append(new_window)
        new_window.show()
    
    def closeEvent(self,event):
        self.close_event = event
        self.closed = True
        self.save_status = 'close'
        if self.modify:
            self.run_messagebox_button()
        
        self.config['geometry'] = self.x(),self.y()+30,self.width(),self.height()
        with open(str(os.path.join(CURRENT_PATH,'config.json')),'w') as w:
            json.dump(self.config,w,indent=4)
    
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
        
        self.find_next_button = QPushButton('다음 찾기(&F)')
        if self.find_line_edit.text():
            self.find_next_button.setEnabled(True)
        else:
            self.find_next_button.setEnabled(False)
        
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
        
        # signal
        self.find_line_edit.textChanged.connect(self.line_edit_text_changer)
        self.find_next_button.clicked.connect(self.set_find_next_button)
        
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
    
    def set_find_next_button(self):
        document = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        cursor_position = cursor.position()
        self.keyword_to_find = self.find_line_edit.text()
        
        if self.radiobox_down.isChecked():
            if self.case_sensitivity_checkbox.isChecked():
                flag = QTextDocument.FindCaseSensitively
                cursor = document.find(self.keyword_to_find,cursor_position,flag)
            else:
                cursor = document.find(self.keyword_to_find,cursor_position)
        else:
            if cursor.selectedText():
                start_position = cursor_position - len(self.keyword_to_find)
            else:
                start_position = cursor_position
            
            if self.case_sensitivity_checkbox.isChecked():
                flag = QTextDocument.FindBackward | QTextDocument.FindCaseSensitively
                cursor = document.find(self.keyword_to_find,start_position,flag)
            else:
                flag = QTextDocument.FindBackward
                cursor = document.find(self.keyword_to_find,start_position,flag)
        
        if not cursor.isNull():
            self.text_edit.setTextCursor(cursor)
        else:
            if self.wrap_around_checkbox.isChecked():
                if self.radiobox_down.isChecked():
                    if self.case_sensitivity_checkbox.isChecked():
                        flag = QTextDocument.FindCaseSensitively
                        cursor = document.find(self.keyword_to_find,0,flag)
                    else:
                        cursor = document.find(self.keyword_to_find,0)
                else:
                    end_index = document.characterCount() - 1
                    if end_index != -1:
                        if self.case_sensitivity_checkbox.isChecked():
                            flag = QTextDocument.FindBackward | QTextDocument.FindCaseSensitively
                            cursor = document.find(self.keyword_to_find,end_index,flag)
                        else:
                            flag = QTextDocument.FindBackward
                    cursor = document.find(self.keyword_to_find,end_index,flag)
                
                self.text_edit.setTextCursor(cursor)
            else:
                QMessageBox.information(self, '메모장', f'"{self.keyword_to_find}"을(를) 찾을 수 없습니다.')
    
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
        horizon_find_lineedit_layout = QHBoxLayout()
        horizon_replace_lineedit_layout = QHBoxLayout()
        vertical_button_layout = QVBoxLayout()
        vertical_checkbox_layout = QVBoxLayout()
        
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
        
        self.replace_button = QPushButton('바꾸기(&R)')
        
        self.all_replace_button = QPushButton('모두 바꾸기(&A)')
        
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
        
        # signal
        self.find_line_edit.textChanged.connect(self.line_edit_text_changer)
        self.find_next_button.clicked.connect(self.set_find_next_button)
        
        # add widget
        grid_layout.addWidget(find_label,0,0)
        grid_layout.addWidget(self.find_line_edit,0,1,1,3)
        grid_layout.addWidget(replace_label,1,0)
        grid_layout.addWidget(self.replace_line_edit,1,1,1,3)
        
        grid_layout.addWidget(self.find_next_button,0,4)
        grid_layout.addWidget(self.replace_button,1,4)
        grid_layout.addWidget(self.all_replace_button,2,4)
        grid_layout.addWidget(find_cancel_button,3,4)
        
        grid_layout.addWidget(self.case_sensitivity_checkbox,3,0,1,2)
        grid_layout.addWidget(self.wrap_around_checkbox,4,0,1,2)
        
        # grid_layout.addWidget(QWidget(self.replace_window),4,2,1,1)
        # grid_layout.addWidget(QWidget(self.replace_window),4,3,1,1)
        # grid_layout.addWidget(QWidget(self.replace_window),4,4,1,1)
        
        # self.replace_window.setAttribute(Qt.WA_DeleteOnClose)
        self.replace_window.closeEvent = self.set_find_cancel_button
        self.replace_window.show()
    
    def set_find_cancel_button(self,event):
        self.config['find_keyword'] = self.find_line_edit.text()
        if not self.find_line_edit.text():
            self.find_next_action_isrun = False
        
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
    
app = QApplication(sys.argv)
window = MainWindow()
app.exec()
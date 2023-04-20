import sys,os
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QGridLayout,QFrame,
    QPlainTextEdit,QMenuBar,QMenu,QStatusBar,
    QDialog,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QCheckBox,QRadioButton,QGroupBox,QMessageBox)
from PySide6.QtGui import QAction,QIcon,QFont,QTextCursor,QColor,QPalette
from PySide6.QtCore import Qt

from actions import SetActions

image_path = os.path.dirname(os.path.abspath(__file__))

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
        
        # select color
        self.palette = QPalette()
        self.palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        self.palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    def set_ui(self):
        self.setWindowIcon(QIcon('./image/notepad_icon.png'))
        self.setWindowTitle(self.window_title)
        self.resize(1280,720)
        
        self.set_text_edit()
        self.set_menu()
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
    
    def set_text_edit(self):
        self.text_edit = QPlainTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_edit.setFrameShape(QFrame.NoFrame)
        self.original_text = self.text_edit.toPlainText()
        self.text_edit.setPalette(self.palette)
        
        # signal
        self.text_edit.textChanged.connect(self.checking_modify_document)
        self.text_edit.undoAvailable.connect(self.undo_available)
        self.text_edit.redoAvailable.connect(self.redo_available)
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
        
        self.form_menu = QMenu(self.menubar)
        self.form_menu.setTitle('서식(&O)')
        self.menubar.addMenu(self.form_menu)
        self.set_form_action()
        
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
        
        self.bing_action = QAction('Bing으로 검색...(&S)')
        self.bing_action.setShortcut('Ctrl+E')
        
        self.find_action = QAction('찾기...(&F)')
        self.find_action.triggered.connect(self.test)
        
        self.find_next_action = QAction('다음 찾기(&N)')
        self.find_next_action.setShortcut('F3')
        
        self.find_previous_action = QAction('이전 찾기(&V)')
        self.find_previous_action.setShortcut('Shift+F3')
        
        self.replace_action = QAction('바꾸기...(&R)')
        self.replace_action.setShortcut('Ctrl+H')
        
        self.go_to_action = QAction('이동...(&G)')
        self.go_to_action.setShortcut('Ctrl+G')
        
        separator3 = self.edit_menu.addSeparator()
        
        self.select_all_action = QAction('모두 선택(&A)')
        self.select_all_action.setShortcut('Ctrl+A')
        
        self.time_date_action = QAction('시간/날짜(&D)')
        self.time_date_action.setShortcut('F5')
        
        self._action = QAction('(&)')
        self._action.setShortcut('Ctrl+Shift+')
        
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
    
    def set_form_action(self):
        pass
    
    def set_view_action(self):
        pass
    
    def set_help_action(self):
        pass
    
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
    
    def test(self):
        self.find_window = QDialog(self)
        self.find_window.setWindowTitle('찾기')
        self.find_window.setFixedSize(392,156)
        
        # layout
        self.grid_layout = QGridLayout(self.find_window)
        self.horizon_lineedit_layout = QHBoxLayout()
        self.vertical_button_layout = QVBoxLayout()
        self.vertical_checkbox_layout = QVBoxLayout()
        self.direction_groupbox = QGroupBox('방향')
        self.direction_groupbox.setMaximumHeight(60)
        self.horizon_direction_layout = QHBoxLayout()
        
        # widget
        self.label = QLabel('찾을 내용')
        self.find_line_edit = QLineEdit()
        self.find_line_edit.setPalette(self.palette)
        
        self.find_next_button = QPushButton('다음 찾기(&F)')
        if self.text_edit.toPlainText():
            self.find_next_button.setEnabled(True)
        else:
            self.find_next_button.setEnabled(False)
        self.cancel_button = QPushButton('취소')
        
        self.checkbox1 = QCheckBox('대/소문자 구분(&C)')
        self.checkbox2 = QCheckBox('주위에 배치(&R)')
        
        self.radiobox1 = QRadioButton('위로(&U)')
        self.radiobox1.setMaximumWidth(60)
        self.radiobox2 = QRadioButton('아래로(&D)')
        self.radiobox2.setChecked(True)
        
        # signal
        self.find_line_edit.textChanged.connect(self.line_edit_text_changer)
        self.find_next_button.clicked.connect(self.find_next)
        
        # add widget
        self.horizon_lineedit_layout.addWidget(self.label)
        self.horizon_lineedit_layout.addWidget(self.find_line_edit)
        self.grid_layout.addLayout(self.horizon_lineedit_layout,0,0,1,3)
        
        self.grid_layout.addWidget(self.find_next_button,0,4)
        self.grid_layout.addWidget(self.cancel_button,1,4)
        
        self.vertical_checkbox_layout.addWidget(self.checkbox1)
        self.vertical_checkbox_layout.addWidget(self.checkbox2)
        self.grid_layout.addLayout(self.vertical_checkbox_layout,2,0)
        
        self.horizon_direction_layout.addWidget(self.radiobox1)
        self.horizon_direction_layout.addWidget(self.radiobox2)
        self.direction_groupbox.setLayout(self.horizon_direction_layout)
        self.grid_layout.addWidget(self.direction_groupbox,1,1,2,1)
        
        self.setLayout(self.grid_layout)
        self.find_window.show()
    
    def find_next(self):
        keyword = self.find_line_edit.text()
        cursor = self.text_edit.document().find(keyword)
        if keyword:
            if cursor.isNull():
                    QMessageBox.information(self, "Information", f"No result for {keyword}")
            else:
                # 검색 결과가 있으면 해당 영역을 선택합니다.
                self.text_edit.setTextCursor(cursor)
                # 검색된 영역을 스크롤합니다.
                cursor.select(QTextCursor.WordUnderCursor)
                self.text_edit.ensureCursorVisible()

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
import sys,os
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QGridLayout,QVBoxLayout,QFrame,
    QPlainTextEdit,QMenuBar,QMenu,QStatusBar)
from PySide6.QtGui import QAction,QIcon
from PySide6.QtCore import Qt

from actions import SetActions

image_path = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_window = QMainWindow()
        self.set_init()
        self.set_ui()
        self.set_menu()
        # self.test()
        self.show()
    
    def set_init(self):
        self.action = SetActions()
        self.file_name = '제목 없음'
        self.previous_filename = self.file_name
        self.window_title = self.file_name + ' - Windows 메모장'
        self.modify = False
        self.filter_option='텍스트 문서(*.txt);;모든 파일 (*.*)'
        self.windows = []
        self.save_status = ''
        self.closed = False
        self.clipboard = QApplication.clipboard()
    
    def set_ui(self):
        self.setWindowIcon(QIcon('./image/notepad_icon.png'))
        self.setWindowTitle(self.window_title)
        self.resize(1280,720)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.vlayout = QVBoxLayout(self.central_widget)
        self.vlayout.setContentsMargins(0,0,0,0)
        
        self.text_edit = QPlainTextEdit(self.central_widget)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_edit.setFrameShape(QFrame.NoFrame)
        self.vlayout.addWidget(self.text_edit)
        self.original_text = self.text_edit.toPlainText()
        
        # signal
        self.text_edit.textChanged.connect(self.checking_modify_document)
        self.text_edit.undoAvailable.connect(self.action.undo_available)
        self.text_edit.redoAvailable.connect(self.redo_available)
        self.text_edit.copyAvailable.connect(self.select_available)
        self.clipboard.dataChanged.connect(self.paste_available)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
    
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
        self.paste_action.setEnabled(self.text_edit.canPaste())
        self.paste_action.triggered.connect(self.text_edit.paste)
        
        self.delete_action = QAction('삭제(&D)')
        self.delete_action.setShortcut('Del')
        self.delete_action.setDisabled(True)
        self.delete_action.triggered.connect(self.delete)
        
        separator2 = self.edit_menu.addSeparator()
        
        self.bing_action = QAction('Bing으로 검색...(&S)')
        self.bing_action.setShortcut('Ctrl+E')
        
        self.find_action = QAction('찾기...(&F)')
        self.find_action.setShortcut('Ctrl+F')
        
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
        pass

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
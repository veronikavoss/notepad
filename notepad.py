import sys,os
from PySide6.QtWidgets import (
    QApplication,QMainWindow,QWidget,QGridLayout,QVBoxLayout,
    QPlainTextEdit,QMenuBar,QMenu,QStatusBar)
from PySide6.QtGui import QAction,QIcon
from PySide6.QtCore import Signal,QObject

from actions import SetActions

image_path = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow,SetActions):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_window = QMainWindow()
        self.set_init()
        self.set_ui()
        self.set_menu()
        self.show()
    
    def set_init(self):
        self.file_name = '제목 없음'
        self.previous_filename = self.file_name
        self.window_title = self.file_name + ' - Windows 메모장'
        self.modify = False
        self.filter_option='텍스트 문서 (*.txt);;모든 파일 (*.*)'
        self.windows = []
    
    def set_ui(self):
        self.setWindowIcon(QIcon('./image/notepad_icon.png'))
        self.setWindowTitle(self.window_title)
        self.resize(1280,720)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.vlayout = QVBoxLayout(self.central_widget)
        self.vlayout.setContentsMargins(0,0,0,0)
        
        self.plain_text_edit = QPlainTextEdit(self.central_widget)
        self.vlayout.addWidget(self.plain_text_edit)
        self.original_text = self.plain_text_edit.toPlainText()
        self.plain_text_edit.textChanged.connect(self.checking_modify_document)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
        # self.grid_layout = QGridLayout(self.central_widget)
        # self.grid_layout.setContentsMargins(0,0,0,0)
        
        # self.grid_layout.addLayout(self.vlayout,0,0,1,1)
    
    def checking_modify_document(self):
        # if not self.file_name:
        #     self.file_name = self.setWindowTitle(self.previous_filename)
        # else:
        #     self.file_name = os.path.basename(self.file_name)
        
        if self.original_text != self.plain_text_edit.toPlainText():
            print('modify')
            self.setWindowTitle(f'*{os.path.basename(self.file_name)}' + ' - Windows 메모장')
            self.modify = True
        elif self.original_text == self.plain_text_edit.toPlainText():
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
    
    def set_file_action(self):
        # self = FileAction(self,self.plain_text_edit,self.file_name)
        
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
        
        self.file_separator1 = self.file_menu.addSeparator()
        
        self.page_action = QAction('페이지 설정(&U)...')
        
        self.print_action = QAction('인쇄(&P)...')
        self.print_action.setShortcut('Ctrl+P')
        
        self.file_separator2 = self.file_menu.addSeparator()
        
        self.exit_action = QAction('끝내기(&X)')
        self.exit_action.triggered.connect(self.close)
        
        self._action = QAction('&')
        self._action.setShortcut('Ctrl+Shift+')
        
        self.file_menu.addActions([
            self.new_action,
            self.new_window_action,
            self.open_action,
            self.save_action,
            self.saveas_action,
            self.file_separator1,
            self.page_action,
            self.print_action,
            self.file_separator2,
            self.exit_action
            ])
    
    def new_window(self):
        new_window = MainWindow()
        self.windows.append(new_window)
        new_window.show()
    
    def closeEvent(self,event):
        print('close')
        if self.modify:
            self.save_messagebox()

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
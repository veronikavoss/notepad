from actions import *

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
        self.go_to_line_number = 1
        
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
            'wrap_around':'',
            'word_wrap_action':'',
            'font_family':{'font':'','style':'','size':''}
            }
        
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
        self.config['replace_keyword'] = config_json['replace_keyword']
        
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
        
        if config_json['word_wrap_action']:
            self.config['word_wrap_action'] = config_json['word_wrap_action']
        else:
            self.config['word_wrap_action'] = False
        
        if config_json['font_family']['font']:
            self.config['font_family']['font'] = config_json['font_family']['font']
        else:
            self.config['font_family']['font'] = "Arial"
        
        if config_json['font_family']['style']:
            self.config['font_family']['style'] = config_json['font_family']['style']
        else:
            self.config['font_family']['style'] = "regular"
        
        if config_json['font_family']['size']:
            self.config['font_family']['size'] = config_json['font_family']['size']
        else:
            self.config['font_family']['size'] = "12"
        
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
        self.undo_action.triggered.connect(self.set_undo_action)
        
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
        self.go_to_action.triggered.connect(self.set_go_to_action)
        
        separator3 = self.edit_menu.addSeparator()
        
        self.select_all_action = QAction('모두 선택(&A)')
        self.select_all_action.setShortcut('Ctrl+A')
        self.select_all_action.triggered.connect(lambda: self.text_edit.selectAll())
        
        self.time_date_action = QAction('시간/날짜(&D)')
        self.time_date_action.setShortcut('F5')
        self.time_date_action.triggered.connect(self.set_time_data_action)
        
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
        self.word_wrap_action.setChecked(self.config['word_wrap_action'])
        self.word_wrap_action.triggered.connect(self.set_word_wrap_action)
        self.set_word_wrap_action(self.config['word_wrap_action'])
        
        self.set_font_action = QAction('글꼴(F&)...')
        self.set_font_action.triggered.connect(self.set_font)
        
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
        self.config['word_wrap_action'] = self.word_wrap_action.isChecked()
        
        with open(str(os.path.join(CURRENT_PATH,'config.json')),'w') as w:
            json.dump(self.config,w,indent=4)
    
    def set_font(self):
        font_window = QDialog(self)
        font_window.setModal(True)
        font_window.setWindowTitle('글꼴')
        font_window.setFixedSize(404,486)
        
        # widget settings
        font_label = QLabel('글꼴(F):') # label
        self.font_lineedit = QLineEdit() # lineedit
        self.font_list = QListView() # list
        self.set_font_widget(font_label, self.font_lineedit, self.font_list, 160)
        self.font_list_model = QStandardItemModel()
        self.font_list.setModel(self.font_list_model)
        self.font_list_selectionmodel = self.font_list.selectionModel()
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
        
        self.set_font_list()
        
        font_preview_groupbox = QGroupBox('보기')
        font_preview_groupbox.setMaximumHeight(100)
        # font_preview_groupbox.setMaximumSize(QSize(16777215, 120))
        font_preview_label = QLabel()
        font_preview_label.setMargin(5)
        font_preview_label.setText('AaBbYyZz')
        # font_preview_label.setFont(QFont(self.config['font_family']['font'],int(self.config['font_family']['size'])))
        font = self.config['font_family']['font']
        style = self.config['font_family']['style']
        size = self.config['font_family']['size']
        font_preview_label.setStyleSheet(self.set_font_preview(font,style,size))
        font_preview_label.setAlignment(Qt.AlignCenter)
        font_preview_groupbox_layout = QVBoxLayout(font_preview_groupbox)
        font_preview_groupbox_layout.addWidget(font_preview_label)
        
        font_script_label = QLabel('스크립트(R):')
        font_script_combobox = QComboBox()
        
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
        font_preview_layout.addWidget(font_script_combobox)
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
        list.setMaximumSize(size,145)
    
    def show_more_fonts(self):
        url = QUrl("ms-settings:fonts")
        QDesktopServices.openUrl(url)
    
    def set_font_list(self):
        font_families = QFontDatabase.families()
        
        black_list = ['Fixedsys','Modern','MS Serif','MS Sans Serif','Roman','Script','Small Fonts','System','Terminal']
        for font in font_families:
            if not QFontDatabase.pointSizes(font):
                black_list.append(font)
            item = QStandardItem(font)
            if font not in black_list:
                item.setFont(QFont(font, 12))  # Apply the font
                item.setSizeHint(QSize(100,20))
                self.font_list_model.appendRow(item)
        
        current_font = self.config['font_family']['font']
        font_select_item = self.font_list_model.findItems(current_font, Qt.MatchExactly) # MatchFixedString
        for item in font_select_item:
            selected_font_list_item_text = item.text()
            index = item.index()
            self.font_list_selectionmodel.select(index,QItemSelectionModel.Select)
        
        self.font_lineedit.setText(selected_font_list_item_text)
        self.font_lineedit.selectAll()
    
    def set_font_list_item_selected(self, selected, deselected):
        self.font_style_list_model.clear()
        selected_font_list_item = selected
        selected_font_list_item_index = selected_font_list_item.indexes()[0]
        selected_font_list_item_text = selected_font_list_item_index.data(Qt.DisplayRole)
        # print(selected_item,selected_index)
        
        # append style list
        font_style_list = [style for style in QFontDatabase.styles(selected_font_list_item_text)]
        print(font_style_list)
        for style_name in font_style_list:
            item = QStandardItem(style_name)
            font = QFont(selected_font_list_item_text,12)
            # font.setStyle(style_name)
            item.setFont(QFont(font))  # Apply the font
            item.setSizeHint(QSize(100,20))
            self.font_style_list_model.appendRow(item)
        
        # append size list
        font_size_list = [size for size in QFontDatabase.pointSizes(selected_font_list_item_text)]
        print(font_size_list)
        self.font_size_list_model.setStringList((str(size) for size in font_size_list))
        
        # select style
        current_font_style = self.config['font_family']['style']
        font_style_select_item = self.font_style_list_model.findItems(current_font_style, Qt.MatchExactly) # MatchFixedString
        
        if not font_style_select_item:
            if font_style_select_item != current_font_style:
                self.font_style_list.setCurrentIndex(self.font_style_list_model.index(0,0))
                selected_style_list_item_text = self.font_style_list_model.itemFromIndex(self.font_style_list_model.index(0,0)).text()
        else:
            for item in font_style_select_item:
                selected_style_list_item_text = item.text()
                index = item.index()
                self.font_style_list_selectionmodel.select(index,QItemSelectionModel.Select)
                # selected_style_item_text = self.font_style_list_model.itemFromIndex(index).text()
        
        # select size
        current_font_size = self.config['font_family']['size']
        
        # 리스트에서 문자열 찾아 인덱스 가져오기
        indexes = self.font_size_list_model.match(
            self.font_size_list_model.index(0), Qt.DisplayRole, current_font_size, -1, Qt.MatchExactly)
        
        if indexes:
            # 찾은 인덱스로 선택하기
            index = indexes[0]
            self.font_size_list.setCurrentIndex(index)
            selected_size_list_item_text = index.row()
        else:
            # 인덱스 0을 선택하고 선택된 값 가져오기
            self.font_size_list.setCurrentIndex(self.font_size_list_model.index(0))
            selected_size_list_item_index = self.font_size_list.selectedIndexes()[0]
            selected_size_list_item_text = self.font_size_list_model.data(selected_size_list_item_index,Qt.DisplayRole)
        
        self.font_lineedit.setText(selected_font_list_item_text)
        self.font_lineedit.selectAll()
        self.font_style_lineedit.setText(selected_style_list_item_text)
        self.font_size_lineedit.setText(str(selected_size_list_item_text))
    
    def set_font_preview(self,font,style,size):
        font_family = f'font-family: {font}; font-style: {style}; font-size: {size}px;'
        return font_family
    
    def set_font_ok_button(self):
        print(0)

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
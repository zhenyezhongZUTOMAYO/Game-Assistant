import sys
import os
import subprocess
from PyQt5.QtWidgets import *
import RecognizePicture.Output
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QTextCursor
from totaltrigger import TotalTrigger#不断点击启动游戏
from qfluentwidgets import(
    SpinBox,ComboBox,CardWidget,setTheme,Theme,NavigationInterface,
    NavigationItemPosition,PrimaryPushButton,TitleLabel,BodyLabel,
    TransparentToolButton,FluentIcon,LineEdit,ToolButton,InfoBar,
    InfoBarPosition,MessageBox,FluentWindow,GroupHeaderCardWidget,
    setThemeColor,CompactSpinBox
)
#Version 1  by cy 2025/3/26

#  ======next task======= 
# modify class QComBox
# modify class QSpinBox 
# color setting


#  =====================

class GameAssistant(FluentWindow):
    def __init__(self):
        super().__init__()
        self.running = False  # 运行状态标志
        self.initUI()
        self.tr=TotalTrigger()
        self.process=None
        self.start=True
        self.create_action_buttons()

        #根据屏幕分辨率设置窗口大小
        # 获取屏幕分辨率
        screen=QDesktopWidget().screenGeometry()
        width=screen.width()
        height=screen.height()
        winwidth=(width//1920)*1000
        winheight=(height//1080)*600
        self.resize(winwidth,winheight)
        
    def initUI(self):
        self.COLOR_PALETTE = {# #98F5FF
    "primary": "#0078D4",       # 主色调
    "secondary": "#6B5B95",     # 辅助色
    "success": "#4CAF50",       # 成功状态
    "warning": "#FF9800",       # 警告状态
    "error": "#F44336",         # 错误状态
    "text_primary": "#212121",  # 主要文本
    "text_secondary": "#757575" # 次要文本
}
        self.FONT_CONFIG = {
    "title": ("微软雅黑", 16, QFont.DemiBold),
    "subtitle": ("微软雅黑", 14, QFont.Normal),
    "body": ("Segoe UI", 12),
    "button": ("Segoe UI", 13, QFont.Medium)
}
        self.setWindowTitle('游戏助手')

        self.resize(1000,600)
        setTheme(Theme.LIGHT)
        setThemeColor(self.COLOR_PALETTE["primary"])

        main_widget=QWidget()
        main_widget.setObjectName("MainWidget")
        # 主布局
        self.main_layout=QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # 左侧区域 
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # 使用说明区块
        self.using_card = self.create_instruction_card()
        
        # 文件地址区块
        self.file_card = self.create_file_card()
        
        # 目标刷取区块
        self.target_card = self.create_target_card()
        
        # 角色选择区块
        self.role_card = self.create_role_card()

  
        #group_layout.addWidget(self.create_instruction_card())
        #group_layout.addWidget(self.create_file_card())
        #group_layout.addWidget(self.create_target_card())
        #group_layout.addWidget(self.create_role_card())

        # 开始运行按钮
        self.start_btn = PrimaryPushButton("开始运行")
        self.start_btn.setObjectName("startButton")
        self.start_btn.clicked.connect(self.toggle_running)
        
        # 组装左侧布局
        left_layout.addWidget(self.using_card)
        left_layout.addWidget(self.file_card)
        left_layout.addWidget(self.target_card)
        left_layout.addWidget(self.role_card)
        left_layout.addWidget(self.start_btn)

        left_layout.addStretch(1)

        # 右侧区域 
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.logViewer = RecognizePicture.Output.LogViewer("log")
        self.output = RecognizePicture.Output.Output()
        self.output.set_log_viewer(self.logViewer)
        sys.stdout = self.output
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        right_layout.addWidget(self.logViewer)

        # 主布局比例设置
        self.main_layout.addWidget(left_widget, 5)  
        self.main_layout.addWidget(right_widget, 5)

        self.addSubInterface(
            interface=main_widget,
            icon=FluentIcon.HOME,
            text="主界面",
            position=NavigationItemPosition.TOP
        )
        self.logViewerx = RecognizePicture.Output.LogViewer("log")
        self.outputx = RecognizePicture.Output.Output()
        self.outputx.set_log_viewer(self.logViewerx)
        sys.stdout = self.outputx
        self.addSubInterface(
            interface=self.logViewerx,
            icon=FluentIcon.MESSAGE,
            text="运行日志",
            position=NavigationItemPosition.BOTTOM
        )

    def create_instruction_card(self):
        card=CardWidget()#'使用说明'
        layout = QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 文本部分
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        title = TitleLabel("使用说明")
        self.apply_typography(title, "title")
        text_layout.addWidget(title)
        body = BodyLabel("1. 请先阅读说明文档\n2. 配置必要参数\n3. 点击开始运行")
        self.apply_typography(body, "body")
        text_layout.addWidget(body)
        
        # 按钮部分
        btn = TransparentToolButton(FluentIcon.DOCUMENT)
        btn.clicked.connect(self.showDocumentation)#///未实现部分
        btn.setFixedSize(80, 60)
        
        layout.addWidget(text_widget)
        layout.addWidget(btn)

        return card

    def create_file_card(self):
        card = CardWidget()#"文件地址"
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)  # 统一边距
        layout.setSpacing(10)  # 元素间距
        #layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.file_path = LineEdit()
        self.file_path.setPlaceholderText("请选择游戏客户端路径...")
        self.file_path.setStyleSheet(f"""
        LineEdit {{
            border: 1px solid {self.COLOR_PALETTE['primary']}30;
            border-radius: 6px;
            padding: 6px;
            background-color: #FFFFFF;
        }}
        LineEdit:hover {{
            border-color: {self.COLOR_PALETTE['primary']}60;
        }}
    """)
        #游戏启动
        self.game_start=TransparentToolButton(FluentIcon.PLAY)
        self.game_start.clicked.connect(self.start_game)
        
        # 选择文件按钮
        self.btn = TransparentToolButton(FluentIcon.FOLDER)
        self.btn.setFixedSize(40,40)

        self.btn.clicked.connect(self.browse_file)
        
        layout.addWidget(self.file_path, 70)
        layout.addWidget(self.btn, 15)
        layout.addWidget(self.game_start,15)

        return card
    #可以加入关闭游戏的
    def start_game(self):
        if self.start:
            zzz_path = self.file_path.text().strip()
            if not zzz_path:
                QMessageBox.warning(self, "警告", "文件路径不能为空！", QMessageBox.Ok)
                return
            try:
                with open(zzz_path, 'rb') as f:
                    header = f.read(2)
                    if header != b'MZ':
                        QMessageBox.warning(self, "警告", "非有效的EXE文件", QMessageBox.Ok)
                        return

                    # 加入确认逻辑
                    os.startfile(zzz_path)
                    self.start=False
            except PermissionError:
                QMessageBox.critical(self, "权限错误", "没有权限或文件被其他程序使用", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"操作失败：{str(e)}", QMessageBox.Ok)
    
    def load_existing_file_path(self):
        """初始化加载文件路径"""
        config_file = "Source/file_path.txt"
        try:
            # 检查文件是否存在
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    # 判断内容有效性（示例：路径需真实存在）
                    if first_line and os.path.exists(first_line):
                        self.file_path.setText(first_line)
        except Exception as e:
            self.show_warning( "配置错误", f"读取配置文件失败: {str(e)}")

    def browse_file(self):
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择文件", "", "All Files (*);;Text Files (*.txt)", options=options
        )
        
        if file_path:
            self.file_path.setText(file_path)
            self.save_current_path(file_path)  # 保存新路径

    def save_current_path(self, path):
        """保存路径到配置文件"""
        try:
            # 自动创建缺失目录
            os.makedirs(os.path.dirname("Source/file_path.txt"), exist_ok=True)
           
            
            with open("src/file_path.text", 'w', encoding='utf-8') as f:
                f.write(path + "\n")  # 添加换行符保持格式统一
        except Exception as e:
            QMessageBox.critical(None, "保存失败", f"路径保存失败: {str(e)}")

    def browse_file(self):
        default_path = r"C:"  # 你的默认路径
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            default_path,
            "All Files (*)"
        )

        if path and os.path.isfile(path):
            self.file_path.setText(path)
        elif path:  # 路径存在但不是文件
            self.show_warning( "错误", "请选择有效文件！")

    def create_target_card(self):
        card = CardWidget()#"目标刷取"
        layout = QHBoxLayout(card)
        
        # 输入框
        self.target_input = CompactSpinBox()#Compact
        self.target_input.setRange(0, 999)
        self.target_input.setValue(1)
        
        layout.addWidget(BodyLabel('刷取次数:'),20)
        layout.addWidget(self.target_input,80)
        card.setLayout(layout)
        return card

    def create_role_card(self):
        card = CardWidget()#"角色选择"
        layout = QHBoxLayout(card)
        
        self.role_combo = ComboBox()
        self.role_combo.addItems(["星见雅 凯撒 耀佳音", "目前暂不支持", "目前暂不支持"])

        layout.addWidget(BodyLabel("选择配队："))
        layout.addWidget(self.role_combo)
        
        return card
    def create_action_buttons(self):
    # 动态按钮颜色#{self.COLOR_PALETTE['primary']}
        self.start_btn.setStyleSheet(f"""
            PrimaryPushButton {{
                 background-color: {self.COLOR_PALETTE['primary']};                     
                border-radius: 8px;
                padding: 12px 24px;
                min-width: 120px;
            }}
            PrimaryPushButton:hover {{
                background-color: {self.COLOR_PALETTE['primary']}DD;
            }}
            PrimaryPushButton:pressed {{
                background-color: {self.COLOR_PALETTE['primary']}BB;
            }}
        """)
        # 图标按钮统一处理
        # icon_buttons = [self.btn, self.game_start]
        # for btn in icon_buttons:
        #     btn.setIconSize(QSize(20, 20))
        #     btn.setStyleSheet(f"""
        #         TransparentToolButton {{
        #             border-radius: 8px;
        #             padding: 8px;
        #         }}
        #         TransparentToolButton:hover {{
        #             background-color: {self.COLOR_PALETTE['primary']}10;
        #         }}
        #     """)
        

    def toggle_running(self):
        self.running =not self.running
        self.start_btn.setText('停止运行'if self.running else '开始运行')
        self.start_btn.setProperty('isRunning',self.running)
        self.start_btn.setStyle(QApplication.style())

        if self.running:
            self.show_success("","开始运行")
        else:
            self.show_success("","停止运行")

        if self.running:
            # subprocess.run(["powershell", "Start-Process", f"'{"E:\\MiHoYo\\miHoYo Launcher\\games\\ZenlessZoneZero Game\\ZenlessZoneZero.exe"}'", "-Verb", "RunAs"],
            #                creationflags=subprocess.CREATE_NO_WINDOW)
            self.process=subprocess.Popen([
                "powershell",
                "Start-Process",
                "python.exe",
                "-Verb", "RunAs",
                "-ArgumentList", f"'{__file__[0:__file__.find("Game-Assistant")] + "Game-Assistant\\totaltrigger.py"}'"
            ])
        else:
            self.process.terminate()

    def show_success(self,title,content):
        InfoBar.success(
            title=title,content=content,orient=Qt.Horizontal,
            isClosable=True,position=InfoBarPosition.TOP,duration=2000,
            parent=self
        )
    def show_warning(self,title,content):
        InfoBar.warning(
            title=title,
            content=content,duration=2000,
            parent=self
        ) 
    def showDocumentation(self):
        """显示说明文档"""
        content = """
        <h3>游戏助手使用说明</h3>
        <p>1. 请确保已安装游戏客户端</p>
        <p>2. 配置正确的客户端路径</p>
        <p>3. 选择需要刷取的角色</p>
        <p>4. 设置目标刷取次数</p>
        """
        w = MessageBox('使用说明', content, self)
        w.exec()
    def apply_typography(self,widget, font_type):
        font = QFont(*self.FONT_CONFIG[font_type])
        widget.setFont(font)
        if font_type == "title":
            widget.setStyleSheet(f"color: {self.COLOR_PALETTE['text_primary']};")
        elif font_type == "subtitle":
            widget.setStyleSheet(f"color: {self.COLOR_PALETTE['text_secondary']};")
    
    def append_log(self,text):
        #获得滚动位置
        scrollbar=self.logViewer.logText.verticalScrollBar()
        at_buttom=scrollbar.value()==scrollbar.maximum()

        cursor=self.logViewer.logText.textCursor()
        cursor.movePosition(QTextCursor.End)

        if "Error" in text:
            self.logViewer.logText.setTextColor(QColor(196,43,28))
        elif "Warring" in text:
            self.logViewer.logText.setTextColor(QColor(255, 184, 0))
        else:
            self.logViewer.logText.setTextColor(QColor(0, 0, 0))
        cursor.insertText(text)

        #自动滚动
        if at_buttom:
            cursor.movePosition(QTextCursor.End)
            self.logViewer.logText.setTextCursor(cursor)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"Source\配置@3x.ico"))#E:\zzzHollow脚本\src\icon\配置@3x.ico

    ex = GameAssistant()
    ex.show()
    screen=QDesktopWidget().screenGeometry()
    width=screen.width()
    height=screen.height()
    print(f"Info:屏幕宽度: {width}, 屏幕高度: {height}")

    # for i in range(100):
    #     print("Info: 程序启动成功")
    #     print("Warning: 检测到低电量")
    #     print("Error: 文件打开失败")
    #     print("suffix: 运行结束")
    #     print("InfoABC")
    sys.exit(app.exec_())

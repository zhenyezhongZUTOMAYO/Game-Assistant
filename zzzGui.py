import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from totaltrigger import TotalTrigger
#Version 1  by cy 2025/3/26

#  ======next task======= 
# modify class QComBox
# modify class QSpinBox 
# color setting
#  =====================

class GameAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = False  # 运行状态标志
        self.initUI()
        self.tr=TotalTrigger()
        self.process=None

    def initUI(self):
        self.setWindowTitle('游戏助手')
        self.setGeometry(300, 300, 1000, 600)
        
        # 主窗口容器
        main_widget = QWidget()
        main_widget.setObjectName("MainWidget")
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧区域 
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # 使用说明区块
        self.using_group = self.create_instruction_group()
        
        # 文件地址区块
        self.file_group = self.create_file_group()
        
        # 目标刷取区块
        self.target_group = self.create_target_group()
        
        # 角色选择区块
        self.role_group = self.create_role_group()
        
        # 开始运行按钮
        self.start_btn = QPushButton("开始运行")
        self.start_btn.setObjectName("startButton")
        self.start_btn.clicked.connect(self.toggle_running)
        
        # 组装左侧布局
        left_layout.addWidget(self.using_group)
        left_layout.addWidget(self.file_group)
        left_layout.addWidget(self.target_group)
        left_layout.addWidget(self.role_group)
        left_layout.addWidget(self.start_btn)
        left_layout.addStretch(1)

        # 右侧区域 
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("运行状态显示区域（预留）"))

        right_layout.addStretch(1)

        # 主布局比例设置
        main_layout.addWidget(left_widget, 5)  
        main_layout.addWidget(right_widget, 5)

        # 全局样式 
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: '微软雅黑';
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 1ex;
                font-size: 14px;
                color: #333;
                padding: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 6px;
                min-height: 28px;
            }
            QPushButton {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px 16px;
                color: #333;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
            QPushButton#startButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton#startButton:hover {
                background-color: #45a049;
            }
            QPushButton#startButton:checked {
                background-color: #f44336;
            }
            QSpinBox {
                padding: 4px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
        """)

    def create_instruction_group(self):
        group = QGroupBox("使用说明")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 文本部分
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.addWidget(QLabel("使用说明"))
        text_layout.addWidget(QLabel("1. 请先阅读说明文档2. 配置必要参数\n3. 点击开始运行"))
        
        # 按钮部分
        btn = QPushButton("前往")
        btn.setIcon(QIcon("Source/文档@3x.ico"))#E:/zzzHollow脚本/src/icon/文档@3x.ico
        btn.setStyleSheet("""
         QPushButton {
                background-color: #FFFFFF;  /* 固定白色背景 */
            }
        """
        )
        #btn.setIconSize(QSize(32,32))
        btn.setFixedSize(80, 60)
        
        layout.addWidget(text_widget)
        layout.addWidget(btn)
        group.setLayout(layout)
        return group

    def create_file_group(self):
        group = QGroupBox("文件地址")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 输入框
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("请选择文件路径...")
        
        # 选择按钮
        btn = QPushButton()
        btn.setIcon(QIcon(r"Source\文件夹.ico"))#E:\zzzHollow脚本\src\icon\文件夹.ico
        btn.setStyleSheet("""
         QPushButton {
                background-color: #FFFFFF;  /* 固定白色背景 */
            }
        """
        )
        btn.setFixedSize(32, 42)
        btn.setIconSize(QSize(24, 24))
        btn.clicked.connect(self.browse_file)
        
        layout.addWidget(self.file_path, 8)
        layout.addWidget(btn, 2)
        group.setLayout(layout)
        return group
    #槽函数
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
            QMessageBox.warning(self, "错误", "请选择有效文件！")

    def create_target_group(self):
        group = QGroupBox("目标刷取")
        layout = QHBoxLayout()
        
        # 输入框
        self.target_input = QSpinBox()
        self.target_input.setRange(0, 9999)
        self.target_input.setValue(100)
        
        layout.addWidget(self.target_input)
        #layout.addLayout(btn_layout)
        group.setLayout(layout)
        return group

    def create_role_group(self):
        group = QGroupBox("角色选择")
        layout = QHBoxLayout()
        
        # 下拉框
        #对于combobox组件的修改
        self.role_combo = QComboBox()
        #这里的item
        self.role_combo.addItems(["角色1", "角色2", "角色3"])
        
        layout.addWidget(QLabel("选择角色："))

        layout.addWidget(self.role_combo)
        group.setLayout(layout)
        return group

    def toggle_running(self):
        """
        self.running = not self.running
        self.start_btn.setText("停止运行" if self.running else "开始运行")
        self.start_btn.setStyleSheet("""
        #   background-color: %s;
        """ % ("#DADFE4" if self.running else "#497CB5"))
        """
        self.running = not self.running
        self.start_btn.setText("停止运行" if self.running else "开始运行")
        #self.start_btn.setContentsMargins(100,100,100,100)
        #self.start_btn.setSizePolicy(50,50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;  /* 固定白色背景 */
                color: #000000;            /* 黑色字体 */
                border: 1px solid %s;      /* 动态边框颜色 */
                border-radius: 10px;       /* 圆角半径 */
                padding: 12px 16px;         /* 内边距 */
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F5F5F5;  /* 悬停状态 */
            }
            QPushButton:pressed {
                background-color: #EEEEEE;  /* 按下状态 */
            }
        """% ("#000000" if self.running else "#000000")) 
            #% ("#FF4444" if self.running else "#497CB5"))  # 根据状态改变边框颜色
        #启动exe文件
        
        zzz_path=self.file_path.text().strip()
        if not zzz_path:
            QMessageBox.warning(self, "警告", "文件路径不能为空！", QMessageBox.Ok)
            return
        try:
            with open(zzz_path,'rb') as f:
                header = f.read(2)
                if header != b'MZ':
                    QMessageBox.warning(self, "警告", "非有效的EXE文件", QMessageBox.Ok)
                    return
                
                #加入确认逻辑
                os.startfile(zzz_path)
        except PermissionError:
            QMessageBox.critical(self,"权限错误","没有权限或文件被其他程序使用",QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self,"错误",f"操作失败：{str(e)}",QMessageBox.Ok)
           #exe启动
        
        if self.running:
            subprocess.run(["powershell", "Start-Process", f"'{"E:\\MiHoYo\\miHoYo Launcher\\games\\ZenlessZoneZero Game\\ZenlessZoneZero.exe"}'", "-Verb", "RunAs"],
                           creationflags=subprocess.CREATE_NO_WINDOW)
            self.process=subprocess.Popen([
                "powershell",
                "Start-Process",
                "python.exe",
                "-Verb", "RunAs",
                "-ArgumentList", f"'{__file__[0:__file__.find("Game-Assistant")] + "Game-Assistant\\totaltrigger.py"}'"
            ])
        else:
            self.process.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"Source\配置@3x.ico"))#E:\zzzHollow脚本\src\icon\配置@3x.ico
    ex = GameAssistant()
    ex.show()
    sys.exit(app.exec_())

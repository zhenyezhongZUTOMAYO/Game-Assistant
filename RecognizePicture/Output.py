import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtCore import Qt, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import *

from PyQt5.QtGui import  QColor, QTextCharFormat, QTextCursor

from qfluentwidgets import (
    ScrollArea, TextEdit, CardWidget, PrimaryToolButton,
    FluentIcon as FIF, CheckBox, StrongBodyLabel, setFont,
    isDarkTheme, InfoBar
)
class Output(QObject):
    new_output = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout  # 保存原始的标准输出
        self.log_viewer = None

    def set_log_viewer(self, log_viewer):
        self.log_viewer = log_viewer

    # 采用时间+信息输出
    def write(self, text):
        # timestamp = QDateTime.currentDateTime().toString("HH:mm:ss")
        # # self.new_output.emit(f"{timestamp} {text}")
        # if self.log_viewer:
        #     if not text.endswith("\n"):
        #         text += "\n"
        #     self.log_viewer.appendLog(f"{timestamp} {text}")
        # if self.original_stdout is not None:
        #     # 直接输出到控制台
        #     self.original_stdout.write(f"{timestamp} {text}")
        # else:
        #     print(f"警告：original_stdout 为 None，无法输出: {text}")
        # self.original_stdout.write(text)
        if not text.strip():  # 忽略空内容
            return
            
        timestamp = QDateTime.currentDateTime().toString("HH:mm:ss")
        if self.log_viewer:
            if not text.endswith("\n"):
                text += "\n"
            self.log_viewer.appendLog(f"{timestamp} {text}")
        if self.original_stdout is not None:
            self.original_stdout.write(text)
        # pass

    # 刷新输出缓冲区
    def flush(self):
        self.original_stdout.flush()


class log_output(QObject):
    new_output = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout
        self.log_viewer = None
    def set_log_viewer(self, log_viewer):
        """设置日志显示组件"""
        self.log_viewer = log_viewer

    def log_message(self, text):
        """向日志显示组件输出信息"""
        if self.log_viewer:
            self.log_viewer.appendLog(text)  # 调用 LogViewer 的 appendLog 方法
        else:
            print(f"警告：log_viewer 未设置，无法输出日志: {text}")


class LogViewer(CardWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("LogViewer")
        self.title = title
        self.initUI()
        self.initSignals()

    def initUI(self):
        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)

        # 标题栏
        self.titleLabel = StrongBodyLabel(self.title)
        setFont(self.titleLabel, 16)

        # 工具栏
        self.toolBar = QWidget()
        self.toolLayout = QHBoxLayout(self.toolBar)
        self.toolLayout.setContentsMargins(0, 0, 0, 0)

        self.autoScrollCheck = CheckBox("自动滚动")
        self.autoScrollCheck.setChecked(True)
        self.clearBtn = PrimaryToolButton(FIF.DELETE)
        self.saveBtn = PrimaryToolButton(FIF.SAVE)

        self.toolLayout.addWidget(self.autoScrollCheck)
        self.toolLayout.addStretch(1)
        self.toolLayout.addWidget(self.clearBtn)
        self.toolLayout.addWidget(self.saveBtn)

        # 日志显示区域
        self.scrollArea = ScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.logEdit = TextEdit()
        self.logEdit.setReadOnly(True)
        self.logEdit.setStyleSheet("""
            TextEdit {
                background-color: #FFFFFF; /* 设置背景颜色为白色 */
                border: none;
                font: 14px 'Segoe UI';
            }
        """)

        font=self.logEdit.font()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.logEdit.setFont(font)

        self.scrollArea.setWidget(self.logEdit)

        # 移除 ScrollArea 的黑框
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #FFFFFF; /* 设置背景颜色为白色 */
            }
            QScrollBar:vertical {
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background-color: #888;
                min-height: 0px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # 组装布局
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.toolBar)

        self.updateStyle()

    def initSignals(self):
        self.clearBtn.clicked.connect(self.clearLogs)
        self.saveBtn.clicked.connect(self.saveLogs)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.autoScroll)

    def updateStyle(self):
        bg_color = QColor(255, 255, 255) if not isDarkTheme() else QColor(32, 32, 32)
        self.setStyleSheet(f"""
            LogViewer {{
                background-color: {bg_color.name()};
                border-radius: 4px;
                border: none;
            }}
        """)

    def appendLog(self, text):
        cursor = self.logEdit.textCursor()
        cursor.movePosition(QTextCursor.End)

        # 设置文本颜色
        format = QTextCharFormat()
        # if text.startswith("Error"):r
        if "error" in text:
            text = text.replace("error", "")
            format.setForeground(QColor(196, 43, 28))
        # elif text.startswith("Warning"):
        elif "warning" in text:
            text = text.replace("warning", "")
            format.setForeground(QColor(255, 184, 0))
        # elif text.startswith("Info"):
        elif "info" in text:
            text = text.replace("info", "")
            format.setForeground(QColor(0, 122, 204) if not isDarkTheme() else QColor(96, 205, 255))
        else:
            return
        block_format=cursor.blockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.setBlockFormat(block_format)
        cursor.insertText(text, format)

        # 保持500行限制
        if self.logEdit.document().lineCount() > 500:
            cursor.select(QTextCursor.Document)
            cursor.removeSelectedText()

    def autoScroll(self):
        if self.autoScrollCheck.isChecked():
            scrollbar = self.scrollArea.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def clearLogs(self):
        self.logEdit.clear()
        InfoBar.success("", "日志已清空", parent=self.window(), duration=1500)

    def saveLogs(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "", "文本文件 (*.txt)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.logEdit.toPlainText())
                InfoBar.success("", f"日志已保存至\n{path}", parent=self.window(), duration=2000)
            except Exception as e:
                InfoBar.error("", f"保存失败: {str(e)}", parent=self.window(), duration=2000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    output = Output()
    log_viewer = LogViewer("日志系统")
    output.set_log_viewer(log_viewer)
    sys.stdout = output

    log_viewer.show()

    # 模拟日志输出
    import time
    for i in range(10):
        print(f"日志信息 {i}")
        # time.sleep(1)

    sys.stdout = output.original_stdout
    sys.exit(app.exec_())
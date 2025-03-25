import threading
import time
import pynput
import pyautogui
import ctypes
from Recognize import Recognize  # 只导入类，不共享实例

class LevelSystem:
    def __init__(self):
        self.rec = Recognize()  # 独立实例
        self.keyboard = pynput.keyboard.Controller()

    def _method(self, location, _):
        """专用交互方法（不触发对话）"""
        self.keyboard.press('f')
        time.sleep(0.5)
        self.keyboard.release('f')
        self.rec.end = True

    def start_detection(self):
        """启动入口检测"""
        entrance_path = f"{self.rec.source_path}Game-Assistant\\Source\\{self.rec.resolutionRatio[0]}GanTan.png"
        self.rec.ToRecognizeIfThen(entrance_path, self._enter_flow)

    def _enter_flow(self, location, _):
        """完整的进入流程"""
        # 1. 追踪目标
        self.rec.trakingImage(f"{self.rec.source_path}Game-Assistant\\Source\\{self.rec.resolutionRatio[0]}GanTan.png", 0.8)
        
        # 2. 执行交互
        self._method(None, None)
        
        # 3. 验证结果
        if self._verify_entrance():
            print("成功进入下一层！")
        else:
            print("进入下一层失败")

def start():
    """模块启动入口"""
    system = LevelSystem()
    system.start_detection()

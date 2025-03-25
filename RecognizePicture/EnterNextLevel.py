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
        _enter_flow()

    def start_detection(self):
        """线程化启动入口检测"""
        thread_a = threading.Thread(target=rec.ToRecognizeIfThen, args=[rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "levelEntrance.png", method,confidence])
        thread_a.start()
        rec.trakingImage(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "levelEntrance.png",confidence)

    def _enter_flow(self):
        rec =Recognize.Recognize()
        thread_b = threading.Thread(target=rec.ToRecognizeConWhere, args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"levelEntrance.png",])
        thread_b.start()
        stop=0
        while True:
            rec.pa()
            if not thread_b.is_alive():
                return False
            if rec.real:
                pyautogui.click(rec.x,rec.y)
                stop=0
            else:
                """
                识别不到的停止机制如果连续10次识别不到那么终止
                """
                stop+=1
                if stop > 9:
                    rec.end=True
            rec.vb()


    def start(self):
        """模块启动入口"""
        system = LevelSystem()
        system.start_detection()

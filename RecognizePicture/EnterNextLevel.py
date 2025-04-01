import time
import pynput
import pyautogui
import os
from Recognize import Recognize
import threading
import sys
import ctypes


class LevelSystem:
    def __init__(self):
        self.rec = Recognize()  # 独立实例
        self.keyboard = pynput.keyboard.Controller()
        self.confidence = 0.7  # 确保拼写正确，并且有默认值
        self.running = False
        self.thread = None

    def RecognizeTarget(self):
        """识别目标的方法"""
        # 尝试识别 Timestamp.png
        if self.rec.ToRecognizeConWhere(
            self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Timestamp.png",
            self.confidence
        ):
            return True
            
        # 尝试识别 WuShang.png
        if self.rec.ToRecognizeConWhere(
            self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "WuShang.png",
            self.confidence
        ):
            return True
            
        return False

    def trackingTarget(self):
        """追踪目标的方法"""
        self.rec.end = False
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stop = 0
        
        while not self.rec.end:
            self.rec.pa()
            print("目标开始执行")
            
            # 在主线程中进行识别
            if self.RecognizeTarget():
                # 调整视角对准目标
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) / 2)), 0)
                time.sleep(0.5)  # 等待视角调整完成
                
                # 按W键靠近目标
                self.keyboard.press('w')
                time.sleep(1)  # 靠近1秒
                self.keyboard.release('w')
                print("已靠近目标")
                
                # 按F键与目标交互
                self.keyboard.press('f')
                time.sleep(0.5)
                self.keyboard.release('f')
                print("已与目标交互")
                
                # 等待进入下一层
                time.sleep(2)
                print("目标操作完成")
            else:
                stop += 1
                if stop > 3:
                    print("目标未识别到")
                    self.rec.end = True
                self.rec.vb()
                continue
                
            self.rec.vb()

    def start(self):
        """模块启动入口"""
        print("程序启动")
        self.trackingTarget()
        try:
            while True:  # 保持主线程运行
                time.sleep(1)
        except KeyboardInterrupt:
            print("程序退出")


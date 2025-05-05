import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import pynput
import pyautogui
import os
from Recognize import Recognize
import threading

import ctypes
import random



class LevelSystem:
    def __init__(self):
        self.rec = Recognize()  # 独立实例
        self.keyboard = pynput.keyboard.Controller()
        self.confidence = 0.8  # 确保拼写正确，并且有默认值
        self.running = False
        self.thread = None
        self.signal = []
        self.lock=[]
        self.curpaint = ""
        self.p = 0.3
        self.end = False
        self.real = False
        self.x = None
        self.y = None
        self.As = None
        self.black = 2

    # def RecognizeTarget(self):
    #     """识别目标的方法"""
    #     # 尝试识别 Timestamp.png
    #     if self.rec.ToRecognizeConWhere(
    #         self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Timestamp.png",
    #         self.confidence
    #     ):
    #         return True
    #
    #     # 尝试识别 WuShang.png
    #     if self.rec.ToRecognizeConWhere(
    #         self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "WuShang.png",
    #         self.confidence
    #     ):
    #         return True
    #
    #     return False
    def tankingImage(self,image_path):
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stop = 0
        while True:
            try:
                if self.end:
                    return
                # print(f"开始识别{image_path}")
                location = pyautogui.locateOnScreen(image_path, confidence=0.8)
                if location is not None:
                    self.x, self.y = pyautogui.center(location)
                    self.real=True
            except Exception as e:
                self.real=False
                if self.end:
                    return False
            if self.real:  # 不断找到位置
                print("正在操作")
                # 模拟鼠标的移动
                self.signal[1] = 0
                # print(f"Recognize.signal:{self.signal}")
                if self.lock[2] > 0:
                    self.end = True
                    while self.lock[2] > 0:
                        time.sleep(1)
                        print("Target被锁住!")
                    print("Target解锁")
                # print("到这里的第二步")
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.x - center_x) // 2)), 0)
                stop = 0
                self.keyboard.press('w')
                time.sleep(0.4)
                self.keyboard.release('w')
            else:
                print("将signal赋值为1")
                stop += 1
                if stop > 3:
                    self.signal[1] = 1
                    return

    def RecognizeTarget(self, lock):
        print("Info 开始识别    门")
        next = ["DaiJiaZhiJian", "DaiJiaZhiJian1",  "OuRan", "OuRan1", "ZhiYouHuiTan", "ZhiYouHuiTan1",
                "levelEntrance", "levelEntrance1", "Break",  "Break1", "BangBu", "BangBu1",
                "JiShi", "JiShi1", "TimeStamp", "TimeStamp1", "WuShang", "WuShang1",
                "YingBi", "YingBi1", "ZhanBei", "ZhanBei1", "Boss", "Boss1", "AnotherBoss", "AnotherBoss1"]
        while True:
                # self.rec.pb()
                # if self.rec.end:
                #     self.rec.va()
                #     # print("退出")
                #     return
                for i in next:
                    image_path_1 = self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        self.rec.resolutionRatio[0]) + f"{i}.png"
                    print(f"门正在识别{i}")
                    if i[-1] == "1":
                        p = random.random()
                        if p >= self.p:
                            continue
                    self.p += 0.03
                    if self.rec.ToRecognizeWhere(image_path_1):
                        # self.As.THRESHOLD = 200000000
                        if i == "BangBu" or i == "BangBu1" or i == "ZhanBei" or i == "ZhanBei":
                            self.black -= 1
                            if self.black > 0:
                                continue
                        else:
                            self.black = 4
                        self.rec.lock = self.lock
                        self.p = 0.3
                        self.signal[1] = 0
                        self.curpaint = i
                        self.end = False
                        print(f"门成功识别{i}")
                        if self.curpaint[-1] == "1":
                            keyboard = pynput.keyboard.Controller()
                            for j in range(0, 3):
                                keyboard.press('f')
                                time.sleep(0.2)
                                keyboard.release('f')
                                time.sleep(0.2)
                            keyboard.press('s')
                            time.sleep(1.7)
                            keyboard.release('s')
                            i = i[0:len(i)-1]
                        thread_a = threading.Thread(target=self.rec.ToRecognizeColorIfThen, args=[self.method, 2])
                        thread_a.daemon = True
                        thread_a.start()
                        print("调用method")
                        # print(f"self.rec.sa:{self.rec.sa}")
                        # print(f"self.rec.sb:{self.rec.sb}")
                        self.rec.end = False
                        print("准备tracking")
                        image_path_1 = self.rec.source_path + "Game-Assistant\\Source\\" + str(
                            self.rec.resolutionRatio[0]) + f"{i}.png"
                        self.tankingImage(image_path_1)
                        self.rec.end = True
                        thread_a.join()
                        # print("已经tracking结束")
                        print(f"追踪结束{i}")
                        # image_path_2 = self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        #     self.rec.resolutionRatio[0]) + f"{self.curpaint + "1"}.png"
                        # if self.rec.ToRecognizeWhere(image_path_2):
                        #     self.rec.sa = 0
                        #     self.rec.sb = 1
                        #     self.rec.end = False
                        #     print(f"门成功识别{i}")
                        #     self.curpaint=i+"1"
                        #     thread_a = threading.Thread(target=self.rec.ToRecognizeIfThen, args=[
                        #         self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        #             self.rec.resolutionRatio[0]) + "Inter.png", self.method, 0.8, 2])
                        #     thread_a.start()
                        #     self.rec.end = False
                        #     print("准备tracking")
                        #     self.rec.trakingImage(image_path_2, sleep=0.2, lock=2)
                        # self.signal[1] = 1
                        # stop=0
                        # while stop<5:
                        #     stop+=1
                        #     if self.rec.ToRecognizeWhere(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"Confirm0.png"):
                        #         pyautogui.click(self.rec.x,self.rec.y)
                        #         break
                        #
                        # self.signal[1]=1
                        # self.As.THRESHOLD = 340000000
                    # try:
                    #     # 在屏幕上查找图片
                    #     location = pyautogui.locateOnScreen(image_path_1, confidence=0.8)
                    #
                    #     if location is not None:
                    #         # 获取图片的中心坐标
                    #         self.rec.x, self.rec.y = pyautogui.center(location)
                    #         self.rec.real=True
                    #         self.rec.va()
                    #         print(f"{i}:  第{i}张图片找到图片，坐标位于: ({self.rec.x}, {self.rec.y})")
                    #     else:
                    #         print("未找到图片")
                    # except Exception as e:
                    #     print(f"发生错误: {e}")
                #----识别失败

                    # print("识别成功")
                # if not self.rec.real:
                #     self.rec.va()
                #     # print("识别失败")
                #     if self.rec.end:
                #         return False

    # def trackingTarget(self):
    #     """追踪目标的方法"""
    #     recognize_thread = threading.Thread(target=self.RecognizeTarget)
    #     recognize_thread.start()
    #     screen_width, screen_height = pyautogui.size()
    #     center_x = screen_width // 2
    #     center_y = screen_height // 2
    #     stop = 0
    #     while True:
    #         print("目标开始执行")
    #
    #         # 创建识别线程
    #
    #
    #         # 等待识别结果
    #         self.rec.pa()  # 开始识别前调用一次pa
    #
    #         if self.rec.real:  # 使用rec.real来判断识别结果
    #
    #             # 调整视角对准目标
    #             stop = 0
    #             ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x-center_x)/2)), 0)
    #
    #             # 按W键靠近目标
    #             self.keyboard.press('w')
    #             time.sleep(1)  # 靠近1秒
    #             self.keyboard.release('w')
    #             print("已靠近目标")
    #
    #             # 按F键与目标交互
    #             self.keyboard.press('f')
    #             time.sleep(0.5)
    #             self.keyboard.release('f')
    #             # print("已与目标交互")
    #             self.rec.vb()
    #             # 等待进入下一层
    #             print("目标操作完成")
    #         else:
    #             stop += 1
    #             if stop > 3:
    #                 print("目标未识别到")
    #                 self.rec.vb()
    #                 return  # 直接返回，结束函数
    #             self.rec.vb()  # 识别失败也要通知消费者
    # def trackingTarget(self):
    #     self.rec.end = False
    #     thread_a = threading.Thread(target=self.RecognizeTarget)
    #     thread_a.start()
    #     screen_width, screen_height = pyautogui.size()
    #     center_x = screen_width // 2
    #     center_y = screen_height // 2
    #     stop = 0
    #     while True:
    #         self.rec.pa()
    #         print("Target开始执行")
    #         # print("进入操作")
    #         if not thread_a.is_alive():
    #             self.rec.vb()
    #             return False
    #         if self.rec.real:
    #             print("正在操作")
    #             stop = 0
    #             ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) // 2)), 0)
    #         else:
    #             stop += 1
    #             if stop > 3:
    #                 print("Target未识别到")
    #                 self.rec.end = True
    #             self.rec.vb()
    #             # print("操作完成-误操作")
    #             continue
    #         self.rec.keyboard.press('w')
    #         time.sleep(1)
    #         self.rec.keyboard.release('w')
    #         self.rec.vb()

    def method(self, rec, location):
        print("开始method")
        self.signal[1] = 1
        keyboard = pynput.keyboard.Controller()
        self.rec.keyboard.release('w')
        if self.curpaint[-1] == "1":
            for i in range(0, 3):
                keyboard.press('f')
                time.sleep(0.2)
                keyboard.release('f')
                time.sleep(0.2)
            print("f")
            self.signal[1] = 1
            self.end = True
            return
        image_path_2 = self.rec.source_path + "Game-Assistant\\Source\\" + str(
            self.rec.resolutionRatio[0]) + f"{self.curpaint+"1"}.png"
        if self.rec.ToRecognizeWhere(image_path_2):
            for i in range(0, 3):
                keyboard.press('f')
                time.sleep(0.2)
                keyboard.release('f')
                time.sleep(0.2)
            print("f")
            if self.curpaint == "BangBu" or self.curpaint == "BangBu1":
                self.black = 4
            self.signal[1] = 1
            self.end = True
        else:
            self.end = True

    # def Fifexist(self):
    #     print("调用fif")
    #     thread_b = threading.Thread(target=self.rec.ToRecognizeIfThen, args=[self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Inter.png",self.method])
    #     thread_b.start()

    def start(self,lock):
        """模块启动入口"""
        # print("程序启动")
        while True:
            print("门启动")
            self.RecognizeTarget(lock)
        # thread_a=threading.Thread(target=self.rec.ToRecognizeIfThen, args=[self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"Inter.png",self.method])
        # thread_a.start()
        # self.trackingTarget()

